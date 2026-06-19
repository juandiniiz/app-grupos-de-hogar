import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../lib/api'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await login(email, password)
      localStorage.setItem('token', res.data.access_token)
      // Fetch user profile
      const { default: api } = await import('../lib/api')
      const me = await api.get('/auth/me')
      localStorage.setItem('user', JSON.stringify(me.data))
      navigate('/')
    } catch {
      setError('Email o contraseña incorrectos. Inténtalo de nuevo.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-4">
      <div className="bg-white rounded-card shadow-card w-full max-w-sm px-8 py-10 flex flex-col items-center gap-6">
        {/* Logo */}
        <div className="flex flex-col items-center gap-1">
          <div className="w-16 h-16 rounded-full bg-primary flex items-center justify-center mb-1">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="white">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
            </svg>
          </div>
          <span className="text-[11px] font-roboto tracking-[0.25em] uppercase text-grey-dark font-light">
            seguimiento
          </span>
          <span className="font-marker text-[#66B97B] text-2xl leading-tight tracking-wide">
            GRUPOS DE HOGAR
          </span>
          <span className="text-[10px] text-grey-dark tracking-widest uppercase font-light">
            Punto de Encuentro
          </span>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="w-full flex flex-col gap-4">
          <div className="flex flex-col gap-1">
            <label htmlFor="email" className="text-sm font-bold text-dark">
              Email
            </label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@email.com"
              className="input-field"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label htmlFor="password" className="text-sm font-bold text-dark">
              Contraseña
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="input-field"
            />
          </div>

          {error && (
            <p className="text-xs text-red text-center bg-red/10 rounded-card px-3 py-2">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full mt-2"
          >
            {loading ? 'Iniciando...' : 'INICIAR SESIÓN'}
          </button>
        </form>

        {/* Forgot password */}
        <button
          type="button"
          className="text-sm text-grey-dark hover:text-primary transition-colors"
          onClick={() => alert('Contacta con el administrador para restablecer tu contraseña.')}
        >
          Ups! He olvidado mi contraseña.
        </button>

        <p className="text-[10px] text-grey-dark">v1.0 © CCLN</p>
      </div>
    </div>
  )
}
