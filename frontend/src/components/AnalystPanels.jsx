import { usd, num, tone } from '../format'

function Stat({ label, value, toneOf, mono = true }) {
  return (
    <div className="stat">
      <span className="stat-label">{label}</span>
      <span className={`stat-value ${mono ? 'mono' : ''} ${toneOf ? `t-${tone(toneOf)}` : ''}`}>
        {value ?? '—'}
      </span>
    </div>
  )
}

function Panel({ title, badge, children, note }) {
  return (
    <section className="card panel">
      <header className="panel-head">
        <h3>{title}</h3>
        {badge && <span className={`chip ${tone(badge)}`}>{badge}</span>}
      </header>
      {children}
      {note && <p className="panel-note">{note}</p>}
    </section>
  )
}

function RsiBar({ value }) {
  if (typeof value !== 'number') return null
  return (
    <div className="rsi">
      <div className="rsi-track">
        <div className="rsi-zone" style={{ left: 0, width: '30%' }} />
        <div className="rsi-zone" style={{ left: '70%', width: '30%' }} />
        <div className="gauge-marker" style={{ left: `${Math.max(0, Math.min(100, value))}%` }} />
      </div>
      <div className="gauge-labels">
        <span>Oversold</span>
        <span>Overbought</span>
      </div>
    </div>
  )
}

function AnalystPanels({ result: r }) {
  const exposure = r.portfolio_exposure_after_trade_pct
  return (
    <div className="panel-grid">
      <Panel title="Quantitative" badge={r.quant_trend} note={r.quant_analysis}>
        <div className="stats">
          <Stat label="RSI" value={num(r.quant_rsi, 1)} />
          <Stat label="Momentum" value={r.quant_momentum} toneOf={r.quant_momentum} mono={false} />
          <Stat label="Support" value={usd(r.quant_support)} />
          <Stat label="Resistance" value={usd(r.quant_resistance)} />
          <Stat label="Volatility regime" value={r.quant_volatility_regime} mono={false} />
        </div>
        <RsiBar value={r.quant_rsi} />
      </Panel>

      <Panel title="Risk" badge={r.risk_level} note={r.risk_analysis} />

      <Panel title="News sentiment" badge={r.news_sentiment} note={r.news_analysis}>
        <div className="stats">
          <Stat label="Sentiment score" value={num(r.news_sentiment_score, 2)} toneOf={r.news_sentiment} />
        </div>
      </Panel>

      <Panel title="Position sizing">
        <div className="stats">
          <Stat label="Risk budget" value={usd(r.risk_budget)} />
          <Stat label="Position value" value={usd(r.recommended_position_value)} />
          <Stat label="Units" value={num(r.recommended_position_units, 6)} />
          <Stat label="Est. max loss" value={usd(r.estimated_max_loss)} toneOf={r.estimated_max_loss > 0 ? 'neg' : null} />
          <Stat
            label="Exposure after trade"
            value={typeof exposure === 'number' ? `${num(exposure, 1)}%` : '—'}
          />
          <Stat label="Entry price" value={usd(r.latest_price)} />
        </div>
      </Panel>
    </div>
  )
}

export default AnalystPanels
