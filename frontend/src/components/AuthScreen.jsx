import { useState } from 'react'
import { login, register } from '../api'

function AuthScreen({ onAuthenticated }) {
  const [mode, setMode] = useState('login') // 'login' | 'register'
  const [form, setForm] = useState({ username: '', email: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const isLogin = mode === 'login'
  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const user = isLogin
        ? await login(form.username, form.password)
        : await register(form.username, form.email, form.password)
      onAuthenticated(user)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const switchMode = () => {
    setMode(isLogin ? 'register' : 'login')
    setError('')
  }

  return (
    <div className="auth-page">
      <section className="card auth-card">
        <div className="brand">
          <div className="logo-mark">Q</div>
          <div>
            <div className="logo">QuantMind</div>
            <div className="muted small">Multi-agent crypto intelligence</div>
          </div>
        </div>

        <h1 className="auth-title">{isLogin ? 'Sign in' : 'Create an account'}</h1>

        <form className="form" onSubmit={handleSubmit}>
          <div className="form-section">
            <label className="field">
              <span>Username</span>
              <input
                value={form.username}
                onChange={set('username')}
                autoComplete="username"
                autoFocus
                required
              />
            </label>

            {!isLogin && (
              <label className="field">
                <span>Email (optional)</span>
                <input type="email" value={form.email} onChange={set('email')} autoComplete="email" />
              </label>
            )}

            <label className="field">
              <span>Password</span>
              <input
                type="password"
                value={form.password}
                onChange={set('password')}
                autoComplete={isLogin ? 'current-password' : 'new-password'}
                minLength={isLogin ? undefined : 8}
                required
              />
            </label>
          </div>

          {error && (
            <p className="error-text" role="alert">
              {error}
            </p>
          )}

          <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
            {loading ? <span className="spinner" /> : isLogin ? 'Sign in' : 'Create account'}
          </button>
        </form>

        <p className="muted small auth-switch">
          {isLogin ? "Don't have an account?" : 'Already have an account?'}{' '}
          <button type="button" className="link-btn" onClick={switchMode}>
            {isLogin ? 'Create one' : 'Sign in'}
          </button>
        </p>
      </section>
    </div>
  )
}

export default AuthScreen
