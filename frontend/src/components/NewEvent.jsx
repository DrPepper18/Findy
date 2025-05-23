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

export default NewEventForm;