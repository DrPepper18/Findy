import React, { useEffect, useRef } from 'react';
import {NewEventCard, NewEventAdd} from './NewEvent';
import {EventCard, EventJoin} from './EventCard';
import {config, getCookie} from '../config';
import '../styles/NewEvent.css'


const get_API_KEY = async () => {
    let response = await fetch(config.Host_url + 'yandexmap');
    let data = await response.json();
    return data.api_key || "";
}
  

const YandexMap = ({events}) => {

    const eventsRef = useRef(events);
    useEffect(() => {
        eventsRef.current = events;
    }, [events]);
    
    useEffect(() => {
        const loadScript = (url) => {
            return new Promise((resolve, reject) => {
                const script = document.createElement('script');
                script.src = url;
                script.async = true;
                script.onload = () => resolve();
                script.onerror = () => reject(new Error(`Failed to load script ${url}`));
                document.body.appendChild(script);
            });
        };
        
        const initMap = async () => {
            const API_KEY = await get_API_KEY();
            await loadScript(`https://api-maps.yandex.ru/2.1/?apikey=${API_KEY}&lang=ru_RU`);
            window.ymaps.ready(async () => {
                const map = new window.ymaps.Map('map', {
                    center: [55.7558, 37.6176],
                    zoom: 10
                });
                
                var dots = [];
                let events = eventsRef.current;

                const url = new URL(window.location.href);
                const params = url.searchParams;
                let targetPlacemark = null;
                events.forEach(event => {
                    dots.push(
                        new window.ymaps.Placemark(
                        [event.Latitude, event.Longitude], EventCard(event)
                        )
                    )
                    if (params.has('id') && Number(params.get('id')) === event.ID) {
                        targetPlacemark = dots[dots.length-1];
                    }
                })
                dots.forEach(dot => {
                    map.geoObjects.add(dot);
                })
                if (targetPlacemark) {
                    targetPlacemark.balloon.open();
                    map.setCenter(targetPlacemark.geometry.getCoordinates(), 10);
                }

                let lastCoord = map.getCenter();
                let balloonOpenHandler = null;
                let lastPlacemark = NewEventCard(lastCoord);
                map.geoObjects.add(lastPlacemark);

                map.events.add('actionend', function (e) {
                    lastCoord = e.originalEvent.map.getCenter();
                    if (balloonOpenHandler) {
                        map.events.remove('balloonopen', balloonOpenHandler);
                    }
                    if (lastPlacemark) {
                        map.geoObjects.remove(lastPlacemark);
                    }
                    lastPlacemark = NewEventCard(lastCoord);
                    map.geoObjects.add(lastPlacemark);
                    balloonOpenHandler = async function (e) {
                        setTimeout(async () => {
                            try {
                                const datePicker = document.getElementById('date_input');
                                const today = new Date().toISOString().split('T')[0];
                                datePicker.setAttribute('min', today);
                                document.getElementById("newEventButton").addEventListener("click", async () => {
                                    let event = {
                                        Name: document.getElementById("name_input").value,
                                        Latitude: lastCoord[0],
                                        Longitude: lastCoord[1],
                                        DateTime: document.getElementById("date_input").value,
                                        MinAge: document.getElementById("minage_input").value,
                                        MaxAge: document.getElementById("maxage_input").value,
                                        Capacity: document.getElementById("capacity_input").value
                                    };
                                    NewEventAdd(event);
                                });
                            } catch {};
                            
                            try {
                                const eventID = e.get('target').properties._data.eventID;
                                let token = await getCookie('jwt');
                                const response = await fetch(config.Host_url + 'event/joincheck', {
                                    method: 'POST',
                                    headers: {
                                        'Authorization': `Bearer ${token}`,
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({"EventID": eventID})
                                })
                                let data = await response.json();
                                if (data.joined)
                                    document.getElementById("ToGoID").disabled = true;
                                document.getElementById("ToGoID").addEventListener("click", 
                                    async () => {EventJoin(eventID)});
                            } catch {};
                        }, 0);
                    }
                    map.events.add("balloonopen", balloonOpenHandler)
                });
            });
        };
        initMap();
    }, []);
    return (
        <div id="map"></div>
    );
};
export default YandexMap;
