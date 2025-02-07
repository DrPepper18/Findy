import { useState, useEffect } from "react";
import {EventObj, Event} from "./Event";
import config from '../config';
const EventsList = () => {
    const [events, setEvents] = useState([]); // State to hold events

    function NewEventFromJson(json) {
        return new EventObj(
            json['name'],
            json['author_id'],
            json['start_longitude'],
            json['start_latitude'],
            json['end_longitude'],
            json['end_latitude'],
            Date.parse(json['date']),
            json['capacity'],
            json['members_count'],
            json['tags']
        )
    }

    const getEvents = async () => {
        try {
            let response = await fetch(config.Host_url + 'events');
            if (!response.ok) {
                throw new Error(`Request failed with status: ${response.status}`);
            }
            let data = await response.json();
            return data.events || [];
        } catch (error) {
            console.error('Error fetching events:', error);
            return [];
        }
    }
   // Fetch events on component mount
   useEffect(() => {
    const fetchEvents = async () => {
        const eventsData = await getEvents();
        setEvents(eventsData); // Set state after fetching
    };
    fetchEvents();
}, []); // Empty dependency array means it runs only once on mount
    console.log(events);
    return (
        <div id="CurrentEvents" style={{}}>
            {events.length > 0 ? 
                events.map((event, index) => (
                    <Event key={index} event={event}/>
                )) :
                <h2 style={{textAlign: 'center'}}>
                    Здесь ничего нет, будь первым
                </h2>
            }
        </div>
    );
};

export default EventsList;