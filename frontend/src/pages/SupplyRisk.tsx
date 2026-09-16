import React, { useState, useEffect } from 'react';
import api from '../services/api';

const SupplyRisk: React.FC<{ setView: (v: string) => void }> = ({ setView }) => {
    const [risks, setRisks] = useState<any[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    useEffect(() => {
        api.get('/predictions/risks').then(res => setRisks(res.data)).catch(err => console.error(err));
    }, []);

    // Filter by search term
    const filteredRisks = risks.filter(r => 
        (r.order_id && r.order_id.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (r.product && r.product.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (r.supplier && r.supplier.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    // Pagination logic
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = filteredRisks.slice(indexOfFirstItem, indexOfLastItem);
    const totalPages = Math.ceil(filteredRisks.length / itemsPerPage);

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 style={{ margin: 0 }}>Supply Risk</h2>
                <input 
                    type="text" 
                    placeholder="Search orders, products..." 
                    value={searchTerm}
                    onChange={(e) => {
                        setSearchTerm(e.target.value);
                        setCurrentPage(1); // Reset to page 1 on search
                    }}
                    style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #d1d5db', width: '300px' }}
                />
            </div>

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
                            {currentItems.map(r => (
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
                    
                    {/* Pagination Controls */}
                    {totalPages > 1 && (
                        <div style={{ padding: '1rem', borderTop: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                                Showing {indexOfFirstItem + 1} to {Math.min(indexOfLastItem, filteredRisks.length)} of {filteredRisks.length} results
                            </span>
                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                <button 
                                    disabled={currentPage === 1}
                                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                    style={{ padding: '0.25rem 0.75rem', border: '1px solid #d1d5db', borderRadius: '4px', backgroundColor: currentPage === 1 ? '#f3f4f6' : 'white', cursor: currentPage === 1 ? 'not-allowed' : 'pointer' }}
                                >
                                    Previous
                                </button>
                                <button 
                                    disabled={currentPage === totalPages}
                                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                                    style={{ padding: '0.25rem 0.75rem', border: '1px solid #d1d5db', borderRadius: '4px', backgroundColor: currentPage === totalPages ? '#f3f4f6' : 'white', cursor: currentPage === totalPages ? 'not-allowed' : 'pointer' }}
                                >
                                    Next
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default SupplyRisk;
