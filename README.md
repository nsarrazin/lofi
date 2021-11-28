# Stochastic lo-fi hip-hop generator
## Installation
```
git clone git@github.com:nsarrazin/lofi.git
```
### Development
This starts the server on http://localhost:3000/ with debug mode and it supports auto-reload for both front and backend.
```
npm run install:dev
npm run start:dev
```
### Docker
This starts the react app on http://localhost:8000/web/ using gunicorn and nginx for deployment purposes.
```
npm run build:docker
npm run start:docker
```

## Goal for MVP
### Back-end
 - [x] Set up a webserver with socket.io support
 - [x] Implement a customizable `Instrument` class which outputs generated MIDI chunks 
-  [x] Implement a `Conductor` class which holds all the meta information (keys, bpm, instruments, etc.)
-  [ ] Implement a `Chords` class which deals with generating and distributing the chord progression 
-  [ ] Implement a `Rythm` class to deal with rythmic phrasing, subdivsion of the measure
-  [ ] Implement an API to communicate meta information to the client

### Front-end
- [x] Set up a basic webapp with react and a socket.io client 
- [x] Implement a basic `Player` class that can play an instrument and receive midi chunks
- [x] Implement a ToneJS `Transport` to deal with scheduling notes rythmically even if socket messages are delayed
- [ ] Implement a `Master` class to deal with master volume, effects like reverb etc. 
- [ ] Add display of what's currently being played for each `Player` (piano roll ? display notes?)
- [ ] Find a way to read the meta information from the API
 
### CI/CD
- [x] Have a working docker container for flask
- [x] Have a working docker container for nginx serving react app
- [x] Setup a docker-compose file to handle easy deployment
- [x] Have a proper build process with build/deployment artefacts
- [x] Handle environment variables so that the front-end knows where to find the flask server

## Ressources for further reading
- backend:
    - flask-socketio : https://flask-socketio.readthedocs.io/en/latest/
    - midi-util : https://midiutil.readthedocs.io/en/1.2.1/
    - ChordalPy : https://github.com/P-bibs/ChordalPy (dope, love it)
- frontend:
    - toneJS (sounds, effect, sequencer): 
        - https://github.com/Tonejs/Tone.js
        - https://medium.com/dev-red/tutorial-lets-make-music-with-javascript-and-tone-js-f6ac39d95b8c
    - midi websocket: https://github.com/fa-m/midi-websocket
    - soundfonts : https://github.com/gleitz/midi-js-soundfont

