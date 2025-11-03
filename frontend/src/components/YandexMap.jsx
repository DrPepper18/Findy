import React, { useEffect, useRef } from 'react';
import {NewEventCard, NewEventAdd} from './NewEvent';
import {EventCard, EventJoin, EventJoinCheck} from './EventCard';
import {getApiKey} from '../config';
import '../styles/NewEvent.css';


const DEFAULT_CENTER = [55.7558, 37.6176];
const DEFAULT_ZOOM = 10;


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

        const setPlacemarks = (map) => {
            var dots = [];
            const url = new URL(window.location.href);
            const params = url.searchParams;
            let targetPlacemark = null;
            eventsRef.current.forEach(event => {
                dots.push(
                    new window.ymaps.Placemark(
                    [event.Latitude, event.Longitude], EventCard(event))
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
        };
        
        const initMap = async () => {
            const API_KEY = await getApiKey();
            await loadScript(`https://api-maps.yandex.ru/2.1/?apikey=${API_KEY}&lang=ru_RU`);
            window.ymaps.ready(async () => {
                const map = new window.ymaps.Map('map', {
                    center: DEFAULT_CENTER, // Make it read your geoposition
                    zoom: DEFAULT_ZOOM
                });
                
                setPlacemarks(map);

                let lastCoord = map.getCenter();
                let lastPlacemark = NewEventCard(lastCoord);
                let newEventButtonHandler = null;
                map.geoObjects.add(lastPlacemark);
                
                map.events.add('actionend', function (e) {
                    lastCoord = e.originalEvent.map.getCenter();
                    if (lastPlacemark) {
                        map.geoObjects.remove(lastPlacemark);
                    }
                    lastPlacemark = NewEventCard(lastCoord);
                    map.geoObjects.add(lastPlacemark);
                });
                map.events.add("balloonopen", async function (e) {
                    requestAnimationFrame(async () => {
                        try {
                            const datePicker = document.getElementById("date_input");
                            const today = new Date().toISOString().split('T')[0];
                            datePicker.setAttribute('min', today);
                            if (newEventButtonHandler) {
                                document.getElementById("newEventButton")
                                    .removeEventListener("click", newEventButtonHandler);
                            }
                            newEventButtonHandler = async () => {
                                let date = document.getElementById("date_input").value;
                                let time = document.getElementById("time_input").value;
                                
                                let event = {
                                    Latitude: lastCoord[0],
                                    Longitude: lastCoord[1],
                                    Name: document.getElementById("name_input").value,
                                    DateTime: new Date(`${date}T${time}`).toISOString(),
                                    MinAge: document.getElementById("minage_input").value || null,
                                    MaxAge: document.getElementById("maxage_input").value || null,
                                    Capacity: document.getElementById("capacity_input").value
                                };
                                await NewEventAdd(event);
                            };
                            document.getElementById("newEventButton")
                                .addEventListener("click", newEventButtonHandler);
                            return;
                        } catch {};

                        try {
                            const eventID = e.get('target').properties._data.eventID;
                            document.getElementById("ToGoID").disabled = await EventJoinCheck(eventID);
                            document.getElementById("ToGoID").addEventListener("click", 
                                async () => {await EventJoin(eventID)});
                            return;
                        } catch {};
                    });
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
