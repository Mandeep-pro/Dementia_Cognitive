import React from 'react';
import { Sprout, RotateCcw } from 'lucide-react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('SmritiRoots ErrorBoundary caught an unhandled error:', error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReload = () => {
    window.location.reload();
  };

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          backgroundColor: '#f8fafc',
          fontFamily: 'system-ui, -apple-system, sans-serif',
          color: '#1e293b'
        }}>
          <div style={{
            maxWidth: '480px',
            width: '100%',
            backgroundColor: '#ffffff',
            borderRadius: '20px',
            padding: '32px',
            boxShadow: '0 20px 40px -15px rgba(0, 0, 0, 0.08)',
            textAlign: 'center',
            border: '1px solid #e2e8f0'
          }}>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '16px' }}>
              <Sprout size={48} color="#0d9488" />
            </div>
            <h2 style={{ fontSize: '22px', fontWeight: '700', marginBottom: '8px', color: '#0f172a' }}>
              Something gentle went off track
            </h2>
            <p style={{ fontSize: '15px', color: '#64748b', lineHeight: '1.6', marginBottom: '24px' }}>
              The application encountered an unexpected issue, but your data is safe. You can reload the view or return to the main dashboard.
            </p>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', marginBottom: '20px' }}>
              <button
                onClick={this.handleReset}
                style={{
                  padding: '12px 20px',
                  backgroundColor: '#f1f5f9',
                  color: '#334155',
                  border: 'none',
                  borderRadius: '12px',
                  fontWeight: '600',
                  fontSize: '14px',
                  cursor: 'pointer'
                }}
              >
                Try Again
              </button>
              <button
                onClick={this.handleReload}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '12px 24px',
                  backgroundColor: '#0d9488',
                  color: '#ffffff',
                  border: 'none',
                  borderRadius: '12px',
                  fontWeight: '600',
                  fontSize: '14px',
                  cursor: 'pointer',
                  boxShadow: '0 4px 12px rgba(13, 148, 136, 0.25)'
                }}
              >
                <span>Reload Page</span>
                <RotateCcw size={15} />
              </button>
            </div>

            {this.state.error && (
              <details style={{ textAlign: 'left', marginTop: '16px', fontSize: '12px', color: '#94a3b8' }}>
                <summary style={{ cursor: 'pointer', marginBottom: '8px' }}>Technical diagnostic details</summary>
                <div style={{
                  padding: '12px',
                  backgroundColor: '#f8fafc',
                  borderRadius: '8px',
                  overflowX: 'auto',
                  fontFamily: 'monospace',
                  color: '#e11d48'
                }}>
                  {this.state.error.toString()}
                </div>
              </details>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
