// Thin fetch wrapper around the Django API.
// In dev/Docker, requests go to the relative /api path (proxied to the backend).
// On GitHub Pages, set VITE_API_URL to the public backend origin,
// e.g. https://quantmind-api.onrender.com
const API_BASE = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '')

async function request(path, options = {}) {
  let response
  try {
    response = await fetch(`${API_BASE}/api${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    })
  } catch {
    throw new Error('Cannot reach the QuantMind API. Is the backend running?')
  }

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    const message =
      data.error ||
      Object.entries(data)
        .map(([field, errs]) => `${field}: ${[].concat(errs).join(', ')}`)
        .join(' · ') ||
      `Request failed (${response.status})`
    throw new Error(message)
  }

  return data
}

export const runAnalysis = (params) =>
  request('/analysis/', { method: 'POST', body: JSON.stringify(params) })

export const submitApproval = (threadId, approved) =>
  request('/approval/', {
    method: 'POST',
    body: JSON.stringify({ thread_id: threadId, approved }),
  })

export const getMarketData = (symbol, timeframe, signal) =>
  request(
    `/market-data/?${new URLSearchParams({ symbol, timeframe })}`,
    { signal },
  )
