import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import DetailVidDashboard from './pages/DetailVidDashboard';
import SignUp from './pages/SignUp';
import Login from './pages/Login';
import LogoutButton from './pages/Logout'; // 로그아웃 버튼 컴포넌트 임포트
import EmailInput from './pages/EmailInput';
import EmailCodeInput from './pages/EmailCodeInput';
import ChangePassword from './pages/ChangePassword';
import AddVid from './pages/AddVid';


function AppContent() {
  const location = useLocation();  // 현재 URL 경로 확인

  return (
    <div className="App">
      {location.pathname === "/" && <LogoutButton />}
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/detail/:id" element={<DetailVidDashboard />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/emailinput" element={<EmailInput />} />
        <Route path="/emailcodeinput" element={<EmailCodeInput />} />
        <Route path="/changepassword" element={<ChangePassword />} />
        <Route path="/addvid" element={<AddVid />} />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
