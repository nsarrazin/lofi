import time 
from threading import Thread

from midiutil import MIDIFile

degrees = [[0,3,7,10], [0, 4, 7, 10],[0, 4, 7, 11]]
roots = [62,67,60]
track = 0
channel = 0
duration = 1 # In beats
tempo = 120 # In BPM
volume = 100 # 0-127, as per the MIDI p


class PlayerMIDI:
    def __init__(self, path="midi-default", loc="dump.mid") -> None:
        self.path = path
        self.loc = loc
        self._io = None

        self.n = 0

        self._kill = False
        self._thread = None
    
    @property
    def io(self):
        return self._io

    @io.setter
    def io(self, val):
        self._io = val
    
    def start(self):
        self._thread = Thread(target=self._update)
        self._thread.start()
    
    def stop(self):
        self._kill = True
        self._thread.join()

    def _send(self):
        with open(self.loc, "rb") as input_file:
            self.io.emit(self.path, input_file.read(), json=False)

    def _generate_midi(self):
        MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track

        MyMIDI.addTempo(0, 0, tempo)

        for n, pitch in enumerate(degrees[self.n]):
            MyMIDI.addNote(0,0, roots[self.n]+pitch-24, (n), 1, volume)
        
        with open(self.loc, "wb") as output_file:
            MyMIDI.writeFile(output_file)
    
    def _update(self):
        while not self._kill:

            self._generate_midi()
            if self.io is not None:
                self._send()
            
            self.n = (self.n+1) % 3
            
            time.sleep(4*60*1/tempo)


class PlayerMIDIChord(PlayerMIDI):
    def _generate_midi(self):
        degrees = [[-12, 0,3,7,10], [-12, 0, 4, 7, 10],[-12, 0, 4, 7, 11]]
        roots = [62,67,60]
        volume = 25 # 0-127, as per the MIDI p

        MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track

        MyMIDI.addTempo(0, 0, tempo)

        for n, pitch in enumerate(degrees[self.n]):
            MyMIDI.addNote(0,0, roots[self.n]+pitch-12, 0, 4, volume)
        
        with open(self.loc, "wb") as output_file:
            MyMIDI.writeFile(output_file)