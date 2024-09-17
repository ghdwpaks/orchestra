import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import YouTube from 'react-youtube';
import './MyTableStyles.css';

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
    console.log("token :", token);
    if (token) {
      var params = {
        l:0 
      };
      axios.get('http://127.0.0.1:8000/magnifyer/dashboard/',
        {
          params: params,
          headers: { Authorization: 'Token ' + token }
        }
      ).then(response => {
        console.log("ghdwpaks")
        console.log("response :",response)
        // res 배열의 첫 번째 객체에서 name 값을 추출하여 저장
        if (response.data.result.length > 0) {
          setData(response.data.result);
        } else {
          setData('No data available');
        }
      });

    } else {
      setData('Please login or sign up.'); // CSRF 토큰이 없을 경우 메시지 설정
    }
  }, [csrfToken]); // csrfToken 변경 시 재실행

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
        console.log("JSON.stringify(data, null, 2) :",JSON.stringify(response.data, null, 2))
        console.log("Video details:", response.data);
        // 추가적인 처리 로직을 여기에 작성할 수 있습니다.
      })
      .catch(error => {
        console.error('Error fetching video details:', error);
      });
    };
    const handleNavigation = (item) => {
      console.log("item :", item);
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
          <table>
            <tr>
              
              <td></td>
            </tr>
          </table>
          {data.map((item, index) => (
            <tr>
              <td>
                <button onClick={() => handleNavigation(item)}>{item.name}</button>
              </td>
              <td>
              <div class="video-container">
                <YouTube videoId={item.url.split('=')[1]} containerClassName="youtube-container" style={{ width: '100px'}} />
              </div>
              </td>
            </tr>
          ))}
          {/* 다른 버튼이나 추가적인 요소들이 필요하다면 여기에 포함시키세요. */}
        </div>
      )}
    </div>
  );
}

export default Dashboard;

