import React, { useState, useContext, useEffect } from 'react';
import { SocketContext } from '../context/socket';

import Box from '@mui/material/Box';
import { Grid } from '@mui/material';

import * as Tone from 'tone'

export const Chords = () => {
    const [data, setData] = useState<string[]>(["0", "1"]);
    const [chords, setChords] = useState<string[]>(["Current Chord", "Next Chord"]);

    const socket = useContext(SocketContext);
    useEffect(() => { socket.on("chords", (data: string[]) => { setData(data) }) }, []);
    useEffect(() => { Tone.Transport.scheduleOnce((time) => { setChords(data); }, "0:3:3") }, [data])

    return (
        <Grid
            container
            spacing={0}
            direction="column"
            alignItems="center"
            justifyContent="center"
            style={{ minHeight: '10vh' }}
        >
            <Grid item xs={3}>
                <h1>{chords[0]}</h1>
            </Grid>

            <Grid item xs={3}>
                <h3>{chords[1]}</h3>
            </Grid>
        </Grid>
    );
};