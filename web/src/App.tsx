import React from 'react';
import { Instrument } from './components/instrument';
import './App.css';

import { SocketContext, socket } from './context/socket';
import * as Tone from 'tone'
import Grid from '@mui/material/Grid';
import AlertDialog from './components/alert';
import { Chords } from './components/chords';
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

const drums = new Tone.Sampler({
  urls: {
    C4: "kick/RT_Kick_Rosen.wav",
    D4: "snare/RT_Snare_Crunch.wav",
    E4: "hihats/RT_High_Hat_Lofi_.wav",
    F4: "percussion/RT_Percussion_Foley_Wood_Knock.wav"
  },
  release: 1,
  baseUrl: "audio/drums/",
});


const bass = new Tone.Sampler({
  urls:{C2: "RT_One_Shot_Bass_Synth_Upright_C.wav"},
  baseUrl: "audio/oneshots/"
});

const pad = new Tone.Sampler({
  urls:{C4: "RT_One_Shot_Classic_Rosen_Lead_C.wav"},
  baseUrl: "audio/oneshots/"
})

Tone.Transport.bpm.value = 80;
Tone.Transport.loop = true;
Tone.Transport.loopEnd = "1m";

function App() {
  return (
    <div className="App">
      <AlertDialog/>
      <SocketContext.Provider value={socket}>
      <Grid container direction={'row'} justifyContent="space-around" marginTop="10vh">
        <Instrument source={piano} name='piano' type='chords' />
        <Instrument source={bass} name='doublebass' type='bass' />
        <Instrument source={drums} name='lofikit' type='drums' />
        <Instrument source={pad} name='synthpad' type='pads' />

      </Grid>
      <Chords/>
      </SocketContext.Provider>
    </div>
  );
}

// add meta info in flask with bpm and such
// add meta info to socket next to bytefile with length of midi file 
// add extra meta component with master volume, effect tracks, etc.
export default App;