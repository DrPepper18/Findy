import React, { useEffect, useState } from 'react';
import { getUserInfo, updateUserInfo } from '../../api';
import './Sidebar.css'


const Sidebar = () => {
    const [hidden, setHidden] = useState(true);
    const handleClick = () => setHidden(!hidden);
    const [nickname, setNickname] = useState('');
    const [age, setAge] = useState();
    
    const handleEdit = async () => {
        await updateUserInfo(nickname, age);
        alert("Данные успешно сохранены");
    }

    useEffect(() => {
        const fetchUserData = async () => {
            let userData = await getUserInfo();
            console.log(userData);
            setNickname(userData["name"]);
            setAge(userData["age"]);
        }
        fetchUserData();
    }, []);

    return (
        <div className={`sidebar ${hidden? "sidebar--closed" : "sidebar--open"}`}>
            <input type="button" value="☰" onClick={handleClick}/>
            <div className="sidebar__content">
                <h2>Редактирование профиля</h2>
                <input
                    className="reg-screen__input"
                    placeholder="Nickname"
                    value={nickname}
                    onChange={(e) => setNickname(e.target.value)}
                />
                <br />
                <input
                    type="number"
                    className="reg-screen__input"
                    placeholder="Age"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                />
                <br />
                <input
                    className="button button--to-go"
                    type="button"
                    value="Save"
                    onClick={handleEdit}
                />
            </div>
        </div>
    );
};

export default Sidebar;