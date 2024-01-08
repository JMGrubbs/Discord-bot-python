import React from 'react';

function Message({ sender, text }) {
    // Determine the additional class based on the sender
    const senderClass = sender === 'agent' ? 'agent' : 'user';

    // Apply both `message` and the sender-specific class
    return (
        <div className={`message-list-message ${senderClass}`}>
            <div className={`message-list-message sender ${senderClass}`}>{sender}</div>
            <div className={`message-list-message text ${senderClass} holder`}>
                {text}
            </div>
        </div>
    );
}

export default Message;
