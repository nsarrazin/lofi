import React, {useState, useContext, useEffect, useCallback } from 'react'; 

import {SocketContext} from '../context/socket';
import * as Tone from 'tone'
import { Midi } from '@tonejs/midi'

type PlayerProps = {
    name: string,
    instrument: Tone.PolySynth | Tone.Sampler,
    vol_init: number
}

export const Player = ({name, instrument, vol_init}: PlayerProps) => {
    const [playing, setPlaying] = useState(true);
    const [volume, setVolume] = useState(new Tone.Volume(vol_init))

    useEffect(() => {instrument.chain(volume, Tone.Destination)}, [])

    function handleMessage(data: Int8Array){ 
            const midi = new Midi(data)
            const notes = midi.tracks[0].notes

            notes.forEach(note => {
                instrument.triggerAttackRelease(note.name, note.duration, Tone.now() + note.time)
              })
            
            // do something with notes, add a transport scheduler
            // todo : add length of midi message in beats to the data of socketio send
        }

    // function playChord(data: Int8Array){
    //     Tone.loaded().then(() => { instrument.triggerAttackRelease(data, 2)});
    // }
    
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
    
    useEffect(() => {socket.on(`midi-${name}`, (data:Int8Array) => handleMessage(data))}, []);
    
    return (<div>
                <p> {name} playing something !</p>
                <button onClick={toggle_play}>playing : {String(playing)} </button>
            </div>);
};
