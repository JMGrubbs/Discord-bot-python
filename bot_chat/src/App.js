import React from 'react';
import './css/App.css';
import './css/Sidebar.css';
import './css/ChatApp.css';
import './css/NetworkBox.css';
import ChatApp from './chatapp/ChatApp';
import Sidebar from './sidebar/Sidebar';

import useCustomHook from './messageHooks.js';

function App() {
  const { messages, fetchMessageData, addMessage } = useCustomHook()
  return (
    <div className="App">
      <main className='app-holder'>
        <Sidebar messages={messages} fetchMessageData={fetchMessageData} />
        <ChatApp messages={messages} fetchMessageData={fetchMessageData} addMessage={addMessage} />
      </main>
    </div>
  );
}

export default App;
