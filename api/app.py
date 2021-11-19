from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from player import Player

import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")

player = Player(io=socketio)
player.start()

# @socketio.on('connect')
# def ws_connect():
#     emit('message', "connected")

@app.route("/")
def hello_world():
    return str(player.chord)

if __name__ == '__main__':
    socketio.run(app, debug=True)