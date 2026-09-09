import React, { useState, useEffect } from 'react';
import api from '../services/api';

const SupplyRisk: React.FC<{ setView: (v: string) => void }> = ({ setView }) => {
    const [risks, setRisks] = useState<any[]>([]);

    useEffect(() => {
        api.get('/predictions/risks').then(res => setRisks(res.data)).catch(err => console.error(err));
    }, []);

    return (
        <div>
            <h2>Supply Risk</h2>
            {risks.length === 0 ? (
                <p>No risks detected yet. Upload a dataset and run predictions.</p>
            ) : (
                <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflow: 'hidden' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead style={{ backgroundColor: '#f9fafb', borderBottom: '1px solid #e5e7eb' }}>
                            <tr>
                                <th style={{ padding: '1rem' }}>Order ID</th>
                                <th style={{ padding: '1rem' }}>Product</th>
                                <th style={{ padding: '1rem' }}>Supplier</th>
                                <th style={{ padding: '1rem' }}>Predicted Delay</th>
                                <th style={{ padding: '1rem' }}>Probability</th>
                                <th style={{ padding: '1rem' }}>Risk Level</th>
                                <th style={{ padding: '1rem' }}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {risks.map(r => (
                                <tr key={r.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                                    <td style={{ padding: '1rem' }}>{r.order_id}</td>
                                    <td style={{ padding: '1rem' }}>{r.product}</td>
                                    <td style={{ padding: '1rem' }}>{r.supplier}</td>
                                    <td style={{ padding: '1rem' }}>{Math.round(r.predicted_delay)} days</td>
                                    <td style={{ padding: '1rem' }}>{r.delay_probability}%</td>
                                    <td style={{ padding: '1rem' }}>
                                        <span style={{ 
                                            padding: '0.25rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold',
                                            backgroundColor: r.risk === 'High' ? '#fee2e2' : r.risk === 'Medium' ? '#fef3c7' : '#d1fae5',
                                            color: r.risk === 'High' ? '#991b1b' : r.risk === 'Medium' ? '#92400e' : '#065f46'
                                        }}>
                                            {r.risk}
                                        </span>
                                    </td>
                                    <td style={{ padding: '1rem' }}>
                                        <button 
                                            onClick={() => {
                                                localStorage.setItem('selectedShipment', JSON.stringify(r));
                                                setView('prescriptive');
                                            }}
                                            style={{ padding: '0.5rem 1rem', backgroundColor: '#1e3a8a', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                                        >
                                            View Prescriptions
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default SupplyRisk;
