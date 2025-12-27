import React, { useEffect, useState } from 'react';
import YandexMap from './YandexMap.jsx';
import EventsList from "./EventsList.jsx";
import {Header} from "./Header.jsx";
import {getEvents} from '../api'

const MainScreen = () => {
    const [events, setEvents] = useState([]);
    useEffect(() => {
        if(!localStorage.getItem('jwt')) {
            window.location.href = '/login';
            return;
        }
        const fetchEvents = async () => {
            try {
                let data = await getEvents();
                setEvents(data.events || []);
            } catch (error) {
                console.error('Error fetching events:', error);
                return [];
            }
        };
        fetchEvents();
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