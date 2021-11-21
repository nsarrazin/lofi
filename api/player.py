import time 
from threading import Thread

chords = [["D2", "D3", "F3", "C4"],
         ["G2", "G3", "B3", "F#4"],
         ["C2", "C3", "E3", "A4"]]

class Player:
    def __init__(self, io=None) -> None:
        self.chord = chords[0]
        self._kill = False
        self._thread = None
        self.io = io
        self.n = 0

    def start(self):
        self._thread = Thread(target=self._update)
        self._thread.start()
    
    def stop(self):
        self._kill = True
        self._thread.join()
    
    def _update(self):
        while not self._kill:
            self.chord = chords[self.n]

            self.n = (self.n+1) % 3
            
            if self.io is not None:
                self.io.emit('midi-piano', self.chord)
            
            time.sleep(2)