import React, { useEffect, useRef } from 'react';
import NewEventForm from './NewEvent';
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
                    let name = document.getElementById("name_input");
                    let date = document.getElementById("date_input");
                    let time = document.getElementById("time_input");
                    let capacity = document.getElementById("capacity_input");
                    let minage = document.getElementById("minage_input");
                    let maxage = document.getElementById("maxage_input");
                    if (!(name.value && date.value && time.value)) {
                        alert("Введите все данные");
                    } else {
                        let parent = document.getElementById("NewEventForm");
                        parent.innerHTML = '<h3>Событие создано!</h3>';

                        map.geoObjects.add(
                            new window.ymaps.Placemark(
                            lastCoord, 
                            {
                                balloonContentHeader: name.value,
                                balloonContentBody: `
                                    <p>${new Date(date.value).toLocaleDateString('ru-RU')}</p>
                                    <input type="button" class="ToGoButton" value="Я приду!"></input>
                                `,
                                balloonContentFooter: `${minage.value}-${maxage.value} лет, до ${capacity.value} человек`,
                                hintContent: name.value, 
                            })
                        )

                        await fetch(config.Host_url + 'events', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                "name": name.value, 
                                "lat": lastCoord[0], "lon": lastCoord[1],
                                "date": date.value,
                                "capacity": capacity.value,
                                "minage": minage.value, "maxage": maxage.value
                            })
                        });
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
                        [event.Latitude, event.Longitude], 
                        {
                            balloonContentHeader: event.Name,
                            balloonContentBody: `
                                <p>${new Date(event.DateTime).toLocaleDateString('ru-RU')}</p>
                                <input type="button" class="ToGoButton" value="Я приду!"></input>
                            `,
                            balloonContentFooter: `${event.MinAge}-${event.MaxAge} лет, до ${event.MaxMembers} человек`,
                            hintContent: event.Name, 
                        })
                    )
                    if (params.has('id') && params.get('id') == event.ID) {
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
                            } catch {
                                console.log("Failed to find the button");
                            };
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
