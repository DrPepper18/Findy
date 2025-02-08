import React, { useEffect } from 'react';
import config from '../config';
const API_KEY = '6997c194-93fd-44c8-89ce-8639d5bcd0c1';

const getEvents = async () => {
    try {
        let response = await fetch(config.Host_url + 'events');
        if (!response.ok) {
            throw new Error(`Request failed with status: ${response.status}`);
        }
        let data = await response.json();
        return data.events || []; // Ensure it's always an array
    } catch (error) {
        console.error('Error fetching events:', error);
        return [];
    }
};
let lastCoord = null;

const YandexMap = () => {
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
        await loadScript(`https://api-maps.yandex.ru/2.1/?apikey=${API_KEY}&lang=ru_RU`);
        window.ymaps.ready(async () => {
            const map = new window.ymaps.Map('map', {
                center: [55.7558, 37.6176],
                zoom: 10
            });
            var dots = [];
            let events = await getEvents();
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
            })
            dots.forEach(dot => {
                map.geoObjects.add(dot);
            })
            let lastPlacemark = null;
            map.events.add('actionend', function (e) {
                let coord = e.originalEvent.map.getCenter();
                if (lastPlacemark) {
                    map.geoObjects.remove(lastPlacemark);
                }
                // Create a new placemark at the new center
                lastPlacemark = new window.ymaps.Placemark(coord, {
                    balloonContentHeader: "<h2>Новое событие</h2>",
                    balloonContentBody: `
                    <div style="width: 250px">
                        <input class="placemark_element" id="name_input" placeholder="Название"></input>
                        <div style="display: flex">
                            <input class="placemark_element" id="date_input" style="width: 55%" id="date_input" type="date"></input>
                            <input class="placemark_element" id="time_input" type="time"></input>
                        </div>
                        <div style="display: flex">
                            <input
                                class="placemark_element" 
                                id="capacity_input"
                                type="number" 
                                min="1" max="16" value="5">
                            </input>
                            <h3>человек</h3>
                        </div>
                        <input type="button" class="ToGoButton" value="Начать созыв!" onClick=""></input>
                    </div>`,
                    hintContent: "Нажмите, чтобы создать событие"
                }, {preset: 'islands#redIcon'});
                lastCoord = coord;
                map.geoObjects.add(lastPlacemark);
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
