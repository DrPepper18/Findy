import React, { useEffect, useState } from 'react';
import { getUserInfo, updateUserInfo } from '../../api';
import './Sidebar.css'
import { calculateAge } from '../../utils/DateFucntions';


const Sidebar = () => {
    const [hidden, setHidden] = useState(true);
    const handleClick = () => setHidden(!hidden);
    const [nickname, setNickname] = useState('');
    const [birthdate, setBirthdate] = useState('');
    
    const handleEdit = async () => {
        if (calculateAge(birthdate) < 18) {
            alert("Вам должно быть больше 18 лет.");
            return;
        }
        await updateUserInfo(nickname, birthdate);
        alert("Данные успешно сохранены");
    }

    useEffect(() => {
        const fetchUserData = async () => {
            let userData = await getUserInfo();
            console.log(userData);
            setNickname(userData["name"]);
            setBirthdate(userData["birthdate"]);
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
                    type="date"
                    className="reg-screen__input"
                    placeholder="Birthdate"
                    value={birthdate}
                    onChange={(e) => setBirthdate(e.target.value)}
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