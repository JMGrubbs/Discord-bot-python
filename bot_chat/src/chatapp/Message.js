import React from 'react';

function Message({ sender, text }) {
    // Determine the additional class based on the sender
    const senderClass = sender === 'agent' ? 'agent' : 'user';

    // Apply both `message` and the sender-specific class
    return (
        <div className={`message sender ${senderClass}`}>
            {text}
        </div>
    );
}

export default Message;
