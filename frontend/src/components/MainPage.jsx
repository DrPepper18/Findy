import React, { useEffect, useState } from 'react';
import YandexMap from './YandexMap.jsx';
import EventsList from "./EventsList.jsx";
import {Header} from "./Header.jsx";
import config from '../config';

const MainScreen = () => {
    const [events, setEvents] = useState([]);
    useEffect(() => {
        if(!document.cookie) {
            window.location.href = '/login';
            return;
        }
        const getEvents = async () => {
            try {
                let response = await fetch(config.Host_url + 'events');
                if (!response.ok) {
                    throw new Error(`Request failed with status: ${response.status}`);
                }
                let data = await response.json();
                setEvents(data.events || []);
            } catch (error) {
                console.error('Error fetching events:', error);
                return [];
            }
        };
        getEvents();
    }, []);
    return (
        <div className="App">
            <Header/>
            <main>
                <div className='mainPage'>
                    <EventsList events={events}/>
                    <YandexMap events={events}/>
                </div>
            </main>
        </div>
    );
}
export default MainScreen