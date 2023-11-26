import React from 'react';
import './App.css';
import './Sidebar.css';
import ChatApp from './ChatApp';
import Sidebar from './Sidebar';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Simple Autogen Clone ChatApp</h1>
      </header>
      <main className='app-holder'>
        <Sidebar />
        <ChatApp />
      </main>
    </div>
  );
}

export default App;
