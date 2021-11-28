import React, { useState, useMemo, useEffect } from 'react';
import { Player } from './player';
import * as Tone from 'tone'

import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Slider from '@mui/material/Slider';
import VolumeDown from '@mui/icons-material/VolumeDown';
import VolumeUp from '@mui/icons-material/VolumeUp';

type InstrumentProps = {
    type: string,
    name: string,
    source: Tone.PolySynth | Tone.Sampler | Tone.MonoSynth,
}

export const Instrument = ({ type, name, source }: InstrumentProps) => {
    const vol = useMemo(() => new Tone.Volume(0), [])
    const [value, setValue] = useState(100);

    function handleChange(event: Event, value: number | Array<number>) {
        value = Number(value)
        if (value === 0) {
            vol.mute = true
        }
        else {
            vol.volume.value = 10 * Math.log10(Number(value) / 100)
            setValue(value) // convert % to dB
            vol.mute = false
        }
    };

    return (
        <Box maxWidth="300px" width="30vw" height="30vh"
            padding="20px" border="3px solid darkgrey" borderRadius="20px">
            <h1>{name}</h1>
            <Stack spacing={2} direction="row" sx={{ mb: 1 }} alignItems="center">
                <VolumeDown />
                <Slider aria-label="Volume" value={value}
                    onChange={handleChange} onChangeCommitted={() => { }} />
                <VolumeUp />
            </Stack>
            <Player path={`midi-${type}-${name}`} source={source} volume={vol} />
        </Box>);
};