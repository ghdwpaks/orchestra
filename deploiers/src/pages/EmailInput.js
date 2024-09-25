import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // 페이지 이동을 위해 useNavigate 사용

function EmailInput() {
  const [formData, setFormData] = useState({ email: '' });
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();  // 페이지 이동을 위한 훅

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/listener/send_email/', formData);
      if (response.status === 200) {
        // 이메일을 세션에 저장
        sessionStorage.setItem('userEmail', formData.email);

        // 성공 메시지 설정
        setSuccessMessage('이메일 전송이 완료되었습니다.');
        setErrorMessage('');

        // '/emailcodeinput' 페이지로 이동
        navigate('/emailcodeinput');
      }
    } catch (error) {
      setErrorMessage('이메일 전송 중 오류가 발생했습니다.');
      setSuccessMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>이메일 입력</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      <div>
        <label>Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">전송</button>
    </form>
  );
}

export default EmailInput;
