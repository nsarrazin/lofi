import eventlet
class Conductor:
    def __init__(self, app, io, instruments) -> None:

        self.app = app
        self.io = io

        for instrument in instruments:
            instrument.master = self

        self.instruments = instruments

        self.bpm = 120
        self.key = "C"

        self.i = 0

        self._thread = None
        self._kill = False

    def start(self):
        self._thread = eventlet.spawn(self.update)

    def stop(self):
        self._kill = True
        self._thread.join()

    def _rest(self):
        eventlet.sleep(4 * 60 * 1 / self.bpm)  # sleep for 4 beats in second

    def update(self):
        while not self._kill:
            for instrument in self.instruments:
                instrument.update()

            self.i+=1
            self._rest()