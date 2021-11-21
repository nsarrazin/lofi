import React, {useState, useContext, useEffect, useCallback } from 'react'; 

import {SocketContext} from '../context/socket';
import * as Tone from 'tone'

type PlayerProps = {
    name: string,
    instrument: Tone.PolySynth | Tone.Sampler,
}

export const Player = ({name, instrument}: PlayerProps) => {
    const [chord, setChord] = useState(["Bb3"]);
    const [playing, setPlaying] = useState(true);
    const [volume, setVolume] = useState(new Tone.Volume(0))

    useEffect(() => {instrument.chain(volume, Tone.Destination)}, [])

    function handleMessage(data: string[], playing:boolean){ 
            setChord(data);
            playChord(data)
        }

    function playChord(data: string[]){
        Tone.loaded().then(() => { instrument.triggerAttackRelease(data, 2)});
    }
    
    function toggle_play(){
        if(playing){
            setPlaying(false);
            volume.mute = true;
        }
        else{
            setPlaying(true);
            volume.mute = false;
        }
    }
    
    const socket = useContext(SocketContext);    
    
    useEffect(() => {socket.on(`midi-${name}`, (data:string[]) => handleMessage(data, playing))}, []);
    
    return (<div>
                <p> {name} playing {chord}</p>
                <button onClick={toggle_play}>playing : {String(playing)} </button>
            </div>);
};
