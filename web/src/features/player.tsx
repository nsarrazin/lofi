import React, {useState, useContext, useEffect } from 'react'; 

import {SocketContext} from '../context/socket';
import * as Tone from 'tone'
import { Midi } from '@tonejs/midi'

type PlayerProps = {
    type:string,
    name: string,
    source: Tone.PolySynth | Tone.Sampler,
    vol_init: number
}

export const Player = ({type, name, source, vol_init}: PlayerProps) => {
    const [playing, setPlaying] = useState(true);
    const [volume, setVolume] = useState(new Tone.Volume(vol_init))
    const [eventID, setEventID] = useState([0]);
    const [array, setArray] = useState<Int8Array>();

    
    function handleMessage(){ 
        if (array === undefined){
            return;
        }
        const midi = new Midi(array)
        const notes = midi.tracks[0].notes
        
        eventID.forEach(id => {Tone.Transport.clear(id)}); // clear previous scheduling
        
        setEventID([0]) //empty array

        notes.forEach(note => {
            let id = Tone.Transport.schedule((time) => {
                source.triggerAttackRelease(note.name, note.duration,time)
            }, note.time)
            eventID.push(id)
        })
        setEventID(eventID); 
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
    
    useEffect(() => {socket.on(`midi-${type}-${name}`, (data:Int8Array) => {setArray(data)})}, []);
    useEffect(() => {Tone.Transport.scheduleOnce((time) => {handleMessage();}, "0:3:3")}, [array])
    useEffect(() => {source.chain(volume, Tone.Destination)}, [])

    return (<div>
                <p> {name} playing something !</p>
                <button onClick={toggle_play}>playing : {String(playing)} </button>
            </div>);
};
