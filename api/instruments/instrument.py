import time 
from threading import Thread
from midiutil import MIDIFile

class Instrument:
    def __init__(self, type, name, loc=None) -> None:
        self.type = type
        self.name = name
        self.loc = loc if loc != None else f"dump-{self.type}-{self.name}.mid"
        self.path = f"midi-{self.type}-{self.name}"

        self._master = None
        self._kill = False
        self.i = 0

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, val):
        self._master = val
            
    def start(self):
        self._thread = Thread(target=self._update)
        self._thread.start()
    
    def stop(self):
        self._kill = True
        self._thread.join()
    
    def _rest(self):
        time.sleep(4*60*1/self.master.bpm) #sleep for 4 beats in second

    def _send(self):        
        with open(self.loc, "rb") as input_file:
            self.master.io.emit(self.path, input_file.read(), json=False)
    
    def _generate_midi(self):
        MIDI = MIDIFile(1)
        MIDI.addTempo(0,0, self.master.bpm)

        self._populate(MIDI)

        with open(self.loc, "wb") as output_file:
            MIDI.writeFile(output_file)

    def _populate(self, MIDI):
        MIDI.addNote(0, 0, 60, 1, 1, 100, annotation="default note")
    
    def _update(self):
        while not self._kill:
            self._generate_midi()
            self._send()            
            self._rest()
            self.i += 1

class Bass(Instrument):
    def __init__(self, type, name, loc=None) -> None:
        super().__init__(type, name, loc=loc)
    
    # plays arpeggios two octave lowers
    def _populate(self, MIDI): 
        degrees = [[0,3,7,10], [0, 4, 7, 10],[0, 4, 7, 11]]
        roots = [62,67,60]
        for n, pitch in enumerate(degrees[self.i%3]):
            MIDI.addNote(0,0, roots[self.i%3]+pitch-24, n, 1, 100)

class Piano(Instrument):
    def __init__(self, type, name, loc=None) -> None:
        super().__init__(type, name, loc=loc)
    
    def _populate(self, MIDI): # plays chords in shell voicings
        degrees = [[-12, 0,3,10], [-12, 0, 4, 10],[-12, 0, 4, 11]]
        roots = [62,67,60]

        for pitch in degrees[self.i%3]:
            MIDI.addNote(0,0, roots[self.i%3]+pitch-12, 0, 4, 100)