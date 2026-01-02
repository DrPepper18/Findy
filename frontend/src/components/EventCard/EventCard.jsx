import React, { useState, useEffect } from 'react';
import { Popup } from 'react-leaflet';
import { EventJoinRequest, EventJoinCheck } from '../../api';
import './EventCard.css'


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
    let ageLabel = "";
    if (event.MinAge && event.MaxAge) {
        ageLabel = `${event.MinAge}–${event.MaxAge} лет`;
    } else if (event.MinAge) {
        ageLabel = `от ${event.MinAge} лет`;
    } else if (event.MaxAge) {
        ageLabel = `до ${event.MaxAge} лет`;
    }
    const shareUrl = `${window.location.origin}/?id=${event.ID}`;

    return (
        <Popup>
            <h3>{event.Name}</h3>
            <p>📅 {new Date(event.DateTime).toLocaleString('ru-RU', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })}</p>
            <p>👤 {ageLabel}{ageLabel && '. '}До {event.Capacity} человек</p>
            <input type="button" id="ToGoID" className="ToGoButton" value="Я приду!" disabled={isJoined} onClick={handleJoin}></input>
            <div>
                <small>🔗 </small>
                <a 
                    href={shareUrl} 
                    style={{ fontSize: '11px', textDecoration: 'none', color: '#007bff' }}
                    onClick={(e) => {
                        e.preventDefault();
                        navigator.clipboard.writeText(shareUrl);
                        alert("Скопировано!");
                    }}
                >
                    {shareUrl.replace('http://', '').replace('https://', '')}
                </a>
            </div>
        </Popup>
    );
}


export {EventCard};