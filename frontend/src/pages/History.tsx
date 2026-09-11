import React, { useState, useEffect } from 'react';
import api from '../services/api';

const History: React.FC = () => {
    const [filter, setFilter] = useState('ALL');
    const [history, setHistory] = useState<any[]>([]);

    useEffect(() => {
        api.get('/decisions/').then(res => setHistory(res.data)).catch(err => console.error(err));
    }, []);

    const filtered = filter === 'ALL' ? history : history.filter(h => h.status.includes(filter));

    return (
        <div>
            <h2>Decision History & Outcomes</h2>
            
            <div style={{ marginBottom: '1rem' }}>
                <button onClick={() => setFilter('ALL')} style={{ marginRight: '0.5rem', padding: '0.5rem', cursor: 'pointer' }}>All</button>
                <button onClick={() => setFilter('SUCCESS')} style={{ marginRight: '0.5rem', padding: '0.5rem', cursor: 'pointer' }}>Success</button>
                <button onClick={() => setFilter('DELAYED')} style={{ padding: '0.5rem', cursor: 'pointer' }}>Delayed</button>
            </div>

            <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead style={{ backgroundColor: '#f9fafb', borderBottom: '1px solid #e5e7eb' }}>
                        <tr>
                            <th style={{ padding: '1rem' }}>Date</th>
                            <th style={{ padding: '1rem' }}>Order ID</th>
                            <th style={{ padding: '1rem' }}>Action Taken</th>
                            <th style={{ padding: '1rem' }}>Outcome Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filtered.map(row => (
                            <tr key={row.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                                <td style={{ padding: '1rem' }}>{row.date}</td>
                                <td style={{ padding: '1rem' }}>{row.orderId}</td>
                                <td style={{ padding: '1rem' }}>{row.action}</td>
                                <td style={{ padding: '1rem' }}>
                                    <span style={{ 
                                        padding: '0.25rem 0.5rem', 
                                        borderRadius: '9999px', 
                                        fontSize: '0.75rem',
                                        fontWeight: 'bold',
                                        backgroundColor: row.status === 'SUCCESS' ? '#d1fae5' : row.status === 'DELAYED' ? '#fee2e2' : '#fef3c7',
                                        color: row.status === 'SUCCESS' ? '#065f46' : row.status === 'DELAYED' ? '#991b1b' : '#92400e'
                                    }}>
                                        {row.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div style={{ padding: '1rem', borderTop: '1px solid #e5e7eb', textAlign: 'right', color: '#6b7280', fontSize: '0.875rem' }}>
                    Page 1 of 1 (3 items)
                </div>
            </div>
        </div>
    );
};

export default History;
