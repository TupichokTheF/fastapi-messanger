import router from '../router'

let refreshPromise = null

function extractToken(data) {
  return data && (data.token || data.access_token)
}

async function refreshToken() {
  if (refreshPromise) return refreshPromise
  refreshPromise = (async () => {
    const res = await fetch('/api/v1/auth/refresh', {
      method: 'POST',
      credentials: 'include',
      headers: { accept: 'application/json' },
    })
    if (!res.ok) throw new Error('refresh failed')
    const data = await res.json().catch(() => ({}))
    const next = extractToken(data)
    if (!next) throw new Error('refresh response missing token')
    localStorage.setItem('token', next)
    return next
  })().finally(() => {
    refreshPromise = null
  })
  return refreshPromise
}

function withAuth(options, token) {
  const headers = { ...(options.headers || {}) }
  if (token) headers.Authorization = `Bearer ${token}`
  return { ...options, headers }
}

export async function apiFetch(url, options = {}) {
  let res = await fetch(url, withAuth(options, localStorage.getItem('token')))
  if (res.status !== 401) return res

  try {
    const next = await refreshToken()
    return await fetch(url, withAuth(options, next))
  } catch {
    localStorage.removeItem('token')
    router.push('/login')
    return res
  }
}
