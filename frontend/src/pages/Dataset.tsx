import React, { useState, useEffect } from 'react';

const Dataset: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState('');
    const [summary, setSummary] = useState<any>(null);

    const fetchSummary = async () => {
        try {
            const res = await fetch('http://localhost:8000/api/dataset/summary');
            if (res.ok) {
                const data = await res.json();
                setSummary(data);
            }
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        fetchSummary();
    }, []);

    const handleUpload = async () => {
        if (!file) return;
        setUploading(true);
        setMessage('');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('http://localhost:8000/api/dataset/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (res.ok) {
                setMessage(data.message);
                fetchSummary();
            } else {
                setMessage(data.detail || 'Upload failed');
            }
        } catch (e) {
            setMessage('Network error during upload');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div>
            <h2>Dataset Management</h2>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3>Upload Historical Dataset</h3>
                    <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>Upload a CSV file containing historical shipment records to train the models and power the optimization engine.</p>
                    
                    <div style={{ marginTop: '1rem', padding: '2rem', border: '2px dashed #d1d5db', borderRadius: '8px', textAlign: 'center' }}>
                        <input type="file" accept=".csv" onChange={e => setFile(e.target.files ? e.target.files[0] : null)} />
                        {file && <p style={{ marginTop: '1rem' }}>Selected: {file.name}</p>}
                    </div>
                    
                    <button 
                        onClick={handleUpload} 
                        disabled={!file || uploading}
                        style={{ marginTop: '1rem', width: '100%', padding: '0.75rem', backgroundColor: '#1e3a8a', color: 'white', border: 'none', borderRadius: '4px', cursor: (file && !uploading) ? 'pointer' : 'not-allowed', opacity: (file && !uploading) ? 1 : 0.5 }}
                    >
                        {uploading ? 'Uploading and Processing...' : 'Run Analysis'}
                    </button>
                    {message && <p style={{ marginTop: '1rem', color: message.includes('cleared') || message.includes('Success') ? '#10b981' : '#dc2626' }}>{message}</p>}

                    <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid #e5e7eb' }}>
                        <h4 style={{ color: '#dc2626', margin: '0 0 0.5rem 0' }}>Danger Zone</h4>
                        <button 
                            onClick={async () => {
                                if (window.confirm('Are you sure you want to delete all shipments, predictions, and decisions?')) {
                                    setUploading(true);
                                    try {
                                        const res = await fetch('http://localhost:8000/api/dataset/clear', { method: 'DELETE' });
                                        if (res.ok) {
                                            setMessage('All dataset records have been cleared.');
                                            fetchSummary();
                                            setFile(null);
                                        }
                                    } finally {
                                        setUploading(false);
                                    }
                                }
                            }}
                            disabled={uploading}
                            style={{ width: '100%', padding: '0.75rem', backgroundColor: 'transparent', color: '#dc2626', border: '1px solid #dc2626', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}
                        >
                            Clear All Data
                        </button>
                    </div>
                </div>

                <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                    <h3>Database Summary</h3>
                    {summary ? (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: '0.5rem', borderBottom: '1px solid #e5e7eb' }}>
                                <span style={{ color: '#4b5563' }}>Total Shipments Loaded</span>
                                <span style={{ fontWeight: 'bold' }}>{summary.total_shipments}</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: '0.5rem', borderBottom: '1px solid #e5e7eb' }}>
                                <span style={{ color: '#4b5563' }}>Delayed Shipments</span>
                                <span style={{ fontWeight: 'bold' }}>{summary.delayed_shipments}</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: '0.5rem', borderBottom: '1px solid #e5e7eb' }}>
                                <span style={{ color: '#4b5563' }}>Historical On-Time Rate</span>
                                <span style={{ fontWeight: 'bold' }}>{summary.on_time_rate.toFixed(1)}%</span>
                            </div>
                        </div>
                    ) : (
                        <p>Loading summary...</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dataset;
