import { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import { EventCard } from './EventCard.jsx';
import { NewEventCard } from './NewEvent.jsx';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import '../styles/App.css';
import '../styles/NewEvent.css';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';



let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;


const DEFAULT_CENTER = [55.7558, 37.6176];
const DEFAULT_ZOOM = 10;


function MapEventsHandler({ setCenter }) {
    const map = useMapEvents({
        moveend: () => {
            const center = map.getCenter();
            setCenter([center.lat, center.lng]);
        },
    });
    return null;
}

const Map = ({events}) => {

    const eventsRef = useRef(events);
    useEffect(() => {
        eventsRef.current = events;
    }, [events]);

    const [mapCenter, setMapCenter] = useState(DEFAULT_CENTER);
    
    return (
        <div id="map">
            <MapContainer 
            center={DEFAULT_CENTER} 
            zoom={DEFAULT_ZOOM} 
            style={{ height: "100%", width: "100%" }}
            >
                <TileLayer
                attribution='&copy; OpenStreetMap'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                <MapEventsHandler setCenter={setMapCenter} />

                <Marker position={mapCenter} icon={redIcon}>
                    <NewEventCard position={mapCenter} />
                </Marker>

                {events.map((event) => (
                <Marker key={event.ID} position={[event.Latitude, event.Longitude]}>
                    <EventCard event={event}/>
                </Marker>
                ))}
            </MapContainer>
        </div>
    );
};


export default Map;
