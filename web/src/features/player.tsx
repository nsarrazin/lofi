import React, {useState, useContext, useRef } from 'react'; 

import {SocketContext} from '../context/socket';
import * as Tone from 'tone'

type PlayerProps = {
    name?: string
}

const sampler = new Tone.Sampler({
	urls: {
		"C4": "C4.mp3",
		"D#4": "Ds4.mp3",
		"F#4": "Fs4.mp3",
		"A4": "A4.mp3",
	},
	release: 1,
	baseUrl: "https://tonejs.github.io/audio/salamander/",
}).toDestination();

const poly = new Tone.PolySynth(Tone.Synth).toDestination();

export const Player = (name: PlayerProps) => {
    const [chord, setChord] = useState(["C3","E3","G3"]);

    const socket = useContext(SocketContext);    
    
    socket.on('message', (data:string[]) => {setChord(data)});
        
    const handleClick = () => sampler.triggerAttackRelease(chord,0.1);
    const now = Tone.now()

    Tone.loaded().then(() => { sampler.triggerAttackRelease(chord, 1.5)});

    return (<div>
                <p>hello from player ${chord} </p>
                <button onClick={handleClick}>
                    start
                </button>
            </div>);
};

export const MemoizedPlayer = React.memo(Player);