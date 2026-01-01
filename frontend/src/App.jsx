import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { RegScreen } from "./pages/Register/Register.jsx";
import { LoginScreen } from "./pages/Login/Login.jsx";
import MainScreen from "./pages/MainPage/MainPage.jsx"
import './styles/index.css'
import './styles/base.css'


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