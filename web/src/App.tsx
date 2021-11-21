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

Tone.Transport.bpm.value = 50;
Tone.Transport.loop = true;
Tone.Transport.loopEnd = "2n";
Tone.Transport.start();

function App() {
  return (
    <div className="App">
      <SocketContext.Provider value={socket}>
        Hello World from React!
      <Player instrument={piano} name='piano' vol_init={-12}/>
      <Player instrument={synth} name='bass' vol_init={0}/>
      </SocketContext.Provider>
    </div>
  );
}

export default App;