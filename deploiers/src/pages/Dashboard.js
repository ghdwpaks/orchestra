import React, { useState, useEffect, useContext, useRef} from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import YouTube from 'react-youtube';
import './MyTableStyles.css';  // 기존의 스타일 파일

function Dashboard() {
  const token = localStorage.getItem('token');
  const savedState = JSON.parse(localStorage.getItem('dashboardState'));
  
  // data를 useState로 변경
  const navigate = useNavigate();
  const [isNavigating, setIsNavigating] = useState(false);  // 페이지 이동 여부를 추적하는 상태
  const [hasToken, setHasToken] = useState(false); // 토큰 유무를 추적하는 상태 추가
  const [data, setData] = useState(savedState?.data || 'Loading...');
  const [word, setWord] = useState(savedState?.word || '');
  const [field, setField] = useState(savedState?.field || 'tag');
  
  const l = useRef(savedState?.l || 1);
  const size = useRef(savedState?.size || 10);
  const loc = useRef(savedState?.loc || 1);
  const loc_limit = useRef(savedState?.loc_limit || 1);
  const sort = useRef(savedState?.sort || "upd");


  const handleLogin = () => {
    setIsNavigating(true);
    navigate('/login');
  };

  const handleSignUp = () => {
    setIsNavigating(true);
    navigate('/signup');
  };

  const handleUserPage = () => {
    setIsNavigating(true);
    navigate('/user');
  };
  
  const handleAddVid = () => {
    setIsNavigating(true);
    navigate('/addvid');
  };

  const handleNavigation = (item) => {
    if (item && item.id) {
      setIsNavigating(true);
      navigate(`/detail/${item.id}`);
    } else {
      console.error('Item or item.id is undefined');
    }
  };

  const handleWord = (e) => {
    setWord(e.target.value)
  };

  const handleField = (e) => {
    setField(e.target.value)
  };
  

  const handleLoc = (e) => {
    loc.current = e.target.value;
    
    const params = {l:l.current,size:size.current,loc:loc.current,word:word,field:field,sort:sort.current};
    axios.get('http://127.0.0.1:8000/magnifyer/dashboard/', {
      params,  // params를 객체로 전달
      headers: { Authorization: `Token ${token}` }
    })
    .then(response => {
      console.log("handleSearch entered");
      handlePageData(response.data);
    });
  };

  const handlePageData = (req_data) => {
    setHasToken(true);
    if (req_data.result.length > 0) {
      console.log("result.length() :", req_data.result.length);
      // 상태 변경 (렌더링 트리거)
      console.log("req_data :",req_data)
      console.log("req_data.l :",req_data.l)
      console.log("req_data.Size :",req_data.size)
      console.log("req_data.Loc :",req_data.loc)


      setData(req_data.result);
      l.current = req_data.l;
      size.current = req_data.size;
      loc.current = req_data.loc;
      loc_limit.current = req_data.loc_limit;
      sort.current = req_data.sort;
      localStorage.setItem('dashboardState', JSON.stringify({ 
        data,
        word,
        field,
        l:l.current,
        size:size.current,
        loc:loc.current,
        loc_limit:loc_limit.current,
        sort:sort.current,
      }));
    } else {
      setData('No data available');
    }
  };

  useEffect(() => {
    const clearLocalStorage = (event) => {
      // 사용자가 직접 새로고침을 할 때만 localStorage를 비움
      if (!isNavigating) {
        localStorage.removeItem('dashboardState');
      }
    };

    window.addEventListener('beforeunload', clearLocalStorage);
    
    if (token) {
      const savedState = JSON.parse(localStorage.getItem('dashboardState'));
      const params = {
        l:savedState?.l || 1,
        size:savedState?.size || 10,
        loc:savedState?.loc || 1,
        loc_limit:savedState?.loc_limit || 1,
        word:savedState?.word || '',
        field:savedState?.field || 'tag',
        sort:savedState?.sort || "upd"
      };
      axios.get('http://127.0.0.1:8000/magnifyer/dashboard/', {
          params: params,
          headers: { Authorization: `Token ${token}` }
        })
        .then(response => {
          handlePageData(response.data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    } else {
      setHasToken(false);
      setData('Please login or sign up.');
    }

    return () => {
      window.removeEventListener('beforeunload', clearLocalStorage);
    };
  }, [isNavigating, l, size, loc, token]);

  const handleSearch = () => {
    const params = {l:l.current,size:size.current,loc:loc.current,word:word,field:field,sort:sort.current};
    axios.get('http://127.0.0.1:8000/magnifyer/dashboard/', {
      params,  // params를 객체로 전달
      headers: { Authorization: `Token ${token}` }
    })
    .then(response => {
      handlePageData(response.data);
    });
  };

  const handleSizeChange = (e) => {
    console.log("entered");
    console.log("e.target.value :", e.target.value);
    size.current = e.target.value;
    
    const params = {l:l.current,size:size.current,loc:loc.current,word:word,field:field,sort:sort.current};
    axios.get('http://127.0.0.1:8000/magnifyer/dashboard/', {
      params,  // params를 객체로 전달
      headers: { Authorization: `Token ${token}` }
    })
    .then(response => {
      console.log("handleSearch entered");
      handlePageData(response.data);
    });
  };

  const handleSortChange = (e) => {
    console.log("entered");
    console.log("e.target.value :", e.target.value);
    sort.current = e.target.value;
    
    const params = {l:l.current,size:size.current,loc:loc.current,word:word,field:field,sort:sort.current};
    axios.get('http://127.0.0.1:8000/magnifyer/dashboard/', {
      params,  // params를 객체로 전달
      headers: { Authorization: `Token ${token}` }
    })
    .then(response => {
      console.log("handleSearch entered");
      handlePageData(response.data);
    });
  };

  return (
    <div>
      <h1>Dashboard</h1>
      {hasToken && (
        <>
          <button onClick={handleAddVid}>Add Video</button>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <input
                type="text"
                placeholder="검색어를 입력하세요"
                value={word}
                onChange={handleWord}
                style={{ padding: '10px', marginRight: '10px' }}
              />

              <select
                value={field}
                onChange={handleField}
                style={{ padding: '10px', marginRight: '10px' }}
              >
                <option value="tag">태그</option>
                <option value="name">제목</option>
              </select>

              <button
                onClick={handleSearch}
                style={{ padding: '10px 20px', backgroundColor: 'blue', color: 'white', cursor: 'pointer' }}
              >
                검색
              </button>
            </div>

            <div style={{ display: 'flex', alignItems: 'center' }}>
              
              <select
                value={sort.current}
                onChange={handleSortChange}
                style={{ padding: '10px', marginRight: '10px' }}
              >
                <option value="upd">업로드 최신순</option>
                <option value="upa">업로드 오래된순</option>
                <option value="idd">id 최신순</option>
                <option value="ida">id 오래된순</option>
              </select>

              <select
                value={size.current}
                onChange={handleSizeChange}
                style={{ padding: '10px', marginRight: '10px' }}
              >
                <option value="5">5개</option>
                <option value="10">10개</option>
                <option value="30">30개</option>
                <option value="100">100개</option>
              </select>
              
              <select
                value={loc.current}
                onChange={handleLoc}
                style={{ padding: '10px', marginRight: '10px' }}
              >
                {Array.from({ length: loc_limit.current }, (_, i) => (
                  <option key={i + 1} value={i + 1}>
                    {i + 1} P
                  </option>
                ))}
              </select>
            </div>
          </div>
        </>
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
                    {/*
                    <button 
                      onClick={() => handleNavigation(item)}
                      style={{
                        fontSize: '20px', 
                        width: '100%', 
                        height: '60%', 
                      }}>
                      {item.name.length > 15 ? `${item.name.slice(0, 15)}...` : item.name}
                    </button>
                    */}
                    <a 
                    onClick={() => handleNavigation(item)} 
                    target="_blank" 
                    class="button-link"
                    style={{
                      fontSize: '20px', 
                      width: '100%', 
                      height: '60%', 
                    }}>
                      {item.name.length > 15 ? `${item.name.slice(0, 15)}...` : item.name}
                    </a>
                  </td>
                  <td style={{ width: '20%', padding: '10px' }}>
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
                  <td style={{ width: '55%', padding: '10px' }}>
                    <div className="video-container">
                      <iframe
                        className="video"
                        src={`https://www.youtube.com/embed/${item.url}`}
                        frameBorder="0"
                        allowFullScreen
                      />
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
