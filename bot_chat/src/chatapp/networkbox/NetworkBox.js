import React from 'react';
import NetworkMessage from './NetworkMessage.js';

function NetworkApp({ networkobject }) {
    return (
        <div className={`network event list`}>
            <div className={`network event list proxy`}>
                {networkobject.map((event, index) => (
                    <NetworkMessage key={index} event={event} />
                ))}
            </div>
        </div>
    );
}

export default NetworkApp;