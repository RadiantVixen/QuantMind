// Thin fetch wrapper around the Django API.
// In dev/Docker, requests go to the relative /api path (proxied to the backend).
// On GitHub Pages, set VITE_API_URL to the public backend origin,
// e.g. https://quantmind-api.onrender.com
const API_BASE = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '')

// ---------- Auth token ----------
// Kept in localStorage so a page refresh keeps you signed in. The token is
// sent as an Authorization header (not a cookie), which works across domains.

const TOKEN_KEY = 'quantmind_token'

export const getToken = () => localStorage.getItem(TOKEN_KEY)
const setToken = (token) => localStorage.setItem(TOKEN_KEY, token)
export const clearToken = () => localStorage.removeItem(TOKEN_KEY)

// Called when the backend rejects the token (expired, or logged out elsewhere).
let onUnauthorized = () => {}
export const setUnauthorizedHandler = (fn) => {
  onUnauthorized = fn
}

// ---------- Request helper ----------

async function request(path, options = {}) {
  const token = getToken()
  let response
  try {
    response = await fetch(`${API_BASE}/api${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Token ${token}` } : {}),
        ...options.headers,
      },
    })
  } catch (err) {
    if (err.name === 'AbortError') throw err
    throw new Error('Cannot reach the QuantMind API. Is the backend running?')
  }

  if (response.status === 401 && token) {
    clearToken()
    onUnauthorized()
    throw new Error('Your session has expired. Please sign in again.')
  }

  if (response.status === 204) return null

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    const message =
      (data.error && [].concat(data.error).join(' ')) ||
      data.detail ||
      Object.entries(data)
        .map(([field, errs]) => `${field}: ${[].concat(errs).join(', ')}`)
        .join(' · ') ||
      `Request failed (${response.status})`
    throw new Error(message)
  }

  return data
}

// ---------- Auth ----------

async function authenticate(path, credentials) {
  const data = await request(path, {
    method: 'POST',
    body: JSON.stringify(credentials),
  })
  setToken(data.token)
  return data.user
}

export const login = (username, password) =>
  authenticate('/auth/login/', { username, password })

export const register = (username, email, password) =>
  authenticate('/auth/register/', { username, email, password })

export const getCurrentUser = () => request('/auth/me/')

export async function logout() {
  try {
    await request('/auth/logout/', { method: 'POST' })
  } finally {
    clearToken()
  }
}

// ---------- QuantMind ----------

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
