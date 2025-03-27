import React, { useState, useRef } from 'react';
import config from "../config";

const NewEventForm = ()  => {
    const [name, setName] = useState("");
    const [date, setDate] = useState("");
    const [time, setTime] = useState("");
    const [capacity, setCapacity] = useState(5);

    const NewEventAdd = () => {
        let coords = [0, 0];
        console.log(name, date, time, coords, capacity);
    }
    return(
        <div style={{width: "250px"}}>
            <input 
                className="placemark_element" 
                id="name_input" 
                placeholder="Название"
                onChange={(e) => setName(e.target.value)}
            />
            <div style={{display: "flex"}}>
                <input 
                    className="placemark_element" 
                    id="date_input" 
                    style={{width: "55%"}} 
                    type="date"
                    onChange={(e) => setDate(e.target.value)}
                />
                <input 
                    className="placemark_element" 
                    id="time_input" 
                    type="time"
                    onChange={(e) => setTime(e.target.value)}
                />
            </div>
            <div style={{display: "flex"}}>
                <input
                    className="placemark_element" 
                    id="capacity_input"
                    type="number" 
                    min="1" max="16" value="5"
                    onChange={(e) => setCapacity(e.target.value)}
                />
                <h3>человек</h3>
            </div>
            <input type="button" className="ToGoButton" value="Начать созыв!" onClick={NewEventAdd}/>
        </div>
    );
}

export default NewEventForm;