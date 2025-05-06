import {Event} from "./Event";
const EventsList = ({events}) => {
    return (
        <div id="CurrentEvents">
            {events.length > 0 ? 
                events.map((event, index) => (
                    <Event key={index} event={event}/>
                )) :
                <h2 style={{textAlign: 'center'}}>
                    Здесь ничего нет. Будь первым!
                </h2>
            }
        </div>
    );
};

export default EventsList;