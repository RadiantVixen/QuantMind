import { useEffect, useState } from 'react'
import AnalysisForm from './components/AnalysisForm'
import PriceChart from './components/PriceChart'
import DecisionCard from './components/DecisionCard'
import ApprovalPanel from './components/ApprovalPanel'
import AnalystPanels from './components/AnalystPanels'
import AuthScreen from './components/AuthScreen'
import { getCurrentUser, getToken, logout, runAnalysis, setUnauthorizedHandler } from './api'

const DEFAULT_PARAMS = {
  symbol: 'BTC/USDT',
  timeframe: '1h',
  portfolio_value: 10000,
  risk_per_trade_pct: 1,
  stop_loss_pct: 2,
  max_exposure_pct: 20,
  current_exposure_pct: 0,
}

const AGENTS = ['Market', 'Risk', 'News', 'Quant']

function Pipeline({ loading, result }) {
  const done = result && !loading
  const approval = result?.approval_required
    ? 'pending'
    : result?.approval_status
      ? 'done'
      : 'idle'

  const step = (label, state) => (
    <li key={label} className={`step step-${state}`}>
      <span className="dot" />
      {label}
    </li>
  )

  return (
    <ol className="pipeline" aria-label="Agent pipeline">
      {AGENTS.map((a) => step(a, loading ? 'running' : done ? 'done' : 'idle'))}
      <li className="sep" />
      {step('Decision', done ? 'done' : 'idle')}
      {step('Sizing', done ? 'done' : 'idle')}
      {step('Approval', loading ? 'idle' : approval)}
    </ol>
  )
}

function App() {
  // undefined = still checking the saved token, null = signed out
  const [user, setUser] = useState(getToken() ? undefined : null)

  useEffect(() => {
    setUnauthorizedHandler(() => setUser(null))
    if (getToken()) {
      getCurrentUser()
        .then(setUser)
        .catch(() => setUser(null))
    }
  }, [])

  if (user === undefined) {
    return (
      <div className="auth-page">
        <span className="spinner lg" />
      </div>
    )
  }

  if (user === null) return <AuthScreen onAuthenticated={setUser} />

  return <Dashboard user={user} onLogout={() => logout().catch(() => {}).finally(() => setUser(null))} />
}

function Dashboard({ user, onLogout }) {
  const [params, setParams] = useState(DEFAULT_PARAMS)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const analyze = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await runAnalysis(params)
      if (data.status === 'FAILED') {
        setResult(null)
        setError(data.error || 'An essential analyst failed.')
      } else {
        setResult(data)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Only overlay support/resistance when the result matches the chart.
  const resultMatchesChart = result && result.symbol === params.symbol

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <div className="logo-mark">Q</div>
          <div>
            <div className="logo">QuantMind</div>
            <div className="muted small">Multi-agent crypto intelligence</div>
          </div>
        </div>
        <AnalysisForm params={params} onChange={setParams} onSubmit={analyze} loading={loading} />
        <div className="user-bar">
          <span className="small">
            Signed in as <strong>{user.username}</strong>
          </span>
          <button type="button" className="link-btn" onClick={onLogout}>
            Sign out
          </button>
        </div>
        <p className="disclaimer">
          Model output is probabilistic and for research only. It is not financial advice.
        </p>
      </aside>

      <main className="main">
        <header className="topbar">
          <h1>Dashboard</h1>
          <Pipeline loading={loading} result={result} />
        </header>

        {error && (
          <div className="alert" role="alert">
            <strong>Analysis failed.</strong> {error}
            <button className="link-btn" onClick={() => setError('')}>
              Dismiss
            </button>
          </div>
        )}

        <PriceChart
          symbol={params.symbol}
          timeframe={params.timeframe}
          support={resultMatchesChart ? result.quant_support : null}
          resistance={resultMatchesChart ? result.quant_resistance : null}
        />

        {loading && !result && (
          <section className="card empty-state">
            <span className="spinner lg" />
            <div>
              <strong>Running the four analysts in parallel…</strong>
              <p className="muted">This can take a little while: it fetches market data, scores the news and runs the model.</p>
            </div>
          </section>
        )}

        {!loading && !result && !error && (
          <section className="card empty-state">
            <div>
              <strong>No analysis yet</strong>
              <p className="muted">
                Pick a pair and timeframe, set your position sizing, then run an analysis. The agents
                will propose a decision for you to approve or reject.
              </p>
            </div>
          </section>
        )}

        {result && (
          <div className={`results ${loading ? 'stale' : ''}`}>
            <ApprovalPanel result={result} onComplete={setResult} />
            <DecisionCard result={result} />
            <AnalystPanels result={result} />

            {result.analyst_errors?.length > 0 && (
              <div className="alert alert-warn">
                <strong>Some analysts reported issues.</strong>
                <ul>
                  {result.analyst_errors.map((e) => (
                    <li key={e}>{e}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.explanation && (
              <details className="card explain">
                <summary>Full decision breakdown</summary>
                <p className="mono small">{result.explanation}</p>
                <p className="muted small">Thread {result.thread_id}</p>
              </details>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
