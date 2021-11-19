import socketio from "socket.io-client";
import React from 'react';

let SOCKET_URL = "ws://127.0.0.1:5000/"

export const socket = socketio(SOCKET_URL);
export const SocketContext = React.createContext(socket);