class Conductor:
    def __init__(self, app, io, instruments) -> None:

        self.app = app
        self.io = io

        for instrument in instruments:
            instrument.master = self

        self.instruments = instruments

        self.bpm = 120
        self.key = "C"

    def start(self):
        for instrument in self.instruments:
            instrument.start()

    def stop(self):
        for instrument in self.instruments:
            instrument.stop()
