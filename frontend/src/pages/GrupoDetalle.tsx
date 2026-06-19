import React, { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getGrupo, getGrupoIntegrantes, getReuniones, createReunion, getTestimonios, updateTestimonio } from '../lib/api'
import type { Grupo, GrupoIntegrante, Reunion, Testimonio } from '../lib/types'
import MapaComponent from '../components/MapaComponent'

interface WaModalProps { nombre: string; telefono: string; onClose: () => void }
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

interface NewReunionModalProps { grupoId: number; onClose: () => void; onCreated: (id: number) => void }
function NewReunionModal({ grupoId, onClose, onCreated }: NewReunionModalProps) {
  const [fecha, setFecha] = useState(new Date().toISOString().slice(0, 10))
  const [tipo, setTipo] = useState('periodica')
  const [saving, setSaving] = useState(false)
  const handleSave = async () => {
    setSaving(true)
    try {
      const r = await createReunion({ grupo_id: grupoId, fecha, tipo })
      onCreated(r.data.id)
    } catch { alert('Error al crear la reunión') } finally { setSaving(false) }
  }
  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <div className="card max-w-sm w-full flex flex-col gap-3">
        <h3 className="font-bold text-dark">Nueva Reunión</h3>
        <div>
          <label className="text-xs text-grey-dark mb-1 block">Fecha</label>
          <input type="date" className="input-field" value={fecha} onChange={e => setFecha(e.target.value)} />
        </div>
        <div>
          <label className="text-xs text-grey-dark mb-1 block">Tipo</label>
          <select className="input-field" value={tipo} onChange={e => setTipo(e.target.value)}>
            <option value="periodica">Periódica</option>
            <option value="comunhao">Comunhão</option>
            <option value="evangelistica">Evangelística</option>
          </select>
        </div>
        <div className="flex gap-3">
          <button onClick={handleSave} disabled={saving} className="btn-primary flex-1">{saving ? 'Creando...' : 'Crear'}</button>
          <button onClick={onClose} className="btn-outline flex-1">Cancelar</button>
        </div>
      </div>
    </div>
  )
}

