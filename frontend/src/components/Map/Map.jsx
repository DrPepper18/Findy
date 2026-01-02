import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import { EventCard } from '../EventCard/EventCard.jsx';
import { NewEventCard } from '../NewEvent/NewEvent.jsx';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './Map.css';

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

const Map = ({ events }) => {
    const [map, setMap] = useState(null);
    const [mapCenter, setMapCenter] = useState(DEFAULT_CENTER);
    const markerRefs = useRef({});
    // Добавляем флаг, чтобы не "летать" по карте при каждом обновлении списка ивентов
    const hasCenteredRef = useRef(false);

    useEffect(() => {
        // Ждем, пока карта проинициализируется и придут данные
        if (!map || events.length === 0 || hasCenteredRef.current) return;

        const params = new URLSearchParams(window.location.search);
        const targetMarkerID = params.get('id');

        if (targetMarkerID) {
            const id = Number(targetMarkerID);
            const event = events.find(e => e.ID === id);
            const marker = markerRefs.current[id];

            if (event && marker) {
                hasCenteredRef.current = true; // Фиксируем, что первичный фокус выполнен
                
                // Сначала летим...
                map.setView([event.Latitude, event.Longitude], 15, {
                    animate: true,
                });
                marker.openPopup();
            }
        }
    }, [events, map]); // Зависимости верны
    
    return (
        <div id="map">
            <MapContainer 
                center={DEFAULT_CENTER} 
                zoom={DEFAULT_ZOOM} 
                ref={setMap} // Правильное получение инстанса L.Map
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
                    <Marker
                        key={event.ID}
                        position={[event.Latitude, event.Longitude]}
                        ref={(el) => {
                            if (el) markerRefs.current[event.ID] = el;
                        }}
                    >
                        <EventCard event={event}/>
                    </Marker>
                ))}
            </MapContainer>
        </div>
    );
};


export default Map;
