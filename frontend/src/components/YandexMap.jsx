import React, { useEffect } from 'react';
// import ReactDOM from 'react-dom/client'; // Import ReactDOM for rendering
import NewEventForm from './NewEvent';
import config from '../config';

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
        const get_API_KEY = async () => {
            let response = await fetch(config.Host_url + 'yandexmap');
            return response.api_key;
        }
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
                                balloonContentFooter: `${0}-${9999} лет, до ${capacity.value} человек`,
                                hintContent: name.value, 
                            })
                        )

                        const response = await fetch(config.Host_url + 'events', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                "name": name.value, 
                                "lat": lastCoord[0], 
                                "lon": lastCoord[1],
                                "date": date.value,
                                "capacity": capacity.value,
                                "minage": 0, 
                                "maxage": 9999
                            })
                        });
                    }
                };
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
                        balloonContentBody: NewEventForm,
                        hintContent: "Нажмите, чтобы создать событие"
                    }, {preset: 'islands#redIcon'});

                    lastCoord = coord;
                    map.geoObjects.add(lastPlacemark);
                    map.events.add("balloonopen", function (e) {
                        setTimeout(() => {
                            try{
                                const datePicker = document.getElementById('date_input');
                                const today = new Date().toISOString().split('T')[0]; // Получаем текущую дату в формате YYYY-MM-DD
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
