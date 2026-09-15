import React, { useState } from 'react';
import DashboardLayout from './layouts/DashboardLayout';
import Overview from './pages/Overview';
import Dataset from './pages/Dataset';
import SupplyRisk from './pages/SupplyRisk';
import Prescriptive from './pages/Prescriptive';
import History from './pages/History';
import RoiDashboard from './pages/RoiDashboard';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import { AuthProvider, useAuth } from './context/AuthContext';

function AppContent() {
  const [view, setView] = useState('overview');
  const [authMode, setAuthMode] = useState('login');
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return authMode === 'login' ? <Login setMode={setAuthMode} /> : <Register setMode={setAuthMode} />;
  }

  return (
    <DashboardLayout setView={setView} currentView={view}>
      {view === 'overview' && <Overview setView={setView} />}
      {view === 'dataset' && <Dataset />}
      {view === 'risk' && <SupplyRisk setView={setView} />}
      {view === 'prescriptive' && <Prescriptive />}
      {view === 'history' && <History />}
      {view === 'roi' && <RoiDashboard />}
      {view === 'profile' && <Profile />}
    </DashboardLayout>
  );
}

function App() {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
}

export default App;
