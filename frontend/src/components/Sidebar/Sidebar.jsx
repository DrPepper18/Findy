import React, { useEffect, useState } from 'react';
import { getUserInfo, updateUserInfo, deleteUser } from '../../api';
import './Sidebar.css'
import { calculateAge } from '../../utils/DateFucntions';


const Sidebar = () => {
    const [hidden, setHidden] = useState(true);
    const handleClick = () => setHidden(!hidden);
    const [nickname, setNickname] = useState('');
    const [birthdate, setBirthdate] = useState('');
    const PRIVACY_LINK = 
    "https://docs.google.com/document/d/11QdpZhEwXqzgPyeY6tpTM_JyKh28AqKz5OHvJetl2Gg/edit?usp=sharing";
    
    const handleEdit = async () => {
        if (calculateAge(birthdate) < 18) {
            alert("Вам должно быть больше 18 лет.");
            return;
        }
        await updateUserInfo(nickname, birthdate);
        alert("Данные успешно сохранены");
    }
    const handleDelete = async () => {
        const is_sure = confirm("Ваш аккаунт будет удалён безвозвратно. Вы уверены?");
        if (is_sure) {
            try {
                await deleteUser();
                window.location.href = '/login';
            } catch {
                console.error("Error occured");
            }
            
        }
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
                <div className='content-block'>
                    <h2>Редактирование профиля</h2>
                    <input
                        className="reg-screen__input"
                        placeholder="Nickname"
                        value={nickname}
                        onChange={(e) => setNickname(e.target.value)}
                    />
                    <input
                        type="date"
                        className="reg-screen__input"
                        placeholder="Birthdate"
                        value={birthdate}
                        onChange={(e) => setBirthdate(e.target.value)}
                    />
                    <input
                        className="button button--to-go"
                        type="button"
                        value="Сохранить изменения"
                        onClick={handleEdit}
                    />
                </div>
                <div className='content-block'>
                    <h2>Памятка</h2>
                    <ul>
                        <li>Предупреждайте близких о том, куда и с кем идёте гулять</li>
                        <li>Встречайтесь в людных местах</li>
                        <li>Избегайте скромных переулков</li>
                        <li>Не принимайте и не отдавайте деньги</li>
                        <li>Не садитесь в машину и не заходите домой</li>
                        <li>Не бойтесь говорить НЕТ</li>
                    </ul>
                </div>
                <footer className='content-block'>
                    <p><a href={PRIVACY_LINK}>Политика и Правила сервиса</a></p>
                    <p><a href="" onClick={handleDelete}>Удалить аккаунт</a></p>
                </footer>
            </div>
        </div>
    );
};

export default Sidebar;