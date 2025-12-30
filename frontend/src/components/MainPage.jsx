import { useEffect, useState } from 'react';
import Map from './Map.jsx';
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
                console.log(data.events);
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
                    <Map events={events}/>
                </div>
            </main>
        </div>
    );
}
export default MainScreen