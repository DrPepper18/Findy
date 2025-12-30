import { useState, useEffect } from 'react';
import { Popup } from 'react-leaflet';
import { EventJoinRequest, EventJoinCheck } from '../api';


const EventCard = ({event}) => {
    const [isJoined, setIsJoined] = useState(false);

    useEffect(() => {
        const checkStatus = async () => {
            try {
                const joined = await EventJoinCheck(event.ID);
                setIsJoined(joined);
            } catch (err) {
                console.error("Ошибка проверки статуса:", err);
            }
        };

        checkStatus();
    }, [event.ID]);

    const handleJoin = async () => {
        try {
            await EventJoinRequest(event.ID);
            setIsJoined(true);
            alert("Вы записаны!");
        } catch (error) {
            console.error("Ошибка при записи:", error);
            alert("Не удалось записаться");
        }
    };
    return (
        <Popup>
            <h3>{event.Name}</h3>
            <p>{event.DateTime}</p>
            <p>{event.MinAge}-{event.MaxAge}. До {event.Capacity} человек</p>
            <input type="button" id="ToGoID" className="ToGoButton" value="Я приду!" disabled={isJoined} onClick={handleJoin}></input>
        </Popup>
    );
}


export {EventCard};