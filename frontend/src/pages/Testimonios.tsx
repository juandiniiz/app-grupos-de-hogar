import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getTestimonios } from '../lib/api'
import type { Testimonio } from '../lib/types'

export default function Testimonios() {
  const [testimonios, setTestimonios] = useState<Testimonio[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getTestimonios().then(r => setTestimonios(r.data)).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="animate-pulse text-center py-8 text-grey-dark">Cargando...</div>

  return (
    <div className="flex flex-col gap-4">
      <h2 className="section-title">Testimonios</h2>
      <div className="flex flex-col gap-3">
        {testimonios.map(t => (
          <div key={t.id} className="card">
            <p className="text-xs text-grey-dark mb-1">{t.fecha}</p>
            <h3 className="font-bold text-dark">{t.titulo}</h3>
            {t.grupo_nombre && <span className="inline-block mt-1 px-2 py-0.5 rounded-badge text-xs bg-[#72E6EA] text-dark">{t.grupo_nombre}</span>}
            <p className="text-sm text-grey-dark mt-2 line-clamp-3">{t.contenido}</p>
            <Link to={`/testimonios/${t.id}`} className="text-xs text-primary underline mt-2 inline-block">Leer más →</Link>
          </div>
        ))}
        {testimonios.length === 0 && <div className="card text-center py-8 text-grey-dark">No hay testimonios registrados.</div>}
      </div>
    </div>
  )
}
