import ChordalPy as cp
import numpy as np
import json

Q = np.load("matrix.npy")
statespace = json.load(open("statespace.json", "r"))

class Chords:
    def __init__(self, master) -> None:
        self.master = master

        self._chord_name = "C:maj"
        self._next_chord_name = "C:maj"

    @property
    def chord(self):
        return cp.parse_chord(self._chord_name)

    @property
    def next_chord(self):
        return cp.parse_chord(self._next_chord_name)

    def _send(self):
        self.master.io.emit("chords", [self._chord_name, self._next_chord_name])

    def update(self):
        self._chord_name = self._next_chord_name

        i = statespace.index(self._chord_name)
        P = np.power(Q[i, :], 0.7)
        P /= P.sum() # normalize
        
        self._next_chord_name = np.random.choice(statespace,p=P)
        self._send()


if __name__ == "__main__":
    mvp = Chords(None)

    for n in range(50):
        mvp.update()
        my_chord = mvp.chord
        spelling = my_chord.get_spelling()