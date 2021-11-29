import ChordalPy as cp
import numpy as np
import json

Q = np.load("matrix.npy")
statespace = json.load(open("statespace.json", "r"))


class Chords:
    def __init__(self, master) -> None:
        self.master = master

        self.sequence = ["C:maj", "C:maj", "C:maj", "C:maj"]

    @property
    def chord(self):
        return cp.parse_chord(self._chord_name)

    @property
    def next_chord(self):
        return cp.parse_chord(self._next_chord_name)

    @property
    def _chord_name(self):
        return self.sequence[self.master.i % len(self.sequence)]

    @property
    def _next_chord_name(self):
        return self.sequence[(self.master.i + 1) % len(self.sequence)]

    def _send(self):
        self.master.io.emit("chords", [self._chord_name, self._next_chord_name])

    def update(self):
        for j in range(len(self.sequence)):
            i = statespace.index(self.sequence[j - 1])
            P = np.power(Q[i, :], self.master.spice)
            P /= P.sum()  # normalize

            chord = np.random.choice(statespace, p=P)
            self.sequence[j] = chord
        self._send()


if __name__ == "__main__":
    mvp = Chords(None)

    for n in range(50):
        mvp.update()
        my_chord = mvp.chord
        spelling = my_chord.get_spelling()
