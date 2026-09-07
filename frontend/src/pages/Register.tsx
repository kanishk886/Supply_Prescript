import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Register: React.FC<{ setMode: (m: string) => void }> = ({ setMode }) => {
    const { login } = useAuth();
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirm, setConfirm] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (password !== confirm) {
            setError("Passwords don't match");
            return;
        }

        try {
            const res = await fetch('http://localhost:8000/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password }),
            });

            if (res.ok) {
                // Auto-login after register
                const loginFormData = new URLSearchParams();
                loginFormData.append('username', email);
                loginFormData.append('password', password);

                const loginRes = await fetch('http://localhost:8000/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: loginFormData,
                });
                
                if (loginRes.ok) {
                    const data = await loginRes.json();
                    login(data.access_token);
                }
            } else {
                const data = await res.json();
                setError(data.detail || 'Registration failed');
            }
        } catch (err) {
            setError('An error occurred');
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
                        <label>Name</label>
                        <input required type="text" value={name} onChange={e => setName(e.target.value)} style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem', border: '1px solid #ccc', borderRadius: '4px' }} />
                    </div>
                    <div>
                        <label>Email</label>
                        <input required type="email" value={email} onChange={e => setEmail(e.target.value)} style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem', border: '1px solid #ccc', borderRadius: '4px' }} />
                    </div>
                    <div>
                        <label>Password</label>
                        <input required type="password" value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem', border: '1px solid #ccc', borderRadius: '4px' }} />
                    </div>
                    <div>
                        <label>Confirm Password</label>
                        <input required type="password" value={confirm} onChange={e => setConfirm(e.target.value)} style={{ width: '100%', padding: '0.5rem', marginTop: '0.25rem', border: '1px solid #ccc', borderRadius: '4px' }} />
                    </div>
                    <button type="submit" style={{ padding: '0.75rem', backgroundColor: '#1e3a8a', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Register</button>
                </form>
                <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                    <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>Already have an account? <button onClick={() => setMode('login')} style={{ background: 'none', border: 'none', color: '#1e3a8a', cursor: 'pointer', textDecoration: 'underline' }}>Login</button></span>
                </div>
            </div>
        </div>
    );
};

export default Register;
