import React, { useState } from 'react';
import { Popup } from 'react-leaflet';
import { createEvent } from '../../api';
import './NewEvent.css'



const NewEventCard = ({position}) => {

    const [inputs, setInputs] = useState({
        name: "",
        dateTime: "",
        capacity: 5,
        minAge: "",
        maxAge: ""
    });

    const handleCreate = async () => {       
        const finalData = {
            name: inputs.name,
            datetime: inputs.dateTime,
            latitude: parseFloat(position[0]),
            longitude: parseFloat(position[1]),
            capacity: parseInt(inputs.capacity),
            min_age: inputs.minAge ? parseInt(inputs.minAge) : null,
            max_age: inputs.maxAge ? parseInt(inputs.maxAge) : null
        };

        if (!(finalData.name && finalData.datetime && finalData.capacity)) {
            console.log(finalData);
            alert("Введите все данные");
        } else {
            console.log("Отправка данных:", finalData);
            await createEvent(finalData);
            alert("Событие создано!");
        }
    };

    function handleChange(e) {
        const name = e.target.name;
        const value = e.target.value;
        setInputs(values => ({...values, [name]: value}));
    }

    return (
        <Popup>
            <form id="NewEventForm" style={{width: '250px'}}>
                <input className="event-card__input" name="name" placeholder="Название" value={inputs.name} onChange={handleChange}/>
                <input className="event-card__input" name="dateTime" type="datetime-local" value={inputs.dateTime} onChange={handleChange}/>
                <div id="capacityDiv">
                    <input className="event-card__input" name="capacity" type="number"
                        min="1" max="16" value={inputs.capacity} onChange={handleChange}
                    />
                    <h3>человек</h3>
                </div>
                <div id="ageDiv">
                    <h3>от</h3>
                    <input className="event-card__input" name="minAge" type="number" 
                        min="0" max="100" value={inputs.minAge} onChange={handleChange}
                    />
                    <h3>до</h3>
                    <input className="event-card__input" name="maxAge" type="number" 
                        min="0" max="100" value={inputs.maxAge} onChange={handleChange}
                    />
                    <h3>лет</h3>
                </div>
                <input id="newEventButton" type="button" className="button button--to-go"
                    value="Начать созыв!" onClick={handleCreate}
                />
            </form>
        </Popup>
    );
}


export { NewEventCard };