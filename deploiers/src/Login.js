import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // React Router에서 useNavigate 훅을 임포트

function Login() {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [errorMessage, setErrorMessage] = useState(''); // 로그인 실패 메시지를 저장할 상태
    const navigate = useNavigate(); // 네비게이션 함수 사용
    const [csrfToken, setCsrfToken] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log("enterd event");
            const response = await axios.post('http://127.0.0.1:8000/listener/login/', formData);
            console.log("Login successful:", response.data);
            setCsrfToken(response.data.csrfToken); // 서버로부터 받은 CSRF 토큰 저장
            console.log("response.data.csrfToken :",response.data.csrfToken)
            sessionStorage.setItem('csrfToken', response.data.csrfToken); // 세션 스토리지에 CSRF 토큰 저장
            navigate('/'); // 로그인 성공 시 홈 페이지로 리디렉션
        } catch (error) {
            console.error('Login error:', error.response);
            setErrorMessage('Login failed: ' + (error.response?.data?.detail || 'Unexpected error')); // 오류 메시지 설정
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Login</h2>
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>} {/* 오류 메시지 표시 */}
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
            <div>
                <label>Password</label>
                <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />
            </div>
            <button type="submit">Login</button>
        </form>
    );
}

export default Login;
