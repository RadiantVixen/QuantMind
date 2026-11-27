function PredictionPanel({ result }) {
  if (!result || result.approval_required) return null

  const up = (result.probability_up || 0) * 100
  const down = (result.probability_down || 0) * 100

  const decisionColor = {
    BUY: '#22c55e',
    HOLD: '#f59e0b',
    AVOID: '#ef4444',
  }[result.decision] || '#60a5fa'

  return (
    <section className="panel">
      <h2>Market Prediction</h2>

      <div className="prediction-header">
        <div>
          <p className="muted">Predicted direction</p>
          <h1>{result.prediction}</h1>
        </div>

        <div>
          <p className="muted">Final decision</p>
          <h1 style={{ color: decisionColor }}>
            {result.decision}
          </h1>
        </div>
      </div>

      <p>Probability of upward movement: {up.toFixed(1)}%</p>
      <div className="probability-track">
        <div
          className="probability-up"
          style={{ width: `${up}%` }}
        />
      </div>

      <p>Probability of downward movement: {down.toFixed(1)}%</p>
      <div className="probability-track">
        <div
          className="probability-down"
          style={{ width: `${down}%` }}
        />
      </div>

      <p className="muted">
        These are model probabilities, not guaranteed outcomes.
      </p>
    </section>
  )
}

export default PredictionPanel

