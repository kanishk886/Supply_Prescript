import React, { useState } from 'react';
import api from '../services/api';

const ChatWidget: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState<{sender: 'user'|'bot', text: string}[]>([{sender: 'bot', text: 'Hi! Ask me about ROI, risk, or decisions.'}]);

    const handleSend = async () => {
        if (!query.trim()) return;
        
        const newMsgs = [...messages, {sender: 'user' as const, text: query}];
        setMessages(newMsgs);
        setQuery('');

        try {
            const res = await api.post('/chat/query', { query });
            setMessages([...newMsgs, {sender: 'bot', text: res.data.answer}]);
        } catch (e) {
            setMessages([...newMsgs, {sender: 'bot', text: 'Error connecting to assistant.'}]);
        }
    };

    return (
        <div style={{ position: 'fixed', bottom: '2rem', right: '2rem', zIndex: 50 }}>
            {isOpen ? (
                <div style={{ width: '300px', height: '400px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.15)', display: 'flex', flexDirection: 'column' }}>
                    <div style={{ backgroundColor: '#1e3a8a', color: 'white', padding: '1rem', borderTopLeftRadius: '8px', borderTopRightRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontWeight: 'bold' }}>SupplyPrescript Assistant</span>
                        <button onClick={() => setIsOpen(false)} style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer', fontSize: '1rem' }}>×</button>
                    </div>
                    <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        {messages.map((m, i) => (
                            <div key={i} style={{ alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start', backgroundColor: m.sender === 'user' ? '#dbeafe' : '#f3f4f6', padding: '0.5rem 0.75rem', borderRadius: '8px', maxWidth: '80%' }}>
                                <p style={{ margin: 0, fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}>{m.text}</p>
                            </div>
                        ))}
                    </div>
                    <div style={{ padding: '0.75rem', borderTop: '1px solid #e5e7eb', display: 'flex', gap: '0.5rem' }}>
                        <input 
                            value={query} 
                            onChange={e => setQuery(e.target.value)} 
                            onKeyPress={e => e.key === 'Enter' && handleSend()}
                            placeholder="Ask a question..."
                            style={{ flex: 1, padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '4px' }}
                        />
                        <button onClick={handleSend} style={{ padding: '0.5rem 1rem', backgroundColor: '#1e3a8a', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Send</button>
                    </div>
                </div>
            ) : (
                <button 
                    onClick={() => setIsOpen(true)}
                    style={{ backgroundColor: '#1e3a8a', color: 'white', border: 'none', borderRadius: '50%', width: '60px', height: '60px', cursor: 'pointer', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', fontSize: '1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                >
                    💬
                </button>
            )}
        </div>
    );
};

export default ChatWidget;
