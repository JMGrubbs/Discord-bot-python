import React from 'react';

function NetworkMessage({ event }) {
    return (
        <div className={`network message`}>
            <div className={`network message agent`}>Agent: {event["agent"]}</div>
            <div className={`network message task`}>Task: {event["task"]}:</div>
            <div className={`network message message`}>Message: "{event["message"]}"</div>
        </div>
    );
}

export default NetworkMessage;

