import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import YouTube from 'react-youtube';
import './MyTableStyles.css';  // 기존의 스타일 파일

function Dashboard() {
  const [data, setData] = useState('Loading...');
  const [csrfToken, setCsrfToken] = useState('');
  const navigate = useNavigate();
  const [hasToken, setHasToken] = useState(false); // 토큰 유무를 추적하는 상태 추가

  const handleLogin = () => {
    navigate('/login');
  };

  const handleSignUp = () => {
    navigate('/signup');
  };

  const handleUserPage = () => {
    navigate('/user');
  };
  
  const handleAddVid = () => {
    navigate('/addvid');
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      var params = {
        l:0 
      };
      console.log("token :",token)
      axios.get('http://127.0.0.1:8000/magnifyer/dashboard/', {
          params: params,
          headers: { Authorization: `Token ${token}` }
        })
        .then(response => {
          setHasToken(true);
          if (response.data.result.length > 0) {
            console.log("data :",data)
            setData(response.data.result);
          } else {
            setData('No data available');
          }
        });

    } else {
      setHasToken(false);
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
      headers: { Authorization: `Token ${token}` }
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
    {/* /addvid로 이동하는 버튼 추가 */}
    {hasToken && (
      <button onClick={handleAddVid}>Add Video</button>
    )}

    {data === 'Please login or sign up.' ? (
      <div>
        <button onClick={handleLogin}>Login</button>
        <button onClick={handleSignUp}>Sign Up</button>
      </div>
    ) : typeof data === 'string' ? (
      <p>{data}</p>
    ) : (
      <div style={{ position: 'relative', width: '90%', marginLeft: '10px' }}>
        <table className="myTable" style={{ marginLeft: '10px' }}>
          <tbody>
            {data.map((item, index) => (
              <tr key={item.id || index}>
                <td style={{ width: '20%', padding: '10px' }}>
                  <button 
                    onClick={() => handleNavigation(item)}
                    style={{
                      fontSize: '20px', // 글꼴 크기를 키워서 버튼 텍스트 확대
                      width: '100%', // 버튼의 너비를 전체 셀 너비로 설정
                      height: '60%', // 버튼의 높이를 직접 설정
                    }}>
                      {item.name.length > 15 ? `${item.name.slice(0, 15)}...` : item.name}
                  </button>
                </td>
                <td style={{ width: '15%', padding: '10px' }}>
                  {item.tag && item.tag.length > 0 ? (
                    <p>
                      {item.tag.map((tagItem, tagIndex) => (
                        <p key={tagIndex} className="gray-background">{tagItem.name}</p>
                      ))}
                    </p>
                  ) : (
                    <p/>
                  )}
                </td>
                <td style={{ width: '65%', padding: '10px' }}>
                  <div className="video-container">

                    
                    <iframe
                      class="video"
                      src={`https://www.youtube.com/embed/${item.url}`}
                      frameborder="0"
                      allowfullscreen
                    />

                    {/* <YouTube videoId={item.url} containerClassName="youtube-container" style={{ width: '100%', height: 'auto' }} /> */}
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
