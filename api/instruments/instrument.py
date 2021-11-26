from threading import Thread
from midiutil import MIDIFile

import time, io, eventlet


class Instrument:
    def __init__(self, type, name, log=False) -> None:
        self.type = type
        self.name = name
        self.log = log

        self._master = None
        self._kill = False
        self._generator = lambda instrument: instrument.MIDI.addNote(
            0, 0, 60, 1, 1, 100, annotation="default note"
        )

        self.i = 0

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
    def generator(self):
        return lambda: self._generator(self)

    @generator.setter
    def generator(self, val):
        # assert type(val) == "function", "The generator passed is not a function"
        self._generator = val

    def start(self):
        self._thread = eventlet.spawn(self._update)

    def stop(self):
        self._kill = True
        self._thread.join()

    def _rest(self):
        eventlet.sleep(4 * 60 * 1 / self.master.bpm)  # sleep for 4 beats in second

    def _send(self):
        with io.BytesIO() as buf:
            self.MIDI.writeFile(buf)
            self.master.io.emit(self.path, buf.getvalue(), json=False)
            if self.log:
                with open(self.dump, "wb") as output_file:
                    output_file.write(buf.getvalue())

    def _update(self):
        while not self._kill:
            self.MIDI = MIDIFile(1)
            self.MIDI.addTempo(0, 0, self.master.bpm)

            self.generator()
            self._send()
            self._rest()
            self.i += 1


def populate_bass(ins):
    degrees = [[0, 3, 7, 10], [0, 4, 7, 10], [0, 4, 7, 11]]

    roots = [62, 67, 60]
    for n, pitch in enumerate(degrees[ins.i % 3]):
        ins.MIDI.addNote(0, 0, roots[ins.i % 3] + pitch - 24, n, 1, 100)


def populate_piano(ins):  # plays chords in shell voicings
    degrees = [[-12, 0, 3, 10], [-12, 0, 4, 10], [-12, 0, 4, 11]]
    roots = [62, 67, 60]

    for pitch in degrees[ins.i % 3]:
        ins.MIDI.addNote(0, 0, roots[ins.i % 3] + pitch - 12, 0, 4, 100)


piano = Instrument.new("chords", "piano", populate_piano)
synthbass = Instrument.new("bass", "synthbass", populate_bass)
