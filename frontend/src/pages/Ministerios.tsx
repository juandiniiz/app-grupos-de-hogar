import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getMinisterios, createMinisterio } from '../lib/api'
import type { Ministerio } from '../lib/types'

export default function Ministerios() {
  const [ministerios, setMinisterios] = useState<Ministerio[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [nombre, setNombre] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [saving, setSaving] = useState(false)

  const load = () => getMinisterios().then(r => setMinisterios(r.data)).catch(() => {}).finally(() => setLoading(false))

  useEffect(() => { load() }, [])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!nombre.trim()) return
    setSaving(true)
    try {
      await createMinisterio({ nombre, descripcion })
      setShowModal(false); setNombre(''); setDescripcion('')
      load()
    } catch { alert('Error al crear ministerio') } finally { setSaving(false) }
  }

  return (
    <div className="flex flex-col gap-4 pb-20">
      <div className="flex items-center justify-between">
        <h2 className="section-title">Ministerios</h2>
      </div>

      {loading ? (
        <div className="animate-pulse text-center py-8 text-grey-dark">Cargando...</div>
      ) : (
        <div className="flex flex-col gap-3">
          {ministerios.map(m => (
            <Link to={`/ministerios/${m.id}`} key={m.id}>
              <div className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-bold text-dark">{m.nombre}</h3>
                    {m.descripcion && <p className="text-xs text-grey-dark mt-1">{m.descripcion}</p>}
                    <p className="text-xs text-grey-dark mt-1">{m.integrantes_count} integrantes</p>
                    {m.responsables?.filter(r => r.es_responsable).length > 0 && (
                      <p className="text-xs text-dark mt-1">
                        Responsable: {m.responsables.filter(r => r.es_responsable).map(r => `${r.nombre} ${r.apellidos}`).join(', ')}
                      </p>
                    )}
                  </div>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="#CBCBCB"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" /></svg>
                </div>
              </div>
            </Link>
          ))}
          {ministerios.length === 0 && <div className="card text-center py-8 text-grey-dark">No hay ministerios registrados.</div>}
        </div>
      )}

      <button onClick={() => setShowModal(true)} className="fixed bottom-4 right-4 left-4 z-10 btn-primary w-full">NUEVO MINISTERIO</button>

      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="card max-w-sm w-full">
            <h3 className="font-bold text-dark mb-3">Nuevo Ministerio</h3>
            <form onSubmit={handleCreate} className="flex flex-col gap-3">
              <div>
                <label className="text-xs text-grey-dark mb-1 block">Nombre *</label>
                <input className="input-field" value={nombre} onChange={e => setNombre(e.target.value)} placeholder="Nombre del ministerio" />
              </div>
              <div>
                <label className="text-xs text-grey-dark mb-1 block">Descripción</label>
                <textarea className="input-field" rows={3} value={descripcion} onChange={e => setDescripcion(e.target.value)} placeholder="Descripción opcional..." />
              </div>
              <div className="flex gap-3">
                <button type="submit" disabled={saving} className="btn-primary flex-1">{saving ? 'Creando...' : 'Crear'}</button>
                <button type="button" onClick={() => setShowModal(false)} className="btn-outline flex-1">Cancelar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
