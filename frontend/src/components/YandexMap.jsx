import React, { useEffect, useRef } from 'react';
import NewEventForm from './NewEvent';
import EventCard from './EventCard';
import config from '../config';
import '../styles/NewEvent.css'


const get_API_KEY = async () => {
    let response = await fetch(config.Host_url + 'yandexmap');
    let data = await response.json();
    return data.api_key || "";
}

let lastCoord = null;
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
                const NewEventAdd = async () => {
                    let event = {
                        Name: document.getElementById("name_input").value,
                        Latitude: lastCoord[0],
                        Longitude: lastCoord[1],
                        DateTime: document.getElementById("date_input").value,
                        MinAge: document.getElementById("minage_input").value,
                        MaxAge: document.getElementById("maxage_input").value,
                        Capacity: document.getElementById("capacity_input").value
                    };
                    if (!(event.Name && event.DateTime)) {
                        alert("Введите все данные");
                    } else {
                        let parent = document.getElementById("NewEventForm");
                        parent.innerHTML = '<h3>Событие создано!</h3>';

                        await fetch(config.Host_url + 'events', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(event)
                        });

                        map.geoObjects.add(
                            new window.ymaps.Placemark(lastCoord, EventCard(event))
                        )
                    }
                };
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

                let lastPlacemark = null;
                map.events.add('actionend', function (e) {
                    let coord = e.originalEvent.map.getCenter();
                    if (lastPlacemark) {
                        map.geoObjects.remove(lastPlacemark);
                    }
                    lastPlacemark = new window.ymaps.Placemark(coord, {
                        balloonContentHeader: "<h2>Новое событие</h2>",
                        balloonContentBody: NewEventForm,
                        hintContent: "Нажмите, чтобы создать событие"
                    }, {preset: 'islands#redIcon'});

                    lastCoord = coord;
                    map.geoObjects.add(lastPlacemark);
                    map.events.add("balloonopen", function (e) {
                        setTimeout(() => {
                            try{
                                const datePicker = document.getElementById('date_input');
                                const today = new Date().toISOString().split('T')[0];
                                datePicker.setAttribute('min', today);
                                document.getElementById("newEventButton").addEventListener("click", NewEventAdd);
                            } catch {};
                        }, 0);
                    }) 
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
