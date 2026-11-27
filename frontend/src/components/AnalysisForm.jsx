import { useState } from 'react'

const PAIRS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT']
const TIMEFRAMES = ['15m', '1h', '4h', '1d']

const PORTFOLIO_FIELDS = [
  { key: 'portfolio_value', label: 'Portfolio value', suffix: '$', step: 'any', min: 0.01 },
  { key: 'risk_per_trade_pct', label: 'Risk per trade', suffix: '%', step: 'any', min: 0.01, max: 100 },
  { key: 'stop_loss_pct', label: 'Stop loss', suffix: '%', step: 'any', min: 0.01, max: 100 },
  { key: 'max_exposure_pct', label: 'Max exposure', suffix: '%', step: 'any', min: 0, max: 100 },
  { key: 'current_exposure_pct', label: 'Current exposure', suffix: '%', step: 'any', min: 0, max: 100 },
]

function AnalysisForm({ params, onChange, onSubmit, loading }) {
  const [customPair, setCustomPair] = useState(!PAIRS.includes(params.symbol))
  const set = (key, value) => onChange({ ...params, [key]: value })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!loading) onSubmit()
  }

  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="form-section">
        <div className="section-label">Market</div>

        <label className="field">
          <span>Trading pair</span>
          {customPair ? (
            <input
              value={params.symbol}
              onChange={(e) => set('symbol', e.target.value.toUpperCase())}
              placeholder="e.g. AVAX/USDT"
              autoFocus
            />
          ) : (
            <select value={params.symbol} onChange={(e) => set('symbol', e.target.value)}>
              {PAIRS.map((p) => (
                <option key={p}>{p}</option>
              ))}
            </select>
          )}
          <button
            type="button"
            className="link-btn"
            onClick={() => {
              if (customPair) set('symbol', PAIRS[0])
              setCustomPair(!customPair)
            }}
          >
            {customPair ? 'Choose from list' : 'Enter a custom pair'}
          </button>
        </label>

        <div className="field">
          <span>Timeframe</span>
          <div className="segmented" role="radiogroup" aria-label="Timeframe">
            {TIMEFRAMES.map((tf) => (
              <button
                key={tf}
                type="button"
                role="radio"
                aria-checked={params.timeframe === tf}
                className={params.timeframe === tf ? 'active' : ''}
                onClick={() => set('timeframe', tf)}
              >
                {tf}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="form-section">
        <div className="section-label">Position sizing</div>
        {PORTFOLIO_FIELDS.map(({ key, label, suffix, ...rest }) => (
          <label className="field field-row" key={key}>
            <span>{label}</span>
            <div className="input-affix">
              <input
                type="number"
                value={params[key]}
                onChange={(e) => set(key, e.target.value === '' ? '' : Number(e.target.value))}
                {...rest}
                required
              />
              <em>{suffix}</em>
            </div>
          </label>
        ))}
      </div>

      <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
        {loading ? (
          <>
            <span className="spinner" /> Analyzing…
          </>
        ) : (
          'Run analysis'
        )}
      </button>
    </form>
  )
}

export default AnalysisForm
