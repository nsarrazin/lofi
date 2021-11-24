from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from player_midi import PlayerMIDI, PlayerMIDIChord

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from player_midi import PlayerMIDI, PlayerMIDIChord


import eventlet
eventlet.monkey_patch()

class Conductor:
    def __init__(self, instruments) -> None:

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app,cors_allowed_origins="*")
        
        for instrument in instruments:
            instrument.io = self.socketio

        self.instruments = instruments

        self.bpm = 120
        self.key = "C"

    def start(self):
        for instrument in self.instruments:
            instrument.start()

        self.socketio.run(self.app, debug=True)
        
    def stop(self):
        for instrument in self.instruments:
            instrument.stop()