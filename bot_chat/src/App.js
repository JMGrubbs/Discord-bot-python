import React from 'react';
import './css/App.css';
import './css/Sidebar.css';
import './css/ChatApp.css';
import ChatApp from './chatapp/ChatApp';
import Sidebar from './sidebar/Sidebar';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Simple Autogen Clone</h1>
      </header>
      <main className='app-holder'>
        <Sidebar />
        <ChatApp />
      </main>
    </div>
  );
}

export default App;
