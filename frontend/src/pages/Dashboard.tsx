import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { Link, QrCode, Copy, Trash, ArrowSquareOut, X } from '@phosphor-icons/react';

interface URLItem {
  id: number;
  original_url: string;
  shorten_url: string;
  count: number;
  access_at: string | null;
  expire_at: string;
}

const Dashboard: React.FC = () => {
  const [urls, setUrls] = useState<URLItem[]>([]);
  const [orgUrl, setOrgUrl] = useState('');
  const [customUrl, setCustomUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [qrModal, setQrModal] = useState<{ isOpen: boolean; short: string | null; qrUrl: string | null }>({
    isOpen: false,
    short: null,
    qrUrl: null,
  });
  
  const navigate = useNavigate();

  useEffect(() => {
    fetchUrls();
  }, []);

  const fetchUrls = async () => {
    try {
      const response = await api.get('/url/');
      setUrls(response.data);
    } catch (err: any) {
      if (err.response?.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      }
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await api.post('/url/', {
        org_url: orgUrl,
        custom_url: customUrl || null
      });
      setOrgUrl('');
      setCustomUrl('');
      fetchUrls();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create URL');
    } finally {
      setIsLoading(false);
    }
  };

  const handleShowQR = async (short: string) => {
    try {
      const response = await api.post(`/url/${short}/qr`, {}, {
        responseType: 'blob'
      });
      const imageUrl = URL.createObjectURL(response.data);
      setQrModal({ isOpen: true, short, qrUrl: imageUrl });
    } catch (err) {
      console.error('Failed to load QR code');
    }
  };

  const closeQrModal = () => {
    if (qrModal.qrUrl) {
      URL.revokeObjectURL(qrModal.qrUrl);
    }
    setQrModal({ isOpen: false, short: null, qrUrl: null });
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // Could add a toast notification here
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-xl)' }}>
        <h2>Dashboard</h2>
      </div>

      {/* Create Form */}
      <div className="card" style={{ marginBottom: 'var(--space-2xl)' }}>
        <h3 style={{ marginBottom: 'var(--space-md)' }}>Create New Link</h3>
        
        {error && (
          <div style={{ 
            padding: 'var(--space-sm) var(--space-md)', 
            background: 'rgba(239, 68, 68, 0.1)', 
            color: 'var(--color-destructive)', 
            border: '1px solid var(--color-destructive)',
            borderRadius: '8px',
            marginBottom: 'var(--space-md)'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleCreate} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: 'var(--space-md)', alignItems: 'end' }}>
          <div>
            <label className="label" htmlFor="orgUrl">Original URL</label>
            <input 
              id="orgUrl"
              type="url" 
              className="input" 
              placeholder="https://example.com/very/long/path" 
              value={orgUrl}
              onChange={(e) => setOrgUrl(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="label" htmlFor="customUrl">Custom Alias (Optional)</label>
            <input 
              id="customUrl"
              type="text" 
              className="input" 
              placeholder="my-campaign" 
              value={customUrl}
              onChange={(e) => setCustomUrl(e.target.value)}
            />
          </div>
          <button type="submit" className="btn-primary" disabled={isLoading} style={{ height: '48px' }}>
            <Link size={20} />
            {isLoading ? 'Shortening...' : 'Shorten'}
          </button>
        </form>
      </div>

      {/* URLs List */}
      <div className="card">
        <h3 style={{ marginBottom: 'var(--space-md)' }}>Your Links</h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
          {urls.length === 0 ? (
            <p style={{ textAlign: 'center', padding: 'var(--space-xl) 0' }}>No links found. Create one above!</p>
          ) : (
            urls.map((url) => {
              const fullShortUrl = `http://localhost:8000/url/${url.shorten_url}`;
              return (
                <div key={url.id} style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  padding: 'var(--space-md)',
                  background: 'var(--color-background)',
                  border: '1px solid var(--color-border)',
                  borderRadius: '8px'
                }}>
                  <div style={{ overflow: 'hidden', flex: 1, marginRight: 'var(--space-md)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)', marginBottom: 'var(--space-xs)', flexWrap: 'wrap' }}>
                      <a href={fullShortUrl} target="_blank" rel="noopener noreferrer" style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
                        {url.shorten_url} <ArrowSquareOut size={16} />
                      </a>
                      <span style={{ fontSize: '0.875rem', color: 'var(--color-muted-foreground)', background: 'var(--color-muted)', padding: '2px 8px', border: '1px solid var(--color-border)', fontWeight: 600 }}>
                        {url.count} clicks
                      </span>
                      {url.expire_at && (
                        <span style={{ fontSize: '0.875rem', color: 'var(--color-muted-foreground)', background: 'var(--color-muted)', padding: '2px 8px', border: '1px solid var(--color-border)', fontWeight: 600 }}>
                          Expires: {new Date(url.expire_at).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                    <p style={{ margin: 0, fontSize: '0.875rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {url.original_url}
                    </p>
                  </div>
                  
                  <div style={{ display: 'flex', gap: 'var(--space-sm)' }}>
                    <button 
                      onClick={() => copyToClipboard(fullShortUrl)}
                      className="btn-secondary" 
                      style={{ padding: '8px', border: '1px solid var(--color-border)' }}
                      title="Copy URL"
                    >
                      <Copy size={20} />
                    </button>
                    <button 
                      onClick={() => handleShowQR(url.shorten_url)}
                      className="btn-secondary" 
                      style={{ padding: '8px', border: '1px solid var(--color-border)' }}
                      title="QR Code"
                    >
                      <QrCode size={20} />
                    </button>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* QR Modal */}
      {qrModal.isOpen && (
        <div className="modal-overlay" onClick={closeQrModal}>
          <div className="modal" onClick={e => e.stopPropagation()} style={{ textAlign: 'center' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
              <h3 style={{ margin: 0 }}>QR Code</h3>
              <button onClick={closeQrModal} style={{ background: 'none', border: 'none', color: 'var(--color-foreground)', cursor: 'pointer' }}>
                <X size={24} />
              </button>
            </div>
            
            {qrModal.qrUrl ? (
              <div>
                <img src={qrModal.qrUrl} alt={`QR Code for ${qrModal.short}`} style={{ maxWidth: '100%', height: 'auto', borderRadius: '8px', marginBottom: 'var(--space-lg)' }} />
                <a 
                  href={qrModal.qrUrl} 
                  download={`qrcode-${qrModal.short}.png`}
                  className="btn-primary"
                  style={{ width: '100%' }}
                >
                  Download PNG
                </a>
              </div>
            ) : (
              <p>Loading...</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
