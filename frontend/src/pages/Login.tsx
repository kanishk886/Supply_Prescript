import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Login: React.FC<{ setMode: (m: string) => void }> = ({ setMode }) => {
    const { login } = useAuth();
    const [username, setUsername] = useState('admin@example.com');
    const [password, setPassword] = useState('password123');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const res = await fetch('http://localhost:8000/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData,
            });

            if (res.ok) {
                const data = await res.json();
                login(data.access_token);
            } else {
                setError('Invalid credentials');
            }
        } catch (err) {
            setError('Login failed');
        }
    };

    return (
        <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f3f4f6' }}>
            <div style={{ width: '100%', maxWidth: '400px', padding: '2rem', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
                <h2 style={{ textAlign: 'center', marginBottom: '0.5rem', color: '#1e3a8a' }}>SUPPLY PRESCRIPT</h2>
                <p style={{ textAlign: 'center', color: '#6b7280', marginBottom: '2rem' }}>From Supply Risk to Smarter Decisions.</p>
                {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div>
                        <label>Email</label>
                        <input type="text" value={username} onChange={e => setUsername(e.target.value)} style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem', border: '1px solid #ccc', borderRadius: '4px' }} />
                    </div>
                    <div>
                        <label>Password</label>
                        <input type="password" value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem', border: '1px solid #ccc', borderRadius: '4px' }} />
                    </div>
                    <button type="submit" style={{ padding: '0.75rem', backgroundColor: '#1e3a8a', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Login</button>
                </form>
                <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                    <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>Don't have an account? <button onClick={() => setMode('register')} style={{ background: 'none', border: 'none', color: '#1e3a8a', cursor: 'pointer', textDecoration: 'underline' }}>Register</button></span>
                </div>
            </div>
        </div>
    );
};

export default Login;
