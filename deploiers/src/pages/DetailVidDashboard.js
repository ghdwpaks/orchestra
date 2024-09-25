import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import YouTube from 'react-youtube';
import { useParams } from 'react-router-dom';
import './MyTableStyles.css';
import { useNavigate } from 'react-router-dom';


function DetailVidDashboard({ videoId }) {
  const [videoData, setVideoData] = useState(null);
  const [tagInput, setTagInput] = useState('');
  const [highlightInput, setHighlightInput] = useState('');
  let { id } = useParams();
  let { timestamp } = useParams();
  const navigate = useNavigate();
  

  useEffect(() => {
    const token = localStorage.getItem('token');
    const params = { l: 1, vid_id: id };
    axios.get('http://127.0.0.1:8000/magnifyer/vid_detail/', {
      params,
      headers: { Authorization: `Token ${token}` }
    })
    .then(response => setVideoData(response.data.result))
    .catch(error => console.error('Error fetching video details', error));



  }, [videoId]);

  const navigateDashboard = () => {
    
    // navigate('/', { state: { data, l, size, loc, loc_limit, word, field } });
    navigate('/');
  };

  const handleTagDelSubmit = (tag_id) => {
    
    const token = localStorage.getItem('token');
    const params = { tag_id: tag_id, vid_id: id , l: 1};
    
    axios.post('http://127.0.0.1:8000/tag/del_tag/', 
      params,  // 이 부분은 데이터 본문으로 전달
      {
        headers: { Authorization: `Token ${token}` }
      }
    )

    // Submit tag logic here
    setTagInput('');
  };


  const handleHighDelSubmit = (high_id) => {
    
    const token = localStorage.getItem('token');
    const params = { high_id: high_id, vid_id: id , l: 1};
    
    axios.post('http://127.0.0.1:8000/high/del_high/', 
      params,  // 이 부분은 데이터 본문으로 전달
      {
        headers: { Authorization: `Token ${token}` }
      }
    )

    // Submit tag logic here
    setTagInput('');
  };

  const handleTagSubmit = () => {
    
    const token = localStorage.getItem('token');
    const params = { name: tagInput, vid_id: id , l: 1};
    axios.post('http://127.0.0.1:8000/tag/add_tag/', 
      params,  // 이 부분은 데이터 본문으로 전달
      {
        headers: { Authorization: `Token ${token}` }
      }
    );

    // Submit tag logic here
    setTagInput('');
  };

  const handleHighlightSubmit = () => {
    const token = localStorage.getItem('token');
    const params = { timestamp: highlightInput, vid_id: id };
    axios.post('http://127.0.0.1:8000/high/add_high/', 
      params,  // 이 부분은 데이터 본문으로 전달
      {
        headers: { Authorization: `Token ${token}` }
      }
    );

    // Submit highlight logic here
    setHighlightInput('');
  };

  if (!videoData) return <div>Loading...</div>;

  return (
    
    <div style={{ position: 'relative', width: '80%', marginLeft: '10px' }}>
    <body>
    
      <button onClick={() => { navigateDashboard(); window.location.reload();}}>Dashboard</button>
      <table className="myTable" style={{ marginLeft: '10px' }}>
        <caption>
          <h2
            style={{
              color: 'gray',
              marginBottom: '20px',
              textAlign: 'center',
            }}
          >
            {videoData.vid.name}
          </h2>
        </caption>
        <thead>
          <tr>
            <th style={{ position: 'relative', width: '20%' }}>
              {videoData.tag.map((item, index) => (
                <tr key={index}>
                  <td>
                    <button onClick={() => {handleTagDelSubmit(item.id); window.location.reload();}}>{item.name}</button>
                  </td>
                </tr>
              ))}
            </th>
            <th>
              <div class="video-container">
                <iframe
                  class="video"
                  src={`https://www.youtube.com/embed/${videoData.vid.url}`}
                  frameborder="0"
                  allowfullscreen
                />
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input
                type="text"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                placeholder="Enter tag"
                style={{ borderColor: 'blue' }}
              />
              <button onClick={() => { handleTagSubmit(); window.location.reload();}} style={{ backgroundColor: 'lightblue' }}>
                Submit Tag
              </button>
            </td>
            <td>
              <input
                type="text"
                value={highlightInput}
                onChange={(e) => setHighlightInput(e.target.value)}
                placeholder="Enter highlight URL"
                style={{ borderColor: 'purple' }}
              />
              <button onClick={() => { handleHighlightSubmit(); window.location.reload();}} style={{ backgroundColor: 'violet' }}>
                Submit Highlight
              </button>
            </td>
          </tr>
  
          {videoData.high.map((item, index) => (
            <tr key={index}>
              <td></td>
              <td>
                <div class="video-container">
                  <iframe
                    class="video"
                    src={`https://www.youtube.com/embed/${videoData.vid.url}?start=${item.timestamp}`}
                    frameborder="0"
                    allowfullscreen
                  />
                </div>
              </td>
              <td width="10px" marginLeft="0px">
                <td>
                  <button onClick={() => {handleHighDelSubmit(item.id); window.location.reload();}}>삭제</button>
                </td>
              </td>
            </tr>
          ))}
  
        </tbody>
      </table>
    </body>
  </div>
  
);


}

export default DetailVidDashboard;
