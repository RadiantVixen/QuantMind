import { useEffect, useState } from 'react'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine,
} from 'recharts'
import { getMarketData } from '../api'
import { usd, pct } from '../format'

const formatTick = (iso, timeframe) => {
  const d = new Date(iso)
  return timeframe === '1d' || timeframe === '4h'
    ? d.toLocaleDateString([], { month: 'short', day: 'numeric' })
    : d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function ChartTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const c = payload[0].payload
  return (
    <div className="chart-tooltip">
      <div className="muted">{new Date(c.timestamp).toLocaleString()}</div>
      <div className="mono strong">{usd(c.close)}</div>
      <div className="tooltip-grid mono">
        <span>O</span>{usd(c.open)}
        <span>H</span>{usd(c.high)}
        <span>L</span>{usd(c.low)}
      </div>
    </div>
  )
}

function PriceChart({ symbol, timeframe, support, resistance }) {
  const [state, setState] = useState({ status: 'loading', candles: [] })

  useEffect(() => {
    if (!symbol) return
    const controller = new AbortController()
    // Debounce so typing a custom pair doesn't spam the API.
    const timer = setTimeout(() => {
      setState((s) => ({ ...s, status: 'loading' }))
      getMarketData(symbol, timeframe, controller.signal)
        .then((data) => setState({ status: 'ready', candles: data.candles ?? [] }))
        .catch((err) => {
          if (err.name !== 'AbortError') setState({ status: 'error', candles: [], error: err.message })
        })
    }, 350)

    return () => {
      clearTimeout(timer)
      controller.abort()
    }
  }, [symbol, timeframe])

  const { candles, status } = state
  const first = candles[0]?.close
  const last = candles.at(-1)?.close
  const change = first && last ? last / first - 1 : null
  const up = (change ?? 0) >= 0
  const color = up ? 'var(--pos)' : 'var(--neg)'

  return (
    <section className="card chart-card">
      <header className="card-head">
        <div>
          <div className="eyebrow">
            {symbol} · {timeframe}
          </div>
          <div className="price-line">
            <span className="price mono">{usd(last)}</span>
            {change !== null && (
              <span className={`chip ${up ? 'pos' : 'neg'}`}>
                {up ? '▲' : '▼'} {pct(Math.abs(change), 2)}
              </span>
            )}
          </div>
        </div>
        <span className="muted small">Last {candles.length || 100} candles</span>
      </header>

      <div className="chart-body">
        {status === 'error' ? (
          <div className="empty">
            <strong>Couldn't load market data</strong>
            <span className="muted">{state.error}</span>
          </div>
        ) : candles.length === 0 ? (
          <div className="skeleton" />
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={candles} margin={{ top: 8, right: 8, bottom: 0, left: 8 }}>
              <defs>
                <linearGradient id="priceFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={color} stopOpacity={0.22} />
                  <stop offset="100%" stopColor={color} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="var(--grid)" vertical={false} />
              <XAxis
                dataKey="timestamp"
                tickFormatter={(v) => formatTick(v, timeframe)}
                stroke="var(--text-3)"
                tickLine={false}
                axisLine={false}
                minTickGap={48}
                fontSize={11}
              />
              <YAxis
                domain={['auto', 'auto']}
                orientation="right"
                stroke="var(--text-3)"
                tickLine={false}
                axisLine={false}
                fontSize={11}
                width={72}
                tickFormatter={(v) => v.toLocaleString('en-US', { maximumFractionDigits: v < 10 ? 4 : 0 })}
              />
              <Tooltip content={<ChartTooltip />} cursor={{ stroke: 'var(--text-3)', strokeDasharray: '3 3' }} />
              {support != null && (
                <ReferenceLine y={support} stroke="var(--pos)" strokeDasharray="4 4" strokeOpacity={0.6}
                  label={{ value: 'Support', position: 'insideBottomLeft', fill: 'var(--pos)', fontSize: 11 }} />
              )}
              {resistance != null && (
                <ReferenceLine y={resistance} stroke="var(--neg)" strokeDasharray="4 4" strokeOpacity={0.6}
                  label={{ value: 'Resistance', position: 'insideTopLeft', fill: 'var(--neg)', fontSize: 11 }} />
              )}
              <Area
                type="monotone"
                dataKey="close"
                stroke={color}
                strokeWidth={2}
                fill="url(#priceFill)"
                isAnimationActive={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
        {status === 'loading' && candles.length > 0 && <div className="chart-refresh">Updating…</div>}
      </div>
    </section>
  )
}

export default PriceChart
