import time 
from threading import Thread

from midiutil import MIDIFile

degrees = [0, 2, 4, 5, 7, 9, 11, 12] # MIDI note number
roots = [62,67,60]
track = 0
channel = 0
duration = 1 # In beats
tempo = 60 # In BPM
volume = 100 # 0-127, as per the MIDI p


class PlayerMIDI:
    def __init__(self, io=None, path="midi-default") -> None:
        self._kill = False
        self._thread = None
        self.io = io
        self.path = path

        self.n = 0

    def start(self):
        self._thread = Thread(target=self._update)
        self._thread.start()
    
    def stop(self):
        self._kill = True
        self._thread.join()

    def _send(self):
        with open("dump.mid", "rb") as input_file:
            self.io.emit(self.path, input_file.read(), json=False)

    def _generate_midi(self):
        MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track

        MyMIDI.addTempo(0, 0, 60)

        for n, pitch in enumerate(degrees):
            MyMIDI.addNote(0,0, roots[self.n]+pitch, (n)/4, 1/4, volume)
        
        with open("dump.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
    
    def _update(self):
        while not self._kill:

            self._generate_midi()
            if self.io is not None:
                self._send()
            
            self.n = (self.n+1) % 3
            
            time.sleep(2*60*1/tempo)