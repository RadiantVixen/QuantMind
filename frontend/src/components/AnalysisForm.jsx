import { useState } from 'react'
import api from '../api'

function AnalysisForm({ onResult, onLoading }) {
  const [symbol, setSymbol] = useState('BTC/USDT')
  const [timeframe, setTimeframe] = useState('1h')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    onLoading(true)

    try {
      const response = await api.post('/analysis/', {
        symbol,
        timeframe,
      })
      onResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed.')
    } finally {
      onLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Market Analysis</h2>

      <label>Trading Pair</label>
      <input
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
      />

      <label>Timeframe</label>
      <select
        value={timeframe}
        onChange={(e) => setTimeframe(e.target.value)}
      >
        <option value="15m">15 minutes</option>
        <option value="1h">1 hour</option>
        <option value="4h">4 hours</option>
        <option value="1d">1 day</option>
      </select>

      <button type="submit">Run Analysis</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  )
}

export default AnalysisForm

