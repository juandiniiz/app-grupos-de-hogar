import React, { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getIntegrante, deleteIntegrante, getIntegranteAsistencia, getServicios } from '../lib/api'
import type { Integrante } from '../lib/types'

function ProgressBar({ label, value, total }: { label: string; value: number; total: number }) {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0
  return (
    <div className="mb-3">
      <div className="flex justify-between text-sm mb-1">
        <span className="text-dark">{label}</span>
        <span className="text-grey-dark">{value} ({pct}%)</span>
      </div>
      <div className="bg-[#CBCBCB] rounded-full h-2">
        <div className="bg-primary h-2 rounded-full" style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

function EstadoBadge({ estado }: { estado: string }) {
  const colors: Record<string, string> = {
    no_iniciado: 'bg-[#CBCBCB] text-dark',
    cursando: 'bg-[#BCD11A] text-dark',
    terminado: 'bg-[#66B97B] text-white',
  }
  const labels: Record<string, string> = { no_iniciado: 'No iniciado', cursando: 'Cursando', terminado: 'Terminado' }
  return <span className={`px-2 py-0.5 rounded-badge text-xs font-bold ${colors[estado] ?? 'bg-grey text-dark'}`}>{labels[estado] ?? estado}</span>
}

interface WaModalProps {
  nombre: string
  telefono: string
  onClose: () => void
}

function WhatsAppModal({ nombre, telefono, onClose }: WaModalProps) {
  const clean = telefono.replace(/\D/g, '')
  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <div className="card max-w-sm w-full">
        <h3 className="font-bold text-dark mb-2">Abrir WhatsApp</h3>
        <p className="text-sm text-grey-dark mb-4">¿Abrir WhatsApp para contactar a <strong>{nombre}</strong>?</p>
        <div className="flex gap-3">
          <button onClick={() => { window.open(`https://wa.me/${clean}`); onClose() }} className="btn-primary flex-1">Confirmar</button>
          <button onClick={onClose} className="btn-outline flex-1">Cancelar</button>
        </div>
      </div>
    </div>
  )
}

export default function IntegranteDetalle() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [integrante, setIntegrante] = useState<Integrante | null>(null)
  const [asistencia, setAsistencia] = useState<any>(null)
  const [servicios, setServicios] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [deleting, setDeleting] = useState(false)
  const [showWa, setShowWa] = useState(false)

  useEffect(() => {
    Promise.all([
      getIntegrante(Number(id)),
      getIntegranteAsistencia(Number(id)).catch(() => null),
      getServicios({ integrante_id: id }).catch(() => ({ data: [] })),
    ]).then(([i, a, s]) => {
      setIntegrante(i.data)
      setAsistencia(a?.data)
      setServicios(s.data)
    }).catch(() => navigate('/integrantes')).finally(() => setLoading(false))
  }, [id])

  const handleDelete = async () => {
    if (!confirm(`¿Seguro que quieres dar de baja a ${integrante?.nombre}?`)) return
    setDeleting(true)
    try {
      await deleteIntegrante(Number(id))
      navigate('/integrantes')
    } catch {
      alert('Error al eliminar el integrante.')
      setDeleting(false)
    }
  }

  if (loading) return <div className="animate-pulse text-center py-20 text-grey-dark">Cargando...</div>
  if (!integrante) return null

  const initials = `${integrante.nombre} ${integrante.apellidos}`.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)

  const formRows = [
    { label: 'Discipulado inicial', value: integrante.discipulado_inicial },
    { label: 'Pre-bautismo', value: integrante.pre_batismo },
    { label: 'Escuela bíblica', value: integrante.escuela_biblica },
    { label: 'Escuela discipulado', value: integrante.escuela_discipulado },
    { label: 'Entrenamiento', value: integrante.treinamento },
  ]

  return (
    <div className="flex flex-col gap-4 pb-24">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-grey-dark hover:text-primary w-fit">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" /></svg>
        Volver
      </button>

      {/* Bloco 1: Info */}
      <div className="card flex flex-col items-center gap-3 py-5">
        {integrante.foto_url
          ? <img src={integrante.foto_url} alt={integrante.nombre} className="w-20 h-20 rounded-full object-cover shadow-card" />
          : <div className="w-20 h-20 rounded-full bg-primary flex items-center justify-center text-white text-3xl font-bold shadow-card">{initials}</div>
        }
        <div className="text-center">
          <h2 className="text-2xl font-bold text-dark">{integrante.nombre} {integrante.apellidos}</h2>
          {integrante.edad && <p className="text-sm text-grey-dark">{integrante.edad} años</p>}
          {integrante.fecha_nacimiento && !integrante.edad && <p className="text-sm text-grey-dark">{integrante.fecha_nacimiento}</p>}
        </div>

        <div className="w-full mt-2 flex flex-col gap-2">
          {integrante.email && (
            <div className="flex items-center justify-between py-2 border-b border-background">
              <span className="text-sm text-dark">{integrante.email}</span>
              <button onClick={() => navigator.clipboard?.writeText(integrante.email!)} className="text-grey-dark hover:text-primary ml-2">📋</button>
            </div>
          )}
          {integrante.telefono && (
            <div className="flex items-center justify-between py-2 border-b border-background">
              <span className="text-sm text-dark">{integrante.telefono}</span>
              <div className="flex gap-2">
                <button onClick={() => setShowWa(true)} className="text-xs px-2 py-1 bg-[#25D366] text-white rounded-badge">WhatsApp</button>
                <a href={`tel:${integrante.telefono}`} className="text-xs px-2 py-1 bg-primary text-white rounded-badge">Llamar</a>
                <button onClick={() => navigator.clipboard?.writeText(integrante.telefono!)} className="text-grey-dark hover:text-primary">📋</button>
              </div>
            </div>
          )}
          {integrante.endereco && (
            <div className="py-2 border-b border-background">
              <span className="text-xs text-grey-dark">Dirección</span>
              <p className="text-sm text-dark">{integrante.endereco}</p>
            </div>
          )}
          {integrante.grupos?.filter(g => g.rol_en_grupo === 'responsable').length > 0 && (
            <div className="py-2 border-b border-background">
              <span className="text-xs text-grey-dark">Responsable de</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {integrante.grupos.filter(g => g.rol_en_grupo === 'responsable').map(g => (
                  <span key={g.grupo_id} className="px-2 py-0.5 rounded-badge text-xs bg-[#72E6EA] text-dark">{g.grupo_nombre}</span>
                ))}
              </div>
            </div>
          )}
          {integrante.grupos?.filter(g => g.rol_en_grupo === 'supervisor').length > 0 && (
            <div className="py-2 border-b border-background">
              <span className="text-xs text-grey-dark">Supervisor de</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {integrante.grupos.filter(g => g.rol_en_grupo === 'supervisor').map(g => (
                  <span key={g.grupo_id} className="px-2 py-0.5 rounded-badge text-xs bg-[#CBCBCB] text-dark">{g.grupo_nombre}</span>
                ))}
              </div>
            </div>
          )}
          {integrante.is_membro && (
            <div className="py-2">
              <span className="px-2 py-1 rounded-badge text-xs bg-primary text-white">Miembro {integrante.numero_membro ? `#${integrante.numero_membro}` : ''}</span>
            </div>
          )}
        </div>
      </div>

      {/* Bloco 2: Asistencia */}
      {asistencia && (
        <div className="card">
          <h3 className="font-bold text-dark mb-3">Asistencia</h3>
          <ProgressBar label="Último mes" value={asistencia.ultimo_mes ?? 0} total={asistencia.total_reuniones_mes ?? 1} />
          <ProgressBar label="Último año" value={asistencia.ultimo_ano ?? 0} total={asistencia.total_reuniones_ano ?? 1} />
          <ProgressBar label="Total" value={asistencia.total ?? 0} total={asistencia.total_reuniones ?? 1} />
        </div>
      )}

      {/* Bloco 3: Formación y Fe */}
      <div className="card">
        <h3 className="font-bold text-dark mb-3">Formación</h3>
        <table className="w-full text-sm">
          <tbody>
            {formRows.map(row => (
              <tr key={row.label} className="border-b border-background">
                <td className="py-1.5 text-grey-dark pr-4">{row.label}</td>
                <td className="py-1.5"><EstadoBadge estado={row.value} /></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="mt-4 flex flex-col gap-2">
          <h4 className="font-bold text-dark text-sm">Fe</h4>
          <div className="flex flex-wrap gap-2">
            {integrante.bautizado && <span className="px-2 py-1 rounded-badge text-xs bg-[#66B97B] text-white">Bautizado</span>}
            {integrante.novo_crente && <span className="px-2 py-1 rounded-badge text-xs bg-[#45C1EE] text-white">Novo crente</span>}
            {integrante.novo_batizado && <span className="px-2 py-1 rounded-badge text-xs bg-[#BCD11A] text-dark">Novo bautizado</span>}
            {integrante.iglesia_procedente && <span className="px-2 py-1 rounded-badge text-xs bg-[#CBCBCB] text-dark">De otra iglesia{integrante.iglesia_procedente_nome ? `: ${integrante.iglesia_procedente_nome}` : ''}</span>}
          </div>
          {integrante.ministerios?.length > 0 && (
            <div className="mt-2">
              <span className="text-xs text-grey-dark">Ministerios: </span>
              {integrante.ministerios.map(m => (
                <span key={m.id} className="mr-1 text-sm text-dark">{m.nombre}{m.es_responsable ? ' (resp.)' : ''}</span>
              ))}
            </div>
          )}
          {integrante.observaciones && (
            <div className="mt-2">
              <span className="text-xs text-grey-dark">Observaciones</span>
              <p className="text-sm text-dark mt-1 whitespace-pre-wrap">{integrante.observaciones}</p>
            </div>
          )}
        </div>
      </div>

      {/* Bloco 4: Servicios */}
      {servicios.length > 0 && (
        <div className="card">
          <h3 className="font-bold text-dark mb-3">Servicios</h3>
          <div className="flex flex-col gap-2">
            {servicios.map((s: any) => (
              <div key={s.id} className="flex justify-between items-center py-2 border-b border-background">
                <div>
                  <p className="text-sm font-bold text-dark">{s.titulo}</p>
                  <p className="text-xs text-grey-dark">{s.fecha}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="fixed bottom-4 right-4 left-4 z-10 flex flex-col gap-2">
        <Link to={`/integrantes/${id}/editar`}>
          <button className="btn-primary w-full">EDITAR</button>
        </Link>
        <button onClick={handleDelete} disabled={deleting} className="w-full py-3 text-center font-bold text-[#F21D61] border border-[#F21D61] rounded-button text-sm">
          {deleting ? 'Procesando...' : 'DAR DE BAJA'}
        </button>
      </div>

      {showWa && integrante.telefono && (
        <WhatsAppModal nombre={`${integrante.nombre} ${integrante.apellidos}`} telefono={integrante.telefono} onClose={() => setShowWa(false)} />
      )}
    </div>
  )
}
