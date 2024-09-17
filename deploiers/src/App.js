import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import DetailVidDashboard from './pages/DetailVidDashboard';
import SignUp from './pages/SignUp';
import Login from './pages/Login';
import LogoutButton from './pages/Logout'; // 로그아웃 버튼 컴포넌트 임포트

function App() {
  return (
    <Router>
      <div className="App">
        <LogoutButton />  {/* 로그아웃 버튼 추가 */}
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/detail/:id" element={<DetailVidDashboard />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div> 
    </Router>
  );
}

export default App;
