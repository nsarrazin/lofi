import React from 'react';
import { MemoizedPlayer } from './features/player';
import './App.css';

import {SocketContext, socket} from './context/socket';

function App() {
  return (
    <div className="App">
      <SocketContext.Provider value={socket}>
        Hello World from React!
      <MemoizedPlayer/>
      </SocketContext.Provider>
    </div>
  );
}

export default App;