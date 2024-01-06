import React from 'react';
import './css/App.css';
import './css/Sidebar.css';
import './css/ChatApp.css';
import './css/NetworkBox.css';
import ChatApp from './chatapp/ChatApp';
import Sidebar from './sidebar/Sidebar';
import NetworkApp from './networkapp/NetworkApp';

function App() {
  return (
    <div className="App">
      <main className='app-holder'>
        <Sidebar />
        <ChatApp />
        <NetworkApp />
      </main>
    </div>
  );
}

export default App;
