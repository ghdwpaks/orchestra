import React, { useState } from 'react';
import axios from 'axios';

function SignUp() {
    const [formData, setFormData] = useState({
        id: '',
        nickname: '',
        email: '',
        password: '',
        confirmPassword: ''
    });

    const [errorMessage, setErrorMessage] = useState('');
    const [isButtonDisabled, setIsButtonDisabled] = useState(true);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });

        if (formData.password !== formData.confirmPassword) {
            setErrorMessage('비밀번호가 일치하지 않습니다.');
            setIsButtonDisabled(true);
        } else {
            setErrorMessage('');
            setIsButtonDisabled(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (formData.password !== formData.confirmPassword) {
            setErrorMessage('비밀번호가 일치하지 않습니다.');
            return;
        }
        try {
            const response = await axios.post('http://127.0.0.1:8000/listener/signUp/', formData);
            alert(`Signup successful: ${response.data.message}`);
            window.location.href = '/';
        } catch (error) {
            if (error.response) {
                alert(`Signup failed: ${error.response.data.detail || 'Unknown error'}`);
            } else {
                alert('Signup failed: Network error or server not responding');
            }
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: '0', paddingLeft: '20px' }}>
            <h2>Sign Up</h2>
            <div style={{ marginBottom: '10px' }}>
                <label>ID</label>
                <input
                    type="text"
                    name="id"
                    value={formData.id}
                    onChange={handleChange}
                    required
                    style={{ width: '100%' }}
                />
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Nickname</label>
                <input
                    type="text"
                    name="nickname"
                    value={formData.nickname}
                    onChange={handleChange}
                    required
                    style={{ width: '100%' }}
                />
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Email</label>
                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    style={{ width: '100%' }}
                />
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Password</label>
                <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    style={{ width: '100%' }}
                />
            </div>
            <div style={{ marginBottom: '10px' }}>
                <label>Confirm Password</label>
                <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                    style={{ width: '100%' }}
                />
            </div>
            {errorMessage && <p style={{ color: 'red', marginBottom: '10px' }}>{errorMessage}</p>}
            <button type="submit" disabled={isButtonDisabled} style={{ width: '100%' }}>
                Sign Up
            </button>
        </form>
    );
}

export default SignUp;
