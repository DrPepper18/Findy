import {config, getCookie} from '../config';


const EventJoin = async (eventID) => {
    let token = await getCookie('jwt');
    await fetch(config.Host_url+'event/join', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'EventID': eventID})
    })
    alert('Success!');
    document.getElementById("ToGoID").disabled = true;
}


const EventCard = (event) => {
    return {
        balloonContentHeader: `<h3>${event.Name}</h3>`,
        balloonContentBody: `
            <p>${new Date(event.DateTime).toLocaleDateString('ru-RU')}</p>
            <p>${event.MinAge}-${event.MaxAge} лет, до ${event.Capacity} человек</p>
            <input type="button" id="ToGoID" class="ToGoButton" value="Я приду!"></input>
        `,
        balloonContentFooter: event.ID ? `http://localhost:3000?id=${event.ID}` : 'Перезагрузите страницу',
        hintContent: event.Name,
        eventID: event.ID
    }
}

const EventJoinCheck = async (eventID) => {
    let token = await getCookie('jwt');
    const response = await fetch(config.Host_url + 'event/joincheck', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"EventID": eventID})
    });
    let data = await response.json();
    return data.joined;
}


export {EventCard, EventJoin, EventJoinCheck};