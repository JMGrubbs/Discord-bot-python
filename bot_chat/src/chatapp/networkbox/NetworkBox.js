import React, { useState } from 'react';

function NetworkApp() {
    const [events, setEvents] = useState(["Network App", "Network"]);

    return (
        <div className={`network event list`}>
            <div className={`network event list proxy`}>
                {events.map((event, index) => (
                    <div key={index} className='event'>
                        <div className='event-text'>
                            {event}
                        </div>
                    </div>
                ))}
            </div>
        </div >
    );
}

export default NetworkApp;