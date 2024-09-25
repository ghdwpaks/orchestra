import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // 페이지 이동을 위한 useNavigate 훅 사용

function ChangePassword() {
  const [formData, setFormData] = useState({
    //email: localStorage.getItem('userEmail'),
    //code: localStorage.getItem('userCode'),  // 6자리 코드도 로컬 스토리지에서 가져온다고 가정
    email: "hjm7904@gmail.com",
    code: "jp61Tn",  // 6자리 코드도 로컬 스토리지에서 가져온다고 가정
    password: '',
    confirmPassword: ''
  });
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();  // 페이지 이동을 위한 훅

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setErrorMessage('비밀번호가 일치하지 않습니다.');
      return;
    }

    if (formData.password.length < 6) {
      setErrorMessage('비밀번호는 최소 6글자 이상이어야 합니다.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/listener/change_password/', {
        email: formData.email,
        code: formData.code,
        password: formData.password
      });
      if (response.status === 200) {
        // 비밀번호 변경 성공 시
        navigate('/login');  // 비밀번호 변경 후 로그인 페이지로 이동
      }
    } catch (error) {
      setErrorMessage('비밀번호 변경 중 오류가 발생했습니다.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>비밀번호 변경</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <div>
        <label>새 비밀번호</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>비밀번호 확인</label>
        <input
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit" disabled={formData.password !== formData.confirmPassword}>
        비밀번호 변경
      </button>
    </form>
  );
}

export default ChangePassword;
