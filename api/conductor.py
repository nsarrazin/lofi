import eventlet

from chords import Chords


class Conductor:
    def __init__(self, app, io, instruments) -> None:

        self.app = app
        self.io = io

        for instrument in instruments:
            instrument.master = self

        self.instruments = instruments

        self.bpm = 80
        self.key = "C"

        self.cm = Chords(self)

        self.i = 0

        self._thread = None
        self._kill = False

        self.spice = 0.6

        @io.on("spice")
        def handle_chords(data):
            self.spice = float(data)
            self.cm.update()

    @property
    def chord(self):
        self.cm.chord

    def start(self):
        self._thread = eventlet.spawn(self.update)

    def stop(self):
        self._kill = True
        self._thread.join()

    def _rest(self):
        eventlet.sleep(4 * 60 * 1 / self.bpm)  # sleep for 4 beats in second

    def update(self):
        while not self._kill:
            self.cm.update()

            for i in range(8):
                for instrument in self.instruments:
                    instrument.update()

                self.i += 1
                self._rest()

                self.cm._send()
