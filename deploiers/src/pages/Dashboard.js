import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import YouTube from 'react-youtube';
import './MyTableStyles.css';  // 기존의 스타일 파일

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
    const token = localStorage.getItem('token');
    if (token) {
      var params = {
        l:0 
      };
      axios.get('http://127.0.0.1:8000/magnifyer/dashboard/', {
          params: params,
          headers: { Authorization: 'Token ' + token }
        })
        .then(response => {
          if (response.data.result.length > 0) {
            setData(response.data.result);
          } else {
            setData('No data available');
          }
        });

    } else {
      setData('Please login or sign up.');
    }
  }, [csrfToken]);

  const fetchVideoDetail = (videoId) => {
    const token = localStorage.getItem('token');
    const params = {
      l: 1,
      vid_id: videoId
    };

    axios.get('http://127.0.0.1:8000/magnifyer/vid_detail/', {
      params: params,
      headers: { Authorization: 'Token ' + token }
    })
    .then(response => {
      console.log("Video details:", response.data);
    })
    .catch(error => {
      console.error('Error fetching video details:', error);
    });
  };

  const handleNavigation = (item) => {
    if (item && item.id) {
      navigate(`/detail/${item.id}`);
    } else {
      console.error('Item or item.id is undefined');
    }
  };

  return (
    <div>
      <h1>Dashboard</h1>
      {data === 'Please login or sign up.' ? (
        <div>
          <button onClick={handleLogin}>Login</button>
          <button onClick={handleSignUp}>Sign Up</button>
        </div>
      ) : typeof data === 'string' ? (
        <p>{data}</p>
      ) : (
        <div>
          <table className="custom-table">
            <tbody>
              {data.map((item, index) => (
                <tr key={item.id || index}>
                  <td>
                    <button onClick={() => handleNavigation(item)}>{item.name}</button>
                  </td>
                  <td>
                    <div className="video-container">
                      <YouTube videoId={item.url.split('=')[1]} containerClassName="youtube-container" />
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
