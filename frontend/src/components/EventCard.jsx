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
    }
}
export default EventCard;