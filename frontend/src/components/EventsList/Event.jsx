import React, { useState, useRef } from "react";
import './EventList.css'


export const Event = ({ event }) => {
    const [joined, setJoined] = useState(false);

    const handleJoin = () => {
        event.join(setJoined);
    };

    return (
        <div className="event-list__card" ref={useRef('event-list')}>
            <div>
                <h2>{event.name}</h2>
                <h4>
                    {new Date(event.datetime).toLocaleDateString('ru-RU')} {event.min_age} - {event.max_age} лет
                </h4>
            </div>
            <div>
                {joined ? (<span>Вы добавлены</span>) : (
                    <input type="button" value="Я приду" className="button button--to-go" onClick={handleJoin}></input>
                )}
                <h5>до {event.capacity} человек</h5>
            </div>
        </div>
    )
}

export default Event;
