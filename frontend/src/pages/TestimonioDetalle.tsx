import React, { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getTestimonio, getTestimonios } from '../lib/api'
import type { Testimonio } from '../lib/types'

export default function TestimonioDetalle() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [testimonio, setTestimonio] = useState<Testimonio | null>(null)
  const [otros, setOtros] = useState<Testimonio[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      getTestimonio(Number(id)),
      getTestimonios(),
    ]).then(([t, all]) => {
      setTestimonio(t.data)
      setOtros(all.data.filter((o: Testimonio) => o.id !== Number(id)).slice(0, 4))
    }).catch(() => navigate('/testimonios')).finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="animate-pulse text-center py-20 text-grey-dark">Cargando...</div>
  if (!testimonio) return null

  return (
    <div className="flex flex-col gap-4 pb-8">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-grey-dark hover:text-primary w-fit">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" /></svg>
        Volver
      </button>

      <div className="card">
        <p className="text-xs text-grey-dark mb-1">{testimonio.fecha}</p>
        <h2 className="text-2xl font-bold text-dark mb-2">{testimonio.titulo}</h2>
        <div className="flex flex-wrap gap-2 mb-3">
          {testimonio.grupo_nombre && <span className="px-2 py-0.5 rounded-badge text-xs bg-[#72E6EA] text-dark">{testimonio.grupo_nombre}</span>}
          {testimonio.integrante_nombre && <span className="px-2 py-0.5 rounded-badge text-xs bg-[#CBCBCB] text-dark">{testimonio.integrante_nombre}</span>}
          {testimonio.destacado && <span className="px-2 py-0.5 rounded-badge text-xs bg-[#BCD11A] text-dark">★ Destacado</span>}
        </div>
        <p className="text-dark text-sm whitespace-pre-wrap leading-relaxed">{testimonio.contenido}</p>
      </div>

      {otros.length > 0 && (
        <>
          <div className="border-t border-grey my-2" />
          <h3 className="font-bold text-dark">Otros testimonios</h3>
          <div className="grid grid-cols-2 gap-3">
            {otros.map(t => (
              <Link to={`/testimonios/${t.id}`} key={t.id}>
                <div className="card h-full">
                  <p className="text-xs text-grey-dark mb-1">{t.fecha}</p>
                  <p className="font-bold text-dark text-sm">{t.titulo}</p>
                  {t.grupo_nombre && <span className="inline-block mt-1 px-1.5 py-0.5 rounded-badge text-xs bg-[#72E6EA] text-dark">{t.grupo_nombre}</span>}
                  <p className="text-xs text-grey-dark mt-1 line-clamp-2">{t.contenido}</p>
                  <span className="text-xs text-primary underline mt-1 inline-block">Leer más →</span>
                </div>
              </Link>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
