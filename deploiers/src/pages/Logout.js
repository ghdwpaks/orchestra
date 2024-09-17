// src/components/LogoutButton.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    
    const response = axios.post('http://127.0.0.1:8000/listener/send_email/');
    console.log("response :",response)


    // 로컬 스토리지에서 토큰 제거
    localStorage.removeItem('token');
    
    // 로그인 페이지로 리다이렉트
    navigate('/');
    
    // 서버에 로그아웃 사실 알림 (옵션)
    // axios.post('http://127.0.0.1:8000/listener/logout/');
  };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default LogoutButton;