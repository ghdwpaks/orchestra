import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';



function Dashboard() {
  const [data, setData] = useState('Loading...');
  const [csrfToken, setCsrfToken] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate('/login');
  };

  const handleSignUp = () => {
    navigate('/signup');
  };

  const handleUserPage = () => {
    navigate('/user');
  };

  useEffect(() => {
    const token = sessionStorage.getItem('csrfToken');
    setCsrfToken(token);
    console.log("csrfToken :", csrfToken);
    if (csrfToken) {
      axios.get('http://127.0.0.1:8000/magnifyer/dashboard/')
        .then(response => {
          // res 배열의 첫 번째 객체에서 name 값을 추출하여 저장
          if (response.data.res && response.data.res.length > 0) {
            setData(response.data.res[0].name);
          } else {
            setData('No data available');
          }
        })
        .catch(error => {
          console.error('There was an error!', error);
          setData('Failed to load data');
        });
    } else {
      setData('Please login or sign up.'); // CSRF 토큰이 없을 경우 메시지 설정
    }
  }, [csrfToken]); // csrfToken 변경 시 재실행

  return (
    <div>
      <h1>Dashboard Data</h1>
      {data === 'Please login or sign up.' ? (
        <div>
          <button onClick={handleLogin}>Login</button>
          <button onClick={handleSignUp}>Sign Up</button>
        </div>
      ) : (
        <div>
          <p>{data}</p>
          <button onClick={handleUserPage}>Go to User Page</button>
        </div>
      )}
    </div>
  );
}

export default Dashboard;

