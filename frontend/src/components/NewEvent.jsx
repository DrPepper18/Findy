import {config, getCookie} from "../config"


const NewEventForm = `
    <div id="NewEventForm" style="width: 250px;">
        <input
            class="placemark_element"
            id="name_input"
            placeholder="Название"
        />
        <div id="datetimeDiv">
            <input
                class="placemark_element"
                id="date_input"
                style="width: 55%;"
                type="date"
            />
            <input
                class="placemark_element"
                id="time_input"
                type="time"
            />
        </div>
        <div id="capacityDiv">
            <input
                class="placemark_element"
                id="capacity_input"
                type="number"
                min="1" max="16" value="5"
            />
            <h3>человек</h3>
        </div>
        <div id="ageDiv">
            <h3>от</h3>
            <input 
                class="placemark_element"
                id="minage_input"
                type="number" 
                min="0" max="100"
            />
            <h3>до</h3>
            <input 
                class="placemark_element"
                id="maxage_input"
                type="number" 
                min="0" max="100" 
            />
            <h3>лет</h3>
        </div>
        <input
            id="newEventButton"
            type="button"
            class="ToGoButton"
            value="Начать созыв!"
        />
    </div>`


const NewEventCard = (coord) => {
    return new window.ymaps.Placemark(coord, {
        balloonContentHeader: "<h2>Новое событие</h2>",
        balloonContentBody: NewEventForm,
        hintContent: "Нажмите, чтобы создать событие"
    }, {preset: 'islands#redIcon'});
}


const NewEventAdd = async (event) => {        
    if (!(event.Name && event.DateTime)) {
        alert("Введите все данные");
    } else {
        let token = await getCookie('jwt');
        const response = await fetch(config.Host_url + 'event/create', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(event)
        });

        if (response.ok) {
            window.location.href = '/';
            return;
        }
    }
};


export {NewEventForm, NewEventCard, NewEventAdd};