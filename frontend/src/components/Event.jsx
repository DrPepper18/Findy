import React, { useState, useRef } from "react";

export const Event = ({ event }) => {
    const [joined, setJoined] = useState(false);

    const handleJoin = () => {
        event.join(setJoined);
    };

    return (
        <div className="Event" ref={useRef('CurrentEvents')}>
            <div>
                <h2 style={{marginTop: '5px'}}>{event.Name}</h2>
                <h4 style={{ marginTop: '-10px' }}>
                    {new Date(event.DateTime).toLocaleDateString('ru-RU')} {event.MinAge} - {event.MaxAge} лет
                </h4>
            </div>
            <div>
                {joined ? (<span>Вы добавлены</span>) : (
                    <input type="button" value="Я приду" className="ToGoButton" onClick={handleJoin}></input>
                )}
                <h5 style={{marginTop: 0, marginLeft: '4%'}}>до {event.MaxMembers} человек</h5>
            </div>
        </div>
    )
}

const components = { Event };

export default components;
