import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getReunion, updateReunion, updateAsistencia, addOracionReunion, updateOracionReunion, deleteOracionReunion, createTestimonio, getTestimonios } from '../lib/api'
import type { ReunionDetalle, OracaoReunion, AsistenciaItem, Testimonio } from '../lib/types'

export default function ReunionDetalleePage() {
  const { id, reunionId } = useParams<{ id: string; reunionId: string }>()
  const navigate = useNavigate()
  const [reunion, setReunion] = useState<ReunionDetalle | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const [fecha, setFecha] = useState('')
  const [tipo, setTipo] = useState('periodica')
  const [visitantes, setVisitantes] = useState(0)
  const [novosCrentes, setNovosCrentes] = useState(0)
  const [observaciones, setObservaciones] = useState('')
  const [asistencia, setAsistencia] = useState<AsistenciaItem[]>([])
  const [oraciones, setOraciones] = useState<OracaoReunion[]>([])
  const [newOracaoTexto, setNewOracaoTexto] = useState('')
  const [showAddOracao, setShowAddOracao] = useState(false)
  const [testimonios, setTestimonios] = useState<Testimonio[]>([])
  const [newTestTitulo, setNewTestTitulo] = useState('')
  const [newTestContenido, setNewTestContenido] = useState('')
  const [newTestDestacado, setNewTestDestacado] = useState(false)
  const [addingTest, setAddingTest] = useState(false)

  useEffect(() => {
    Promise.all([
      getReunion(Number(reunionId)),
      getTestimonios({ reunion_id: reunionId }).catch(() => ({ data: [] })),
    ]).then(([r, t]) => {
      const d: ReunionDetalle = r.data
      setReunion(d)
      setFecha(d.fecha)
      setTipo(d.tipo)
      setVisitantes(d.visitantes_count)
      setNovosCrentes(d.novos_crentes_count)
      setObservaciones(d.observaciones ?? '')
      setAsistencia(d.asistencia ?? [])
      setOraciones(d.oraciones ?? [])
      setTestimonios(t.data)
    }).catch(() => navigate(`/grupos/${id}`)).finally(() => setLoading(false))
  }, [reunionId])

  const handleSave = async () => {
    setSaving(true); setError('')
    try {
      await updateReunion(Number(reunionId), { fecha, tipo, visitantes_count: visitantes, novos_crentes_count: novosCrentes, observaciones: observaciones || null })
      await updateAsistencia(Number(reunionId), asistencia.map(a => ({ integrante_id: a.integrante_id, presente: a.presente })))
      navigate(`/grupos/${id}`)
    } catch { setError('Error al guardar la reunión.') } finally { setSaving(false) }
  }

  const toggleAsistencia = (iid: number) => setAsistencia(prev => prev.map(a => a.integrante_id === iid ? { ...a, presente: !a.presente } : a))

  const handleAddOracao = async () => {
    if (!newOracaoTexto.trim()) return
    try {
      const r = await addOracionReunion(Number(reunionId), { texto: newOracaoTexto, respondida: false })
      setOraciones(prev => [...prev, r.data])
      setNewOracaoTexto('')
      setShowAddOracao(false)
    } catch { alert('Error al añadir oración') }
  }

  const toggleOracao = async (o: OracaoReunion) => {
    try {
      const updated = { ...o, respondida: !o.respondida, fecha_respondida: !o.respondida ? new Date().toISOString().slice(0, 10) : null }
      await updateOracionReunion(Number(reunionId), o.id, { respondida: updated.respondida, fecha_respondida: updated.fecha_respondida })
      setOraciones(prev => prev.map(p => p.id === o.id ? { ...p, respondida: updated.respondida, fecha_respondida: updated.fecha_respondida ?? undefined } : p))
    } catch { alert('Error') }
  }

  const deleteOracao = async (oid: number) => {
    if (!confirm('¿Eliminar esta oración?')) return
    try {
      await deleteOracionReunion(Number(reunionId), oid)
      setOraciones(prev => prev.filter(o => o.id !== oid))
    } catch { alert('Error') }
  }

  const handleAddTestimonio = async () => {
    if (!newTestTitulo.trim() || !newTestContenido.trim()) return
    setAddingTest(true)
    try {
      const r = await createTestimonio({ titulo: newTestTitulo, contenido: newTestContenido, destacado: newTestDestacado, grupo_id: Number(id), reunion_id: Number(reunionId) })
      setTestimonios(prev => [...prev, r.data])
      setNewTestTitulo(''); setNewTestContenido(''); setNewTestDestacado(false)
    } catch { alert('Error al añadir testimonio') } finally { setAddingTest(false) }
  }

  if (loading) return <div className="animate-pulse text-center py-20 text-grey-dark">Cargando...</div>
  if (!reunion) return null

  const presentesCount = asistencia.filter(a => a.presente).length

  return (
    <div className="flex flex-col gap-4 pb-24">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-grey-dark hover:text-primary w-fit">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" /></svg>
        Volver
      </button>
      <h2 className="section-title">Reunión</h2>
      {error && <div className="bg-red-100 border border-red-300 text-red-700 rounded-card p-3 text-sm">{error}</div>}

      {/* Bloco 1: Datos */}
      <div className="card flex flex-col gap-3">
        <h3 className="font-bold text-dark">Datos de la reunión</h3>
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
      </div>

      {/* Bloco 2: Asistencia */}
      <div className="card">
        <h3 className="font-bold text-dark mb-2">Asistencia ({presentesCount}/{asistencia.length})</h3>
        <div className="flex flex-col gap-1 mb-4">
          {asistencia.map(a => (
            <label key={a.integrante_id} className="flex items-center gap-3 py-2 border-b border-background last:border-0 cursor-pointer">
              <input type="checkbox" checked={a.presente} onChange={() => toggleAsistencia(a.integrante_id)} className="w-5 h-5 accent-primary" />
              <span className="text-sm text-dark">{a.integrante_nombre}</span>
            </label>
          ))}
          {asistencia.length === 0 && <p className="text-sm text-grey-dark text-center py-2">No hay integrantes en este grupo.</p>}
        </div>
        <div className="flex gap-4">
          <div className="flex-1">
            <label className="text-xs text-grey-dark mb-1 block">Visitantes</label>
            <input type="number" min="0" className="input-field" value={visitantes} onChange={e => setVisitantes(Number(e.target.value))} />
          </div>
          <div className="flex-1">
            <label className="text-xs text-grey-dark mb-1 block">Novos crentes</label>
            <input type="number" min="0" className="input-field" value={novosCrentes} onChange={e => setNovosCrentes(Number(e.target.value))} />
          </div>
        </div>
      </div>

      {/* Bloco 3: Oraciones */}
      <div className="card">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-bold text-dark">Oraciones</h3>
          <button onClick={() => setShowAddOracao(!showAddOracao)} className="text-xs text-primary underline">+ AÑADIR ORACIÓN</button>
        </div>
        {showAddOracao && (
          <div className="mb-3 flex flex-col gap-2 bg-background rounded-card p-3">
            <textarea className="input-field" rows={3} placeholder="Texto de la oración..." value={newOracaoTexto} onChange={e => setNewOracaoTexto(e.target.value)} />
            <div className="flex gap-2">
              <button onClick={handleAddOracao} className="btn-primary flex-1 text-sm py-2">Añadir</button>
              <button onClick={() => setShowAddOracao(false)} className="btn-outline flex-1 text-sm py-2">Cancelar</button>
            </div>
          </div>
        )}
        <div className="flex flex-col gap-3">
          {oraciones.map(o => (
            <div key={o.id} className="border-b border-background pb-3 last:border-0">
              <div className="flex items-start justify-between gap-2">
                <p className="text-sm text-dark flex-1">{o.texto}</p>
                <button onClick={() => deleteOracao(o.id)} className="text-grey-dark hover:text-red-500 text-xs flex-shrink-0">✕</button>
              </div>
              <div className="flex items-center gap-2 mt-2">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" checked={o.respondida} onChange={() => toggleOracao(o)} className="accent-primary" />
                  <span className={`text-xs font-bold ${o.respondida ? 'text-primary' : 'text-grey-dark'}`}>Respondida</span>
                </label>
                {o.respondida && o.fecha_respondida && (
                  <span className="text-xs text-grey-dark">{o.fecha_respondida}</span>
                )}
              </div>
            </div>
          ))}
          {oraciones.length === 0 && <p className="text-sm text-grey-dark text-center py-2">Sin oraciones registradas.</p>}
        </div>
      </div>

      {/* Bloco 4: Observaciones */}
      <div className="card">
        <h3 className="font-bold text-dark mb-2">Observaciones</h3>
        <textarea className="input-field" rows={4} value={observaciones} onChange={e => setObservaciones(e.target.value)} placeholder="Notas de la reunión..." />
      </div>

      {/* Bloco 5: Testimonios */}
      <div className="card">
        <h3 className="font-bold text-dark mb-3">Testimonios</h3>
        <div className="flex flex-col gap-3 mb-3">
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Título</label>
            <input className="input-field" value={newTestTitulo} onChange={e => setNewTestTitulo(e.target.value)} placeholder="Título del testimonio..." />
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Contenido</label>
            <textarea className="input-field" rows={3} value={newTestContenido} onChange={e => setNewTestContenido(e.target.value)} placeholder="Contenido del testimonio..." />
          </div>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={newTestDestacado} onChange={e => setNewTestDestacado(e.target.checked)} className="accent-primary" />
            <span className="text-sm text-dark">Destacado</span>
          </label>
          <button onClick={handleAddTestimonio} disabled={addingTest} className="btn-primary">{addingTest ? 'Añadiendo...' : 'AÑADIR TESTIMONIO'}</button>
        </div>
        {testimonios.length > 0 && (
          <div className="flex flex-col gap-2 border-t border-background pt-3">
            {testimonios.map(t => (
              <div key={t.id} className="text-sm">
                <p className="font-bold text-dark">{t.titulo}</p>
                <p className="text-xs text-grey-dark line-clamp-2">{t.contenido}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="fixed bottom-4 right-4 left-4 z-10">
        <button onClick={handleSave} disabled={saving} className="btn-primary w-full">{saving ? 'Guardando...' : 'GUARDAR REUNIÓN'}</button>
      </div>
    </div>
  )
}
