import React, { useState, useEffect } from 'react';
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
  console.log("videoData :", JSON.stringify(videoData, null, 2));
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    console.log("id :",id);  // URL에서 추출한 vid_id를 콘솔에 출력
    console.log("token :",token)
    const params = { l: 1, vid_id: id };
    axios.get('http://127.0.0.1:8000/magnifyer/vid_detail/', {
      params,
      headers: { Authorization: `Token ${token}` }
    })
    .then(response => setVideoData(response.data.result))
    .catch(error => console.error('Error fetching video details', error));

    axios.get('http://127.0.0.1:8000/magnifyer/vid_detail/', {
      params,
      headers: { Authorization: `Token ${token}` }
    })
    .then(response => setVideoData(response.data.result))
    .catch(error => console.error('Error fetching video details', error));


  }, [videoId]);

  const navigateDashboard = () => {
    navigate(`/`);
  };

  const handleTagSubmit = () => {
    console.log('Submitting tag:', tagInput);
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
    
  <div style={{ position: 'relative', width: '80%'}}>

  <body>
    
    <button onClick={navigateDashboard} >Dashboard</button>
      <table className="myTable">
          <caption><h2 style={{ color: 'gray', marginBottom: '20px', textAlign: 'center' }}>{videoData.vid.name}</h2></caption>
          <thead>
              <tr>
                  <th style={{ position: 'relative', width: '20%'}}>
                    
                    {/* asdf */}
                      {videoData.tag.map((item, index) => (
                        <tr key={index}>
                          <td>
                            <button onClick={handleTagSubmit} >{item.name}</button>
                          </td>
                        </tr>
                      ))}
                  </th>
                  <th>
                  <div class="video-container"> 
                    <iframe class="video" src={`https://www.youtube.com/embed/${videoData.vid.url}`} frameborder="0" allowfullscreen/>
                  </div>
                  {/* <YouTube videoId={videoData.vid.url} containerClassName="youtube-container" style={{ width: '100%', height: '400px' }} /> */}
                  </th>
              </tr>
          </thead>
          <tbody>
              <tr>
                  <td>
                    <input
                      type="text"
                      value={tagInput}
                      onChange={e => setTagInput(e.target.value)}
                      placeholder="Enter tag"
                      style={{ borderColor: 'blue' }}
                    />
                    <button onClick={handleTagSubmit} style={{ backgroundColor: 'lightblue' }}>Submit Tag</button>
                  </td>
                  <td>
                    <input
                      type="text"
                      value={highlightInput}
                      onChange={e => setHighlightInput(e.target.value)}
                      placeholder="Enter highlight URL"
                      style={{ borderColor: 'purple' }}
                    />
                    <button onClick={handleHighlightSubmit} style={{ backgroundColor: 'violet' }}>Submit Highlight</button>
                  </td>
              </tr>
              
              {videoData.high.map((item, index) => (
                <tr key={index}>
                  <td></td>
                  <td>
                    <div class="video-container"> 
                      <iframe class="video" src={`https://www.youtube.com/embed/${videoData.vid.url}?start=${item.timestamp}`} frameborder="0" allowfullscreen/>
                    </div>
                    {/* <YouTube videoId={videoData.vid.url} opts={{height: '400',width: '100%',playerVars: {rel: 0, start: 35}}} containerClassName="youtube-container" style={{ width: '100%', height: '400px' }} /> */}
                  </td>
                </tr>
              ))}

              <tr>
              <td></td>
              </tr>
              
          </tbody>
      </table>
      


  </body>




    
  </div>
);


}

export default DetailVidDashboard;
