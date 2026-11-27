function Metric({ label, value }) {
  return (
    <div className="metric">
      <p>{label}</p>
      <h3>{value ?? 'N/A'}</h3>
    </div>
  )
}

function AnalysisResults({ result }) {
  if (!result || result.approval_required) return null

  return (
    <section className="dashboard">
      <h2>Analysis Results</h2>

      <div className="metrics-grid">
        <Metric label="Latest Price" value={`$${result.latest_price?.toFixed(2)}`} />
        <Metric label="Prediction" value={result.prediction} />
        <Metric label="Probability UP" value={`${(result.probability_up * 100).toFixed(1)}%`} />
        <Metric label="Risk Level" value={result.risk_level || 'See risk analysis'} />
      </div>

      <h3>Final Decision</h3>
      <div className="decision">
        <h2>{result.decision}</h2>
        <p>Score: {result.decision_score}</p>
        <p>Agreement: {result.analyst_agreement}</p>
        <p>{result.explanation}</p>
      </div>

      <h3>Quantitative Analysis</h3>
      <div className="metrics-grid">
        <Metric label="Trend" value={result.quant_trend} />
        <Metric label="RSI" value={result.quant_rsi} />
        <Metric label="Momentum" value={result.quant_momentum} />
        <Metric label="Volatility" value={result.quant_volatility_regime} />
        <Metric label="Support" value={result.quant_support} />
        <Metric label="Resistance" value={result.quant_resistance} />
      </div>

      <h3>News Analysis</h3>
      <p>{result.news_sentiment} ({result.news_sentiment_score})</p>
      <p>{result.news_analysis}</p>

      <h3>Portfolio</h3>
      <div className="metrics-grid">
        <Metric label="Risk Budget" value={`$${result.risk_budget}`} />
        <Metric label="Position Value" value={`$${result.recommended_position_value}`} />
        <Metric label="Estimated Max Loss" value={`$${result.estimated_max_loss}`} />
      </div>

      <p>Approval: {result.approval_status}</p>
    </section>
  )
}

export default AnalysisResults