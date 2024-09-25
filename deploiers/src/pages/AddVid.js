import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const YoutubeUrlForm = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();  // 폼 제출 기본 동작 방지
    
    if (youtubeUrl.trim() === '') {
      alert('유튜브 URL을 입력해주세요.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/vid/add_vid/', {
        url: youtubeUrl  // vid 키로 유튜브 URL을 전송
      });
      console.log('서버 응답:', response.data);
      alert('URL이 성공적으로 전송되었습니다!');
      navigate('/');
    } catch (error) {
      console.error('에러 발생:', error);
      alert('URL 전송 중 에러가 발생했습니다.');
    }
  };
  const handleSyncChannelVideoList = (item) => {
    const params = {update_channel_videos: item}
    const token = localStorage.getItem('token');
    axios.post('http://127.0.0.1:8000/vid/add_vid/', 
      params,  // 이 부분은 데이터 본문으로 전달
      {
        headers: { Authorization: `Token ${token}` }
      }
    )
    navigate('/')
  };

  return (
    <div style={{ marginTop: '20px', marginLeft: '25px', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: '10px' }}>
        <label style={{ fontSize: '18px', marginBottom: '5px', width: '100%' }}>
          유튜브 URL:
          <textarea
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
            placeholder="유튜브 URL을 입력하세요"
            style={{ width: '80%', height: '160px', padding: '20px', fontSize: '16px', whiteSpace: 'pre-wrap' }}
          />
        </label>
        <button type="submit" style={{ width: '50%', height: '50px', padding: '10px', fontSize: '18px', cursor: 'pointer' }}>URL 전송</button>
      </form>

      
      <button 
        onClick={() => handleSyncChannelVideoList(true)}
        style={{
          fontSize: '20px', // 글꼴 크기를 키워서 버튼 텍스트 확대
          height: '60px', // 버튼의 높이를 직접 설정
          marginTop: '120px'
        }}>
          채널 동영상 동기화
      </button>


    </div>
  );
};

export default YoutubeUrlForm;
