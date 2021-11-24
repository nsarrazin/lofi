import React from 'react';
import { Player } from './features/player';
import './App.css';

import {SocketContext, socket} from './context/socket';
import * as Tone from 'tone'

const piano = new Tone.Sampler({
	urls: {
    A0: "A0.mp3",
    C1: "C1.mp3",
    "D#1": "Ds1.mp3",
    "F#1": "Fs1.mp3",
    A1: "A1.mp3",
    C2: "C2.mp3",
    "D#2": "Ds2.mp3",
    "F#2": "Fs2.mp3",
    A2: "A2.mp3",
    C3: "C3.mp3",
    "D#3": "Ds3.mp3",
    "F#3": "Fs3.mp3",
    A3: "A3.mp3",
    C4: "C4.mp3",
    "D#4": "Ds4.mp3",
    "F#4": "Fs4.mp3",
    A4: "A4.mp3",
    C5: "C5.mp3",
    "D#5": "Ds5.mp3",
    "F#5": "Fs5.mp3",
    A5: "A5.mp3",
    C6: "C6.mp3",
    "D#6": "Ds6.mp3",
    "F#6": "Fs6.mp3",
    A6: "A6.mp3",
    C7: "C7.mp3",
    "D#7": "Ds7.mp3",
    "F#7": "Fs7.mp3",
    A7: "A7.mp3",
    C8: "C8.mp3"
  	},
	release: 10,
	baseUrl: "https://tonejs.github.io/audio/salamander/",
});

const synth = new Tone.PolySynth(Tone.Synth);

Tone.Transport.bpm.value = 120;
Tone.Transport.loop = true;
Tone.Transport.loopEnd = "1m";
Tone.Transport.start();

function App() {
  return (
    <div className="App">
      <SocketContext.Provider value={socket}>
        Hello World from React!
      <Player source={piano} name='piano' type='chords' vol_init={-12}/>
      <Player source={synth} name='synthbass' type='bass' vol_init={0}/>
      </SocketContext.Provider>
    </div>
  );
}

// fix the transport so that it only applies new midi file when looping

// add meta info in flask with bpm and such
// add meta info to socket next to bytefile with length of midi file 
// add extra meta component with master volume, effect tracks, etc.
// add drumkit support
// improve front-end UI with volume sliders 
// fix the deployment with docker
export default App;