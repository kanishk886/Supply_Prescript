import React from 'react';
import { useAuth } from '../context/AuthContext';
import ChatWidget from '../components/ChatWidget';

const DashboardLayout: React.FC<{children: React.ReactNode, setView: (v: string) => void, currentView: string}> = ({ children, setView, currentView }) => {
  const { logout } = useAuth();
  
  const navItems = [
      { id: 'overview', label: 'Overview' },
      { id: 'dataset', label: 'Dataset' },
      { id: 'risk', label: 'Supply Risk' },
      { id: 'prescriptive', label: 'Prescriptions' },
      { id: 'history', label: 'Decisions' },
      { id: 'roi', label: 'Outcome Analytics' },
      { id: 'profile', label: 'User Profile' },
  ];

  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      {/* Sidebar */}
      <aside style={{ width: '250px', backgroundColor: '#1e3a8a', color: 'white', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '1.5rem', borderBottom: '1px solid #3b82f6' }}>
            <h1 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 'bold' }}>SUPPLY PRESCRIPT</h1>
            <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.75rem', color: '#bfdbfe' }}>Closed-Loop Analytics</p>
        </div>
        
        <nav style={{ flex: 1, padding: '1rem 0', display: 'flex', flexDirection: 'column' }}>
            {navItems.map(item => (
                <button 
                    key={item.id}
                    onClick={() => setView(item.id)}
                    style={{
                        padding: '0.75rem 1.5rem',
                        textAlign: 'left',
                        background: currentView === item.id ? '#1e40af' : 'transparent',
                        border: 'none',
                        color: 'white',
                        cursor: 'pointer',
                        fontSize: '0.875rem',
                        fontWeight: currentView === item.id ? 'bold' : 'normal',
                        borderLeft: currentView === item.id ? '4px solid #60a5fa' : '4px solid transparent'
                    }}
                >
                    {item.label}
                </button>
            ))}
        </nav>
        
        <div style={{ padding: '1.5rem', borderTop: '1px solid #3b82f6' }}>
            <button onClick={logout} style={{ width: '100%', padding: '0.5rem', backgroundColor: '#dc2626', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.875rem' }}>Logout</button>
        </div>
      </aside>

      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', position: 'relative' }}>
          <header style={{ backgroundColor: 'white', padding: '1rem 2rem', borderBottom: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h2 style={{ margin: 0, fontSize: '1.25rem', color: '#111827' }}>
                  {navItems.find(i => i.id === currentView)?.label || 'Dashboard'}
              </h2>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>System Status: <span style={{ color: '#10b981', fontWeight: 'bold' }}>Online</span></span>
              </div>
          </header>
          
          <main style={{ flex: 1, padding: '2rem', overflowY: 'auto' }}>
            {children}
          </main>
          <ChatWidget />
      </div>
    </div>
  );
};

export default DashboardLayout;
