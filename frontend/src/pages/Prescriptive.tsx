import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Prescriptive: React.FC = () => {
    const [status, setStatus] = useState('');
    const [loading, setLoading] = useState(false);
    const [shipment, setShipment] = useState<any>(null);
    const [options, setOptions] = useState<any[]>([]);

    useEffect(() => {
        const stored = localStorage.getItem('selectedShipment');
        if (stored) {
            const s = JSON.parse(stored);
            setShipment(s);
            // Fetch dynamically generated options
            setLoading(true);
            api.post(`/decisions/generate/${s.shipment_id}`)
               .then(res => setOptions(res.data))
               .catch(err => setStatus('Error generating options.'))
               .finally(() => setLoading(false));
        }
    }, []);
    
    const executeDecision = async (prescription_id: number) => {
        setStatus('Executing...');
        try {
            const res = await api.post(`/decisions/execute?prescription_id=${prescription_id}`);
            setStatus(res.data.message);
        } catch (err) {
            setStatus('Failed to execute decision.');
        }
    };

    if (!shipment) return <div><p>Please select a shipment from the Supply Risk page first.</p></div>;

    return (
        <div>
            <h2>Supply Risk Detected</h2>
            <div style={{ backgroundColor: 'white', padding: '1rem', borderRadius: '8px', marginBottom: '2rem', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                <p><strong>Shipment:</strong> {shipment.order_id} | <strong>Product:</strong> {shipment.product} | <strong>Supplier:</strong> {shipment.supplier}</p>
                <p><strong>Current Risk:</strong> <span style={{ color: '#dc2626', fontWeight: 'bold' }}>{shipment.risk} ({shipment.delay_probability}%)</span> | <strong>Predicted Delay:</strong> {Math.round(shipment.predicted_delay)} days</p>
                <p><strong>Inventory Status:</strong> {shipment.inventory < shipment.demand ? 'Critical (Below Demand)' : 'Adequate'}</p>
            </div>

            {status && <div style={{ padding: '1rem', backgroundColor: '#d1fae5', color: '#065f46', marginBottom: '1rem', borderRadius: '4px' }}>{status}</div>}

            {loading ? <p>Generating optimized prescriptions...</p> : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
                    {options.map((opt, idx) => (
                        <div key={opt.id} style={{ backgroundColor: idx === 0 ? '#eff6ff' : 'white', border: idx === 0 ? '2px solid #3b82f6' : '1px solid #e5e7eb', padding: '1.5rem', borderRadius: '8px', position: 'relative', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                            {idx === 0 && <div style={{ position: 'absolute', top: '-12px', right: '1rem', backgroundColor: '#3b82f6', color: 'white', padding: '2px 8px', borderRadius: '12px', fontSize: '0.75rem', fontWeight: 'bold' }}>RECOMMENDED</div>}
                            <h3 style={{ margin: '0 0 1rem 0' }}>{opt.option_name}: {opt.action_type}</h3>
                            <p>Expected Cost: <strong>${Math.round(opt.estimated_cost).toLocaleString()}</strong></p>
                            <p>Expected Delay: <strong>{Math.round(opt.estimated_delay)} days</strong></p>
                            <p>Risk Score: <strong>{(opt.risk_score * 100).toFixed(0)}%</strong></p>
                            <p>Expected Savings: <strong>${Math.round(opt.expected_savings).toLocaleString()}</strong></p>
                            <button onClick={() => executeDecision(opt.id)} style={{ width: '100%', padding: '0.75rem', backgroundColor: idx === 0 ? '#1e3a8a' : '#e5e7eb', color: idx === 0 ? 'white' : '#374151', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold', marginTop: '1rem' }}>Execute Decision</button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Prescriptive;
