from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from player_midi import PlayerMIDI, PlayerMIDIChord


import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")
    
player_piano = PlayerMIDIChord(io=socketio, path='midi-piano', loc="dump2.mid")
player_piano.start()

player_bass = PlayerMIDI(io=socketio, path='midi-bass', loc="dump.mid")
player_bass.start()

@app.route("/")
def hello_world():
    return "flask server is running !"

if __name__ == '__main__':
    socketio.run(app, debug=True)