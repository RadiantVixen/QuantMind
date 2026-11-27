const isNum = (v) => typeof v === 'number' && Number.isFinite(v)

export const usd = (v, digits) => {
  if (!isNum(v)) return '—'
  const d = digits ?? (Math.abs(v) >= 1000 ? 2 : Math.abs(v) >= 1 ? 2 : 6)
  return v.toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: d,
    maximumFractionDigits: d,
  })
}

export const pct = (v, digits = 1) => (isNum(v) ? `${(v * 100).toFixed(digits)}%` : '—')

export const num = (v, digits = 2) =>
  isNum(v)
    ? v.toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits })
    : '—'

export const signed = (v, digits = 3) => (isNum(v) ? `${v > 0 ? '+' : ''}${v.toFixed(digits)}` : '—')

// Maps backend labels onto a small set of semantic tones used by the CSS.
const TONES = {
  BUY: 'pos', BULLISH: 'pos', UP: 'pos', LOW: 'pos', APPROVED: 'pos', POSITIVE: 'pos',
  AVOID: 'neg', BEARISH: 'neg', DOWN: 'neg', HIGH: 'neg', REJECTED: 'neg', NEGATIVE: 'neg',
  HOLD: 'warn', MEDIUM: 'warn', MIXED: 'warn', PENDING: 'warn',
}

export const tone = (label) => TONES[String(label ?? '').toUpperCase()] ?? 'neutral'
