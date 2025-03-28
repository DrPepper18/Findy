import React, { useEffect, useState } from 'react';
// import {Profile, loggedUser} from './Profile.jsx';
import YandexMap from './YandexMap.jsx';
import EventsList from "./EventsList.jsx";
import {Header} from "./Header.jsx";
import config from '../config';

const MainScreen = () => {
    const [events, setEvents] = useState([]);
    useEffect(() => {
        const getEvents = async () => {
            try {
                let response = await fetch(config.Host_url + 'events');
                if (!response.ok) {
                    throw new Error(`Request failed with status: ${response.status}`);
                }
                let data = await response.json();
                setEvents(data.events || []); // Ensure it's always an array
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
                {document.cookie ? '' : window.location.href = '/login'}
                <div style={{display: 'flex', width: '100%'}}>
                    <EventsList events={events}/>
                    <YandexMap events={events}/>
                </div>
            </main>
        </div>
    );
}
export default MainScreen