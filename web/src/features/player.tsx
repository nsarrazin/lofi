import React, {useState, useContext, useEffect } from 'react'; 

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

    function handleMessage(data: string[]){
        setChord(data)
        playChord(data)
    }

    function playChord(data: string[]){
        Tone.loaded().then(() => { sampler.triggerAttackRelease(data, 1.1)});
    }

    const socket = useContext(SocketContext);    
    
    useEffect(() => {socket.on('message', (data:string[]) => {handleMessage(data)});}, []);
    

    return (<div>
                <p>hello from player ${chord}</p>
            </div>);
};

export const MemoizedPlayer = React.memo(Player);