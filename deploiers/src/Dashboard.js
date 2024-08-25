


import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [data, setData] = useState('Loading...');

  useEffect(() => {
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
  }, []);

  return (
    <div>
      <h1>Dashboard Data</h1>
      <p>{data}</p>
    </div>
  );
}

export default Dashboard;
