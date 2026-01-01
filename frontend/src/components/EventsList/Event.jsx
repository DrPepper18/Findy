import { useState, useRef } from "react";
import './EventList.css'


export const Event = ({ event }) => {
    const [joined, setJoined] = useState(false);

    const handleJoin = () => {
        event.join(setJoined);
    };

    return (
        <div className="Event" ref={useRef('CurrentEvents')}>
            <div>
                <h2>{event.Name}</h2>
                <h4>
                    {new Date(event.DateTime).toLocaleDateString('ru-RU')} {event.MinAge} - {event.MaxAge} лет
                </h4>
            </div>
            <div>
                {joined ? (<span>Вы добавлены</span>) : (
                    <input type="button" value="Я приду" className="ToGoButton" onClick={handleJoin}></input>
                )}
                <h5>до {event.Capacity} человек</h5>
            </div>
        </div>
    )
}

export default Event;
