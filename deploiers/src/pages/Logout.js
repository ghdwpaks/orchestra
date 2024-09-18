import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // 로컬 스토리지에서 토큰 제거
    localStorage.removeItem('token');
    console.log('토큰이 삭제되었습니다.');

    // 로그인 페이지로 리다이렉트
    if (window.location.pathname === '/') {
      // 사용자가 이미 "/"에 있다면 새로 고침
      window.location.reload();
    } else {
      // 다른 페이지라면 "/"로 리다이렉트
      navigate('/');
    }

    // 서버에 로그아웃 요청 보내기 (선택 사항)
    // axios.post('http://127.0.0.1:8000/listener/logout/');
  };

  // useEffect를 사용하여 토큰 삭제 여부를 확인
  useEffect(() => {
    console.log('현재 토큰:', localStorage.getItem('token'));
  }, []);

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default LogoutButton;
