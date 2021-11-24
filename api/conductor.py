from flask import Flask, render_template
from flask_socketio import SocketIO, emit


import eventlet
eventlet.monkey_patch()

class Conductor:
    def __init__(self, instruments) -> None:

        self.app = Flask(__name__)
        self.io = SocketIO(self.app,cors_allowed_origins="*")
        
        for instrument in instruments:
            instrument.master = self

        self.instruments = instruments

        self.bpm = 120
        self.key = "C"

    def start(self):
        for instrument in self.instruments:
            instrument.start()

        self.io.run(self.app, debug=True)
        
    def stop(self):
        for instrument in self.instruments:
            instrument.stop()