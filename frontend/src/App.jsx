import { useState } from 'react'
import AnalysisForm from './components/AnalysisForm'
import ApprovalPanel from './components/ApprovalPanel'
import AnalysisResults from './components/AnalysisResults'
import './index.css'

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <main className="app">
      <header className="header">
        <div>
          <div className="logo">QUANTMIND</div>
          <p className="subtitle">AI-powered crypto intelligence</p>
        </div>
        <span className="muted">MVP · v1.0</span>
      </header>

      <section className="panel">
        <AnalysisForm
          onResult={setResult}
          onLoading={setLoading}
        />
        {loading && <p className="muted">Analyzing market...</p>}
      </section>

      {result && (
        <>
          <ApprovalPanel result={result} onComplete={setResult} />
          <AnalysisResults result={result} />
        </>
      )}
    </main>
  )
}

export default App