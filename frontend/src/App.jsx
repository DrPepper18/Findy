import React from 'react';
import './styles/App.css';
import {RegScreen} from "./components/Register";
import {LoginScreen} from "./components/Login";
import MainScreen from "./components/MainPage"
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<MainScreen/>}/>
                <Route path="/register" element={<RegScreen/>}/>
                <Route path="/login" element={<LoginScreen/>}/>
            </Routes>
        </Router>
    );
}

export default App;