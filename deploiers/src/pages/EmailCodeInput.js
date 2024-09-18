import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // 페이지 이동을 위한 useNavigate 훅 사용

function EmailCodeInput() {
  const [formData, setFormData] = useState({
    email: localStorage.getItem('userEmail'), // 로컬 스토리지에서 이메일 가져옴
    code: ''
  });
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();  // 페이지 이동을 위한 훅

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value  // 코드 입력값 업데이트
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (formData.code.length !== 6) {
      setErrorMessage('코드는 6글자여야 합니다.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/listener/confirm_email/', formData);
      if (response.status === 200) {
        // 성공하면 change_password 페이지로 이동
        navigate('/changepassword');
      }
    } catch (error) {
      setErrorMessage('코드 확인 중 오류가 발생했습니다.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>코드 입력</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <div>
        <label>코드</label>
        <input
          type="text"
          name="code"
          value={formData.code}  // formData에서 코드 값을 가져옴
          onChange={handleChange}
          maxLength={6}
          required
        />
      </div>
      <button type="submit">확인</button>
    </form>
  );
}

export default EmailCodeInput;
