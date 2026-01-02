import React, { useState } from 'react';
import { Popup } from 'react-leaflet';
import { NewEventRequest } from '../../api';
import './NewEvent.css'



const NewEventCard = ({position}) => {

    const [inputs, setInputs] = useState({
        Name: "",
        DateTime: "",
        Capacity: 5,
        MinAge: "",
        MaxAge: ""
    });

    const handleCreate = async () => {       
        const finalData = {
            Name: inputs.Name,
            DateTime: inputs.DateTime,
            Latitude: parseFloat(position[0]),
            Longitude: parseFloat(position[1]),
            Capacity: parseInt(inputs.Capacity),
            MinAge: inputs.MinAge ? parseInt(inputs.MinAge) : null,
            MaxAge: inputs.MaxAge ? parseInt(inputs.MaxAge) : null
        };

        if (!(finalData.Name && finalData.DateTime && finalData.Capacity)) {
            console.log(finalData);
            alert("Введите все данные");
        } else {
            console.log("Отправка данных:", finalData);
            await NewEventRequest(finalData);
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
                <input className="placemark_element" name="Name" placeholder="Название" value={inputs.Name} onChange={handleChange}/>
                <input className="placemark_element" name="DateTime" type="datetime-local" value={inputs.DateTime} onChange={handleChange}/>
                <div id="capacityDiv">
                    <input className="placemark_element" name="Capacity" type="number"
                        min="1" max="16" value={inputs.Capacity} onChange={handleChange}
                    />
                    <h3>человек</h3>
                </div>
                <div id="ageDiv">
                    <h3>от</h3>
                    <input className="placemark_element" name="MinAge" type="number" 
                        min="0" max="100" value={inputs.MinAge} onChange={handleChange}
                    />
                    <h3>до</h3>
                    <input className="placemark_element" name="MaxAge" type="number" 
                        min="0" max="100" value={inputs.MaxAge} onChange={handleChange}
                    />
                    <h3>лет</h3>
                </div>
                <input id="newEventButton" type="button" className="ToGoButton"
                    value="Начать созыв!" onClick={handleCreate}
                />
            </form>
        </Popup>
    );
}


export { NewEventCard };