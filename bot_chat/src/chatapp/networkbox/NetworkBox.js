import React from 'react';
import NetworkMessage from './NetworkBox.js';

function NetworkApp({ events }) {

    return (
        <div className={`network event list`}>
            <div className={`network event list proxy`}>
                {events.map((event, index) => (
                    <NetworkMessage key={index} text={event} />
                ))}
            </div>
        </div >
    );
}

export default NetworkApp;