from threading import Thread
from midiutil import MIDIFile

import time, io, eventlet
import numpy as np

class Instrument:
    def __init__(self, type, name, log=False) -> None:
        self.type = type
        self.name = name
        self.log = log

        self._master = None
        # self._kill = False
        self._generator = lambda instrument: instrument.MIDI.addNote(
            0, 0, 60, 1, 1, 100, annotation="default note"
        )
    
    @classmethod
    def new(cls, type, name, generator):
        instrument = cls(type, name)
        instrument.generator = generator

        return instrument

    @property
    def path(self):
        return f"midi-{self.type}-{self.name}"

    @property
    def dump(self):
        return f"dump-{self.type}-{self.name}.mid"

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, val):
        self._master = val

    @property
    def i(self):
        return self.master.i

    @property
    def generator(self):
        return lambda: self._generator(self)
    
    @generator.setter
    def generator(self, val):
        self._generator = val

    def _send(self):
        with io.BytesIO() as buf:
            self.MIDI.writeFile(buf)
            self.master.io.emit(self.path, buf.getvalue(), json=False)
            if self.log:
                with open(self.dump, "wb") as output_file:
                    output_file.write(buf.getvalue())

    def update(self):
        self.MIDI = MIDIFile(1)
        self.MIDI.addTempo(0, 0, self.master.bpm)

        self.generator()
        self._send()

def populate_bass(ins):
    degrees = [[3, 7, 10, 3], [4, 7, 11, 4]]

    x=4
    roots = [73, 71] #F -> Eb
    roots=[root-7*(ins.i//x) \
            + 12*(ins.i//(x*2))
            + 12*(ins.i//(x*12)) for root in roots]        
    # ins.MIDI.addNote(0, 0, roots[ins.i % 2] - 12*3, 0, 1, 100)

    for n, pitch in enumerate(degrees[ins.i % 2]):
        ins.MIDI.addNote(0, 0, roots[ins.i % 2] + pitch - 12*3, n+0.05, 1, 100)


def populate_piano(ins):  # plays chords in shell voicings

    #min9 -> maj9
    degrees = [[0, 3, 7, 10, 14, 17], #min9
               [0, 4, 7, 11, 14, 19]] #maj9

    x=4
    roots = [73, 71] #F -> Eb
    roots=[root-7*(ins.i//x) \
            + 12*(ins.i//(x*2))
            + 12*(ins.i//(x*12)) for root in roots]        
    # every x bar we go down one fifth every 2x bar we go up one octave

    
    for pitch in degrees[ins.i % len(degrees)]:
        ins.MIDI.addNote(0, 0, roots[ins.i % len(roots)] + pitch - 12, 0, 4, 100)

def populate_drum(ins):
    kick = 60
    snare = 62
    hihat = 64
    wood = 65

    for n in range(4):
        ins.MIDI.addNote(0, 0, hihat, n+0.5, 1, 25)
    
    ins.MIDI.addNote(0, 0, kick, 0, 1, 75)

    if ins.i%6==0:
        ins.MIDI.addNote(0, 0, kick, 3.55, 1, 50)

    ins.MIDI.addNote(0, 0, snare, 1, 1, 80)
    ins.MIDI.addNote(0, 0, snare, 3, 1, 80)

def populate_pads(ins):
    pass
piano = Instrument.new("chords", "piano", populate_piano)
doublebass = Instrument.new("bass", "doublebass", populate_bass)
lofikit = Instrument.new("drums", "lofikit", populate_drum)
synthpad = Instrument.new("pads", "synthpad", populate_pads)