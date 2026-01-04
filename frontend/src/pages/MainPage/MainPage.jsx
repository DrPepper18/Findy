import React, { useEffect, useState } from 'react';
import Map from '../../components/Map/Map.jsx';
import EventsList from "../../components/EventsList/EventsList.jsx";
import { Header } from "../../components/Header/Header.jsx";
import { getEvents } from '../../api.js'
import './MainPage.css'

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
                <div className='main-page'>
                    <EventsList events={events}/>
                    <Map events={events}/>
                </div>
            </main>
        </div>
    );
}
export default MainScreen;