import time 
from threading import Thread

chords = [["D3", "D4", "F4", "C5"],
         ["G3", "G3", "B4", "F5"],
         ["C3", "C3", "E4", "B5"]]

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
        self.chord = chords[self.n]

        self.n = (self.n+1) % 3
        
        if self.io is not None:
            self.io.send(self.chord)
        
        time.sleep(2)

        if not self._kill:
            self._update()