import React, { useState } from 'react';
import axios from 'axios';

function SignUp() {
    const [formData, setFormData] = useState({
        nickname: '',
        email: '',
        password: ''
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/listener/signUp/', formData);
            // 회원가입 성공 메시지를 alert로 표시
            alert(`Signup successful: ${response.data.message}`);
            // 회원가입 성공 후 홈페이지로 리디렉션
            window.location.href = '/';
        } catch (error) {
            // 에러 메시지를 alert로 표시
            if (error.response) {
                alert(`Signup failed: ${error.response.data.detail || 'Unknown error'}`);
            } else {
                alert('Signup failed: Network error or server not responding');
            }
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Sign Up</h2>
            <div>
                <label>Nickname</label>
                <input
                    type="text"
                    name="nickname"
                    value={formData.nickname}
                    onChange={handleChange}
                    required
                />
            </div>
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
            <button type="submit">Sign Up</button>
        </form>
    );
}

export default SignUp;
