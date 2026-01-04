import React, { useState, useEffect } from 'react';
import { Popup } from 'react-leaflet';
import { joinEvent, checkEventJoinStatus } from '../../api';
import './EventCard.css'


const EventCard = ({event}) => {
    const [isJoined, setIsJoined] = useState(false);

    useEffect(() => {
        const checkStatus = async () => {
            try {
                const joined = await checkEventJoinStatus(event.id);
                setIsJoined(joined);
            } catch (err) {
                console.error("Ошибка проверки статуса:", err);
            }
        };

        checkStatus();
    }, [event.id]);

    const handleJoin = async () => {
        try {
            await joinEvent(event.id);
            setIsJoined(true);
            alert("Вы записаны!");
        } catch (error) {
            console.error("Ошибка при записи:", error);
            alert("Не удалось записаться");
        }
    };
    let ageLabel = "";
    if (event.min_age && event.max_age) {
        ageLabel = `${event.min_age}-${event.max_age} лет`;
    } else if (event.min_age) {
        ageLabel = `от ${event.min_age} лет`;
    } else if (event.max_age) {
        ageLabel = `до ${event.max_age} лет`;
    }
    const shareUrl = `${window.location.origin}/?id=${event.id}`;

    return (
        <Popup>
            <h3>{event.name}</h3>
            <p>📅 {new Date(event.datetime).toLocaleString('ru-RU', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })}</p>
            <p>👤 {ageLabel}{ageLabel && '. '}До {event.capacity} человек</p>
            <input type="button" id="ToGoID" className="button button--to-go" value="Я приду!" disabled={isJoined} onClick={handleJoin}></input>
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