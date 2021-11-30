import React, { useState, useContext, useEffect, SyntheticEvent } from 'react';

import { SocketContext } from '../context/socket';

import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Slider from '@mui/material/Slider';
import { Dictionary } from '@reduxjs/toolkit';

type SpicerProp = {
}

export const Spicer = ({ }: SpicerProp) => {
    const [value, setValue] = useState(1);
    const socket = useContext(SocketContext);

    function handleChange(event: Event | SyntheticEvent, value: number | Array<number>) {
        value = Number(value)
        setValue(value)
        socket.emit("spice", 2 - value)
    };

    useEffect(() => { socket.on("data", (data: Dictionary<any>) => {let x:number=2-data!.spice;setValue(x);})}, []);
    return (
        <Box maxWidth="500px" width="50vw" height="20vh"
            padding="10px" margin='auto'>
            <h3>🌶️ Spice Control 🌶️</h3>
            <Stack spacing={3} direction="row" sx={{ mb: 1 }} alignItems="center">
                <h2>🥱</h2>
                <Slider aria-label="Volume" min={0} max={1.99} step={0.1} value={value}
                    onChangeCommitted={handleChange} />
                <h2>🥵</h2>
            </Stack>
        </Box>);
};