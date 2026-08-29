import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Link as LinkIcon } from '@phosphor-icons/react';
import './App.css';

// Pages (to be implemented)
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

function Navigation() {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <nav className="nav-header">
      <Link to="/" className="nav-brand">
        <LinkIcon size={24} weight="bold" color="var(--color-accent)" />
        <span>URL Shorten</span>
      </Link>
      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <Link to="/dashboard" className="btn-secondary">Dashboard</Link>
            <button onClick={handleLogout} className="btn-secondary" style={{ borderColor: 'var(--color-destructive)', color: 'var(--color-destructive)'}}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn-secondary">Login</Link>
            <Link to="/register" className="btn-primary">Get Started</Link>
          </>
        )}
      </div>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
