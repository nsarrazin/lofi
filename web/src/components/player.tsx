import React, { useState, useContext, useEffect } from 'react';

import { SocketContext } from '../context/socket';
import * as Tone from 'tone'
import { Midi } from '@tonejs/midi'

type PlayerProps = {
    path: string,
    source: Tone.PolySynth | Tone.Sampler | Tone.MonoSynth,
    volume: Tone.Volume,
}

export const Player = ({ path, source, volume }: PlayerProps) => {
    const [eventID, setEventID] = useState([0]);
    const [array, setArray] = useState<Int8Array>();

    function handleMessage() {
        if (array === undefined) {
            return;
        }
        const midi = new Midi(array)
        const notes = midi.tracks[0].notes

        eventID.forEach(id => { Tone.Transport.clear(id) }); // clear previous scheduling

        setEventID([0]) //empty array

        notes.forEach(note => {
            let id = Tone.Transport.schedule((time) => {
                source.triggerAttackRelease(note.name, note.duration, time, note.velocity)
            }, note.time)
            eventID.push(id)
        })
        setEventID(eventID);
    }


    const socket = useContext(SocketContext);

    useEffect(() => { socket.on(path, (data: Int8Array) => { setArray(data) }) }, []);
    useEffect(() => { Tone.Transport.scheduleOnce((time) => { handleMessage(); }, "0:3:3") }, [array])
    useEffect(() => { source.chain(volume, Tone.Destination) }, [])

    return (null);
};
