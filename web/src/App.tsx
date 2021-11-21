import React from 'react';
import { Player } from './features/player';
import './App.css';

import {SocketContext, socket} from './context/socket';
import * as Tone from 'tone'

const piano = new Tone.Sampler({
	urls: {
		"C4": "C4.mp3",
		"D#4": "Ds4.mp3",
		"F#4": "Fs4.mp3",
		"A4": "A4.mp3",
	},
	release: 1,
	baseUrl: "https://tonejs.github.io/audio/salamander/",
});

const synth = new Tone.PolySynth(Tone.Synth);

function App() {
  return (
    <div className="App">
      <SocketContext.Provider value={socket}>
        Hello World from React!
      <Player instrument={piano} name='piano'/>
      <Player instrument={synth} name='synth'/>
      </SocketContext.Provider>
    </div>
  );
}

export default App;