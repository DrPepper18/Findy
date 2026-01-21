import React, { useState } from 'react';
import './Sidebar.css'


const Sidebar = () => {
    const [hidden, setHidden] = useState(true);
    const handleClick = () => setHidden(!hidden);
    
    return (
        <div className={`sidebar ${hidden? "sidebar--closed" : "sidebar--open"}`} onClick={handleClick}>
            <div className="sidebar__content">
                <h2>Здесь будет редактирование профиля</h2>
            </div>
        </div>
    );
};

export default Sidebar;