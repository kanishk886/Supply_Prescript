import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import api from '../services/api';

const RoiDashboard: React.FC = () => {
    const [roi, setRoi] = useState<any>(null);

    useEffect(() => {
        api.get('/roi').then(res => setRoi(res.data)).catch(err => console.error(err));
    }, []);

    if (!roi) return <p>Loading ROI metrics...</p>;

    const data = [
      { name: 'Expected Cost', value: roi.total_expected_cost },
      { name: 'Actual Cost', value: roi.total_actual_cost },
      { name: 'Savings Gen.', value: roi.total_profit_saved },
    ];

    return (
        <div>
            <h2>Outcome Analytics & ROI</h2>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Decisions Reconciled</h3>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>{roi.total_decisions_reconciled}</p>
                </div>
                <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>Net Value Generated</h3>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#10b981' }}>${Math.round(roi.net_value_generated).toLocaleString()}</p>
                </div>
                <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3 style={{ margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>System ROI</h3>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0.5rem 0 0 0', color: '#1e3a8a' }}>{roi.roi_percentage.toFixed(1)}%</p>
                </div>
            </div>

            <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', height: '400px' }}>
                <h3 style={{ margin: '0 0 1rem 0' }}>Financial Impact Reconciled</h3>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <RechartsTooltip />
                        <Bar dataKey="value" fill="#3b82f6" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default RoiDashboard;
