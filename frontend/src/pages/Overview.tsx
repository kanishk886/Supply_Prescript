import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, LineChart, Line, Legend } from 'recharts';
import api from '../services/api';

const dummyData = [
  { name: 'Low Risk', value: 4000 },
  { name: 'Medium Risk', value: 3000 },
  { name: 'High Risk', value: 1245 },
];

const historicalData = [
  { month: 'Jan', delays: 120 },
  { month: 'Feb', delays: 150 },
  { month: 'Mar', delays: 110 },
  { month: 'Apr', delays: 90 },
  { month: 'May', delays: 210 },
  { month: 'Jun', delays: 180 },
];

const dummyOrders = [
    { id: 'ORD-9921', delay_prob: '87%', predicted_delay: 14, risk: 'High', status: 'Pending Decision' },
    { id: 'ORD-9950', delay_prob: '55%', predicted_delay: 4, risk: 'Medium', status: 'In Review' },
    { id: 'ORD-9965', delay_prob: '12%', predicted_delay: 1, risk: 'Low', status: 'Standard' },
];

const Overview: React.FC = () => {
    const [health, setHealth] = useState('Checking...');
    const [summary, setSummary] = useState<any>({});

    useEffect(() => {
        api.get('/health').then(res => setHealth(res.data.status)).catch(err => setHealth('Error'));
        api.get('/dataset/summary').then(res => setSummary(res.data)).catch(err => console.error(err));
    }, []);

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2 style={{marginTop: 0}}>Supply Chain Overview</h2>
                <span style={{ fontSize: '0.875rem', color: health === 'healthy' ? '#10b981' : '#dc2626' }}>Backend: {health}</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Total Orders</h3>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>{summary.total_shipments || 0}</p>
                </div>
                <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>At-Risk Orders</h3>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#dc2626' }}>{summary.delayed_shipments || 0}</p>
                </div>
                <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Decisions Executed</h3>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#10b981' }}>342</p>
                </div>
                <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Active Model</h3>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>MODEL_V2</p>
                </div>
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '2rem' }}>
                <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', height: '350px' }}>
                    <h3 style={{ margin: '0 0 1rem 0' }}>Risk Distribution</h3>
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={dummyData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <RechartsTooltip />
                            <Bar dataKey="value" fill="#1e3a8a" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
                <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', height: '350px' }}>
                    <h3 style={{ margin: '0 0 1rem 0' }}>Historical Delays</h3>
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={historicalData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="month" />
                            <YAxis />
                            <RechartsTooltip />
                            <Legend />
                            <Line type="monotone" dataKey="delays" stroke="#dc2626" />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>

            <div style={{ marginTop: '2rem', backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                <h3 style={{ margin: '0 0 1rem 0' }}>Order Intelligence (Top Risks)</h3>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead style={{ backgroundColor: '#f9fafb', borderBottom: '1px solid #e5e7eb' }}>
                        <tr>
                            <th style={{ padding: '1rem' }}>Order ID</th>
                            <th style={{ padding: '1rem' }}>Delay Probability</th>
                            <th style={{ padding: '1rem' }}>Predicted Delay (Days)</th>
                            <th style={{ padding: '1rem' }}>Risk Level</th>
                            <th style={{ padding: '1rem' }}>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {dummyOrders.map(row => (
                            <tr key={row.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                                <td style={{ padding: '1rem', fontWeight: 'bold', color: '#1e3a8a' }}>{row.id}</td>
                                <td style={{ padding: '1rem' }}>{row.delay_prob}</td>
                                <td style={{ padding: '1rem' }}>{row.predicted_delay}</td>
                                <td style={{ padding: '1rem' }}>
                                    <span style={{ 
                                        padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold',
                                        backgroundColor: row.risk === 'High' ? '#fee2e2' : row.risk === 'Medium' ? '#fef3c7' : '#d1fae5',
                                        color: row.risk === 'High' ? '#991b1b' : row.risk === 'Medium' ? '#92400e' : '#065f46'
                                    }}>
                                        {row.risk}
                                    </span>
                                </td>
                                <td style={{ padding: '1rem' }}>{row.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Overview;
