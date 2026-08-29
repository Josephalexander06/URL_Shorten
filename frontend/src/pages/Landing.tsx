import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Link as LinkIcon, Lightning, ShieldCheck, ChartLineUp } from '@phosphor-icons/react';

const Landing: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem('token')) {
      navigate('/dashboard');
    }
  }, [navigate]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3xl)', paddingTop: 'var(--space-xl)' }}>
      {/* Hero Section */}
      <section style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: 'var(--space-md)' }}>
          Short links, <span style={{ color: 'var(--color-accent)' }}>big results.</span>
        </h1>
        <p style={{ fontSize: '1.25rem', marginBottom: 'var(--space-xl)' }}>
          A powerful, minimal, and fast URL shortener designed for developers and modern teams.
        </p>
        <div style={{ display: 'flex', gap: 'var(--space-md)', justifyContent: 'center' }}>
          <Link to="/register" className="btn-primary" style={{ padding: '16px 32px', fontSize: '1.1rem' }}>
            Get Started for Free
          </Link>
          <Link to="/login" className="btn-secondary" style={{ padding: '16px 32px', fontSize: '1.1rem' }}>
            Sign In
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: 'var(--space-xl)',
        marginTop: 'var(--space-2xl)'
      }}>
        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
          <div style={{ background: 'var(--color-primary)', padding: 'var(--space-sm)', borderRadius: '8px', marginBottom: 'var(--space-md)' }}>
            <Lightning size={32} color="var(--color-accent)" />
          </div>
          <h3>Lightning Fast</h3>
          <p>Powered by FastAPI and Redis caching, redirects happen in milliseconds.</p>
        </div>
        
        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
          <div style={{ background: 'var(--color-primary)', padding: 'var(--space-sm)', borderRadius: '8px', marginBottom: 'var(--space-md)' }}>
            <ShieldCheck size={32} color="var(--color-accent)" />
          </div>
          <h3>Custom Aliases</h3>
          <p>Create branded, memorable links instead of random characters.</p>
        </div>

        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
          <div style={{ background: 'var(--color-primary)', padding: 'var(--space-sm)', borderRadius: '8px', marginBottom: 'var(--space-md)' }}>
            <ChartLineUp size={32} color="var(--color-accent)" />
          </div>
          <h3>Basic Analytics</h3>
          <p>Track how many times your links have been clicked instantly.</p>
        </div>
      </section>
    </div>
  );
};

export default Landing;
