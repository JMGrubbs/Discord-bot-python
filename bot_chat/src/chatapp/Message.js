import React from 'react';

function Message({ sender, text }) {
    // Determine the additional class based on the sender
    const senderClass = sender === 'agent' ? 'agent' : 'user';

    // Apply both `message` and the sender-specific class
    return (
        <div className={`message ${senderClass}`}>
            <div className="message-sender-name">{sender}</div>
            <div className={`message  ${senderClass} holder`}>
                <div className="message-text">{text}</div>
            </div>
        </div>
    );
}

export default Message;
