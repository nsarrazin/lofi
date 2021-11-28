from threading import Thread
from midiutil import MIDIFile

import time, io, eventlet
import numpy as np
from utils import reversed_mapping

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
    def i(self):
        return self.master.i
    
    @property
    def chord(self):
        return self.master.cm.chord
    
    @property
    def next_chord(self):
        return self.master.cm.next_chord

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

def populate_bass(ins): #walk da bass
    octave = 3
    root = 12*octave + reversed_mapping[ins.chord.root]
    intervals = [i for _,i in ins.chord.intervals]

    notes = [root+interval for interval in intervals]

    next_root = 12*octave + reversed_mapping[ins.next_chord.root]
    next_intervals = [i for _,i in ins.next_chord.intervals]
    next_notes = [root+interval for interval in intervals]

    ins.MIDI.addNote(0, 0, root, 0.05, 1, 100)

    choices = np.random.choice(notes, size=2, replace=False)

    ins.MIDI.addNote(0, 0, choices[0], 1.05, 1, 100)
    ins.MIDI.addNote(0, 0, choices[1], 2.05, 1, 100)

    common_notes = list(set(notes).intersection(next_notes))
    if common_notes != []:
        note = np.random.choice(common_notes, size=1)
    else:
        note = np.random.choice(next_notes,size=1)

    ins.MIDI.addNote(0, 0, note[0],3.05,1,100)


def populate_piano(ins):  # plays chords
    octave = 4
    root = 12*octave + reversed_mapping[ins.chord.root]

    for _, interval in ins.chord.intervals:
        ins.MIDI.addNote(0, 0, root+interval, 0, 4, 100)


def populate_drum(ins): #boom tik tchak tik tik tchak tik (boom)
    kick = 60
    snare = 62
    hihat = 64
    wood = 65

    for n in range(4):
        ins.MIDI.addNote(0, 0, hihat, n+0.5, 1, 25)
    
    ins.MIDI.addNote(0, 0, kick, 0, 1, 75)

    if ins.i%4==0:
        ins.MIDI.addNote(0, 0, kick, 3.5, 1, 50)

    ins.MIDI.addNote(0, 0, snare, 1, 1, 80)
    ins.MIDI.addNote(0, 0, snare, 3, 1, 80)

def populate_pads(ins):
    pass

piano = Instrument.new("chords", "piano", populate_piano)
doublebass = Instrument.new("bass", "doublebass", populate_bass)
lofikit = Instrument.new("drums", "lofikit", populate_drum)
synthpad = Instrument.new("pads", "synthpad", populate_pads)