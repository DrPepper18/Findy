import React from 'react';
import { Event } from "./Event";
import './EventList.css'


const EventsList = ({events}) => {
    return (
        <div id="CurrentEvents">
            {events.length > 0 ? 
                events.map((event, index) => (
                    <Event key={index} event={event}/>
                )) :
                <h2 style={{textAlign: 'center'}}>
                    Здесь ничего нет.<br></br>Будь первым!
                </h2>
            }
        </div>
    );
};

export default EventsList;