export default function GrupoDetalle() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [grupo, setGrupo] = useState<Grupo | null>(null)
  const [integrantes, setIntegrantes] = useState<GrupoIntegrante[]>([])
  const [reuniones, setReuniones] = useState<Reunion[]>([])
  const [testimonios, setTestimonios] = useState<Testimonio[]>([])
  const [loading, setLoading] = useState(true)
  const [showMap, setShowMap] = useState(false)
  const [showWa, setShowWa] = useState(false)
  const [showNewReunion, setShowNewReunion] = useState(false)

  const load = () => Promise.all([
    getGrupo(Number(id)),
    getGrupoIntegrantes(Number(id)),
    getReuniones({ grupo_id: id }),
    getTestimonios({ grupo_id: id }),
  ]).then(([g, i, r, t]) => {
    setGrupo(g.data)
    setIntegrantes(i.data)
    setReuniones(r.data)
    setTestimonios(t.data)
  }).catch(() => navigate('/grupos')).finally(() => setLoading(false))

  useEffect(() => { load() }, [id])

  const totalVisitantes = reuniones.reduce((s, r) => s + (r.visitantes_count ?? 0), 0)
  const totalNovos = reuniones.reduce((s, r) => s + (r.novos_crentes_count ?? 0), 0)
  const membros = integrantes.filter(i => i.bautizado).length
  const novosBatizados = integrantes.filter(i => i.novo_batizado).length

  const tipoBadge = (tipo: string) => {
    if (tipo === 'periodica') return 'bg-[#66B97B] text-white'
    if (tipo === 'comunhao') return 'bg-[#45C1EE] text-white'
    if (tipo === 'evangelistica') return 'bg-[#BCD11A] text-dark'
    return 'bg-grey text-dark'
  }

  const tipoLabel = (tipo: string) => ({ periodica: 'Periódica', comunhao: 'Comunhão', evangelistica: 'Evangelística' }[tipo] ?? tipo)

  const frecBadge = (f?: string) => {
    if (f === 'semanal') return 'bg-[#66B97B] text-white'
    if (f === 'quincenal') return 'bg-[#BCD11A] text-dark'
    if (f === 'mensual') return 'bg-[#45C1EE] text-white'
    return 'bg-grey text-dark'
  }

  if (loading) return <div className="animate-pulse text-center py-20 text-grey-dark">Cargando...</div>
  if (!grupo) return null

  const mapPoints = (grupo.latitude && grupo.longitude) ? [{ id: grupo.id, nombre: grupo.nombre, latitude: grupo.latitude, longitude: grupo.longitude }] : []

  return (
    <div className="flex flex-col gap-4 pb-20">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-grey-dark hover:text-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" /></svg>
          Volver
        </button>
        <button onClick={() => setShowNewReunion(true)} className="btn-primary text-sm px-4 py-2">+ REUNIÓN</button>
      </div>

      {/* Bloco 1: Info */}
      <div className="card">
        <div className="flex items-start justify-between">
          <h2 className="text-2xl font-bold text-dark">{grupo.nombre}</h2>
          {!grupo.activo && <span className="px-2 py-0.5 rounded-badge text-xs bg-red text-white">Inactivo</span>}
        </div>
        <p className="text-xs text-grey-dark mt-1">{grupo.created_at ? `Creado: ${grupo.created_at.slice(0,10)}` : ''}</p>
        {grupo.grupo_pai_nombre && <p className="text-sm mt-2">Grupo padre: <span className="text-primary font-bold">{grupo.grupo_pai_nombre}</span></p>}
        <div className="mt-2 flex flex-col gap-1">
          {grupo.responsable_nombre && (
            <div className="flex items-center gap-2">
              <span className="text-xs text-grey-dark">Responsable:</span>
              <span className="text-sm font-bold text-primary">{grupo.responsable_nombre}</span>
              {grupo.responsable_id && (
                <button onClick={() => setShowWa(true)} className="text-xs px-2 py-0.5 bg-[#25D366] text-white rounded-badge">WhatsApp</button>
              )}
            </div>
          )}
          {grupo.ayudante_nombre && <p className="text-sm">Ayudante: <span className="font-bold">{grupo.ayudante_nombre}</span></p>}
          {grupo.supervisor_nombre && <p className="text-sm">Supervisor: <span className="font-bold text-[#45C1EE]">{grupo.supervisor_nombre}</span></p>}
        </div>
      </div>

      {/* Bloco 2: Horario */}
      <div className="card">
        <h3 className="font-bold text-dark mb-2">Horario y lugar</h3>
        <div className="flex flex-wrap gap-2 items-center mb-2">
          {grupo.dia_semana && <span className="capitalize text-dark text-sm">{grupo.dia_semana}</span>}
          {grupo.hora && <span className="text-sm text-dark">{grupo.hora}</span>}
          {grupo.frecuencia && <span className={`px-2 py-0.5 rounded-badge text-xs font-bold ${frecBadge(grupo.frecuencia)}`}>{grupo.frecuencia}</span>}
        </div>
        {grupo.endereco && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-dark">{grupo.endereco}</span>
            <a href={`https://maps.google.com/?q=${encodeURIComponent(grupo.endereco)}`} target="_blank" rel="noreferrer" className="text-grey-dark hover:text-primary">🗺️</a>
          </div>
        )}
        {mapPoints.length > 0 && (
          <button onClick={() => setShowMap(!showMap)} className="mt-2 text-xs text-primary underline">{showMap ? 'Ocultar mapa' : 'MOSTRAR EN MAPA'}</button>
        )}
        {showMap && mapPoints.length > 0 && <div className="mt-2"><MapaComponent points={mapPoints} height="200px" /></div>}
      </div>

      {/* Bloco 3: Integrantes */}
      <div className="card">
        <h3 className="font-bold text-dark mb-2">Integrantes ({integrantes.length})</h3>
        <div className="flex flex-col gap-2">
          {integrantes.map(i => (
            <Link to={`/integrantes/${i.id}`} key={i.id}>
              <div className="flex items-center gap-2 py-2 border-b border-background last:border-0">
                <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                  {`${i.nombre} ${i.apellidos}`.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-dark truncate">{i.nombre} {i.apellidos}</p>
                  <div className="flex items-center gap-1 mt-0.5">
                    <div className="bg-[#CBCBCB] rounded-full h-1.5 flex-1 max-w-[80px]">
                      <div className="bg-primary h-1.5 rounded-full" style={{ width: `${i.asistencia_pct ?? 0}%` }} />
                    </div>
                    <span className="text-xs text-grey-dark">{i.asistencia_pct ?? 0}%</span>
                  </div>
                </div>
                <div className="flex gap-1">
                  {i.novo_crente && <span className="w-2 h-2 rounded-full bg-[#45C1EE]" title="Novo crente" />}
                  {i.bautizado && <span className="w-2 h-2 rounded-full bg-[#66B97B]" title="Bautizado" />}
                  {i.novo_batizado && <span className="w-2 h-2 rounded-full bg-[#BCD11A]" title="Novo bautizado" />}
                </div>
              </div>
            </Link>
          ))}
          {integrantes.length === 0 && <p className="text-sm text-grey-dark text-center py-2">Sin integrantes.</p>}
        </div>
      </div>

      {/* Bloco 4: Fe stats */}
      <div className="card">
        <h3 className="font-bold text-dark mb-2">Estadísticas</h3>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-background rounded-card p-3 text-center"><div className="text-2xl font-bold text-dark">{totalVisitantes}</div><div className="text-xs text-grey-dark">Visitantes</div></div>
          <div className="bg-background rounded-card p-3 text-center"><div className="text-2xl font-bold text-dark">{membros}</div><div className="text-xs text-grey-dark">Bautizados</div></div>
          <div className="bg-background rounded-card p-3 text-center"><div className="text-2xl font-bold text-dark">{novosBatizados}</div><div className="text-xs text-grey-dark">Novos bautizados</div></div>
          <div className="bg-background rounded-card p-3 text-center"><div className="text-2xl font-bold text-dark">{totalNovos}</div><div className="text-xs text-grey-dark">Novos crentes</div></div>
        </div>
      </div>

      {/* Bloco 5: Porcentajes */}
      {integrantes.length > 0 && (
        <div className="card">
          <h3 className="font-bold text-dark mb-2">Porcentajes</h3>
          <div className="flex flex-col gap-2 text-sm">
            <div className="flex justify-between"><span>Bautizados</span><span>{Math.round(membros/integrantes.length*100)}%</span></div>
            <div className="flex justify-between"><span>Novos crentes</span><span>{Math.round(integrantes.filter(i => i.novo_crente).length/integrantes.length*100)}%</span></div>
          </div>
        </div>
      )}

      {/* Bloco 6: Reuniones */}
      <div className="card">
        <h3 className="font-bold text-dark mb-2">Reuniones ({reuniones.length})</h3>
        <div className="flex gap-3 mb-3">
          {['periodica', 'comunhao', 'evangelistica'].map(tipo => (
            <div key={tipo} className="text-center">
              <div className="text-xl font-bold text-dark">{reuniones.filter(r => r.tipo === tipo).length}</div>
              <div className="text-xs text-grey-dark">{tipoLabel(tipo)}</div>
            </div>
          ))}
        </div>
        <div className="flex flex-col gap-2">
          {reuniones.map(r => (
            <Link to={`/grupos/${id}/reuniones/${r.id}`} key={r.id}>
              <div className="flex items-center justify-between py-2 border-b border-background last:border-0">
                <div>
                  <p className="text-sm font-bold text-dark">{r.fecha}</p>
                  <span className={`px-1.5 py-0.5 rounded-badge text-xs ${tipoBadge(r.tipo)}`}>{tipoLabel(r.tipo)}</span>
                </div>
                <div className="text-xs text-grey-dark text-right">
                  <p>{r.asistentes_count} asist.</p>
                  <p>{r.visitantes_count} visit.</p>
                </div>
              </div>
            </Link>
          ))}
          {reuniones.length === 0 && <p className="text-sm text-grey-dark text-center py-2">Sin reuniones.</p>}
        </div>
      </div>

      {/* Bloco 7: Observaciones */}
      {grupo.observaciones && (
        <div className="card">
          <h3 className="font-bold text-dark mb-2">Observaciones</h3>
          <p className="text-sm text-dark whitespace-pre-wrap">{grupo.observaciones}</p>
        </div>
      )}

      {/* Bloco 8: Testimonios */}
      <div className="card">
        <h3 className="font-bold text-dark mb-2">Testimonios</h3>
        <div className="flex flex-col gap-3">
          {testimonios.map(t => (
            <div key={t.id} className="border-b border-background pb-3 last:border-0">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className="font-bold text-dark text-sm">{t.titulo}</p>
                  <p className="text-xs text-grey-dark">{t.fecha}</p>
                  <p className="text-xs text-dark mt-1 line-clamp-2">{t.contenido}</p>
                </div>
                <button onClick={async () => { await updateTestimonio(t.id, { destacado: !t.destacado }); load() }} className={`ml-2 text-xs px-2 py-0.5 rounded-badge ${t.destacado ? 'bg-[#BCD11A] text-dark' : 'bg-grey text-dark'}`}>
                  {t.destacado ? '★ Destacado' : '☆ Destacar'}
                </button>
              </div>
            </div>
          ))}
          {testimonios.length === 0 && <p className="text-sm text-grey-dark text-center py-2">Sin testimonios.</p>}
        </div>
      </div>

      <Link to={`/grupos/${id}/editar`}>
        <button className="btn-primary w-full">EDITAR GRUPO</button>
      </Link>

      {showWa && grupo.responsable_nombre && (
        <WhatsAppModal nombre={grupo.responsable_nombre} telefono={''} onClose={() => setShowWa(false)} />
      )}
      {showNewReunion && (
        <NewReunionModal grupoId={Number(id)} onClose={() => setShowNewReunion(false)} onCreated={rid => navigate(`/grupos/${id}/reuniones/${rid}`)} />
      )}
    </div>
  )
}
