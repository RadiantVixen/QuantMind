import { pct, signed, tone } from '../format'

// decision_score lives in [-1, 1]; BUY at >= 0.25, AVOID at <= -0.25.
const THRESHOLD = 0.25
const toPos = (v) => `${((Math.max(-1, Math.min(1, v)) + 1) / 2) * 100}%`

function DecisionCard({ result }) {
  const score = result.decision_score ?? 0
  const up = result.probability_up ?? 0
  const down = result.probability_down ?? 1 - up

  return (
    <section className={`card decision-card tone-${tone(result.decision)}`}>
      <div className="decision-main">
        <div className="eyebrow">Final decision</div>
        <div className="decision-label">{result.decision ?? '—'}</div>
        <div className="chips">
          <span className={`chip ${tone(result.analyst_agreement)}`}>
            Agreement: {result.analyst_agreement ?? '—'}
          </span>
          <span className={`chip ${tone(result.risk_level)}`}>Risk: {result.risk_level ?? '—'}</span>
          {result.approval_status && (
            <span className={`chip ${tone(result.approval_status)}`}>{result.approval_status}</span>
          )}
        </div>
      </div>

      <div className="decision-metrics">
        <div>
          <div className="metric-head">
            <span>Combined score</span>
            <span className="mono strong">{signed(score)}</span>
          </div>
          <div className="gauge" aria-label={`Decision score ${score}`}>
            <div className="gauge-zone avoid" style={{ left: 0, width: toPos(-THRESHOLD) }} />
            <div className="gauge-zone buy" style={{ left: toPos(THRESHOLD), right: 0 }} />
            <div className="gauge-tick" style={{ left: '50%' }} />
            <div className="gauge-marker" style={{ left: toPos(score) }} />
          </div>
          <div className="gauge-labels">
            <span>AVOID</span>
            <span>HOLD</span>
            <span>BUY</span>
          </div>
        </div>

        <div>
          <div className="metric-head">
            <span>Model prediction</span>
            <span className={`mono strong t-${tone(result.prediction)}`}>{result.prediction ?? '—'}</span>
          </div>
          <div className="split-bar">
            <div className="split-up" style={{ width: pct(up) }} />
            <div className="split-down" style={{ width: pct(down) }} />
          </div>
          <div className="gauge-labels">
            <span className="t-pos">Up {pct(up)}</span>
            <span className="t-neg">Down {pct(down)}</span>
          </div>
        </div>
      </div>

      {result.explanation && <p className="decision-explain">{result.explanation.split('. ')[0]}.</p>}
    </section>
  )
}

export default DecisionCard
