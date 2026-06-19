import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  getMinisterio, updateMinisterio, addMinisterioIntegrante, removeMinisterioIntegrante,
  addMinisterioTarefa, deleteMinisterioTarefa, addTarefaIntegrante, removeTarefaIntegrante,
  getIntegrantes
} from '../lib/api'
import type { Ministerio, Integrante } from '../lib/types'

export default function MinisterioDetalle() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [ministerio, setMinisterio] = useState<Ministerio | null>(null)
  const [intList, setIntList] = useState<Integrante[]>([])
  const [loading, setLoading] = useState(true)
  const [showEditModal, setShowEditModal] = useState(false)
  const [editNombre, setEditNombre] = useState('')
  const [editDescripcion, setEditDescripcion] = useState('')
  const [saving, setSaving] = useState(false)
  const [addIntSearch, setAddIntSearch] = useState('')
  const [newTarefaNombre, setNewTarefaNombre] = useState('')
  const [tarefaIntSearch, setTarefaIntSearch] = useState<Record<number, string>>({})

  const load = async () => {
    try {
      const [m, il] = await Promise.all([getMinisterio(Number(id)), getIntegrantes({ activo: true })])
      setMinisterio(m.data)
      setIntList(il.data)
    } catch { navigate('/ministerios') } finally { setLoading(false) }
  }

  useEffect(() => { load() }, [id])

  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    try {
      await updateMinisterio(Number(id), { nombre: editNombre, descripcion: editDescripcion })
      setShowEditModal(false); load()
    } catch { alert('Error') } finally { setSaving(false) }
  }

  const openEdit = () => {
    if (!ministerio) return
    setEditNombre(ministerio.nombre); setEditDescripcion(ministerio.descripcion ?? '')
    setShowEditModal(true)
  }

  const handleAddIntegrante = async (intId: number) => {
    try { await addMinisterioIntegrante(Number(id), { integrante_id: intId, es_responsable: false }); load() } catch { alert('Error') }
    setAddIntSearch('')
  }

  const handleRemoveIntegrante = async (intId: number) => {
    if (!confirm('¿Quitar este integrante?')) return
    try { await removeMinisterioIntegrante(Number(id), intId); load() } catch { alert('Error') }
  }

  const handleAddTarefa = async () => {
    if (!newTarefaNombre.trim()) return
    try { await addMinisterioTarefa(Number(id), { nombre: newTarefaNombre }); setNewTarefaNombre(''); load() } catch { alert('Error') }
  }

  const handleDeleteTarefa = async (tid: number) => {
    if (!confirm('¿Eliminar esta tarea?')) return
    try { await deleteMinisterioTarefa(tid); load() } catch { alert('Error') }
  }

  const handleAddTarefaInt = async (tarefaId: number, intId: number) => {
    try { await addTarefaIntegrante(tarefaId, { integrante_id: intId }); load() } catch { alert('Error') }
    setTarefaIntSearch(p => ({ ...p, [tarefaId]: '' }))
  }

  const handleRemoveTarefaInt = async (tarefaId: number, intId: number) => {
    try { await removeTarefaIntegrante(tarefaId, intId); load() } catch { alert('Error') }
  }

  if (loading) return <div className="animate-pulse text-center py-20 text-grey-dark">Cargando...</div>
  if (!ministerio) return null

  const existingIds = new Set(ministerio.responsables?.map(r => r.id) ?? [])
  const filteredAdd = intList.filter(i => `${i.nombre} ${i.apellidos}`.toLowerCase().includes(addIntSearch.toLowerCase()) && !existingIds.has(i.id))

  return (
    <div className="flex flex-col gap-4 pb-20">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-grey-dark hover:text-primary w-fit">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" /></svg>
        Volver
      </button>

      {/* Bloco 1: Info */}
      <div className="card">
        <h2 className="text-2xl font-bold text-dark">{ministerio.nombre}</h2>
        {ministerio.descripcion && <p className="text-sm text-grey-dark mt-1">{ministerio.descripcion}</p>}
        {ministerio.responsables?.filter(r => r.es_responsable).length > 0 && (
          <div className="mt-3">
            <span className="text-xs text-grey-dark">Responsables: </span>
            {ministerio.responsables.filter(r => r.es_responsable).map(r => (
              <span key={r.id} className="inline-flex items-center gap-1 mr-2 text-sm text-dark font-bold">
                {r.nombre} {r.apellidos}
                <button onClick={() => handleRemoveIntegrante(r.id)} className="text-grey-dark hover:text-red-500 text-xs">✕</button>
              </span>
            ))}
          </div>
        )}
        <div className="mt-3">
          <p className="text-xs text-grey-dark mb-1">Todos los integrantes ({ministerio.integrantes_count}):</p>
          <div className="flex flex-wrap gap-1">
            {ministerio.responsables?.map(r => (
              <span key={r.id} className="inline-flex items-center gap-1 px-2 py-0.5 rounded-badge text-xs bg-background text-dark">
                {r.nombre} {r.apellidos}
                <button onClick={() => handleRemoveIntegrante(r.id)} className="text-grey-dark hover:text-red-500">✕</button>
              </span>
            ))}
          </div>
          <div className="mt-2">
            <input className="input-field text-sm" placeholder="Añadir integrante..." value={addIntSearch} onChange={e => setAddIntSearch(e.target.value)} />
            {addIntSearch && filteredAdd.length > 0 && (
              <div className="border border-grey rounded-card mt-1 max-h-40 overflow-y-auto bg-white">
                {filteredAdd.slice(0, 8).map(i => (
                  <button key={i.id} type="button" onClick={() => handleAddIntegrante(i.id)} className="w-full text-left px-3 py-2 text-sm hover:bg-background">{i.nombre} {i.apellidos}</button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Bloco 2: Tarefas */}
      <div className="card">
        <h3 className="font-bold text-dark mb-3">Tareas</h3>
        <div className="flex gap-2 mb-4">
          <input className="input-field text-sm flex-1" placeholder="Nueva tarea..." value={newTarefaNombre} onChange={e => setNewTarefaNombre(e.target.value)} />
          <button onClick={handleAddTarefa} className="btn-primary text-sm px-4 py-2">Añadir</button>
        </div>
        <div className="flex flex-col gap-4">
          {ministerio.tarefas?.map(t => {
            const tSearch = tarefaIntSearch[t.id] ?? ''
            const existingTIds = new Set(t.integrantes?.map(i => i.id) ?? [])
            const filteredTInt = intList.filter(i => `${i.nombre} ${i.apellidos}`.toLowerCase().includes(tSearch.toLowerCase()) && !existingTIds.has(i.id))
            return (
              <div key={t.id} className="border border-grey rounded-card p-3">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-bold text-dark text-sm">{t.nombre}</h4>
                  <button onClick={() => handleDeleteTarefa(t.id)} className="text-xs text-red-500 hover:opacity-70">Eliminar</button>
                </div>
                <div className="flex flex-wrap gap-1 mb-2">
                  {t.integrantes?.map(i => (
                    <span key={i.id} className="inline-flex items-center gap-1 px-2 py-0.5 rounded-badge text-xs bg-[#72E6EA] text-dark">
                      {i.nombre} {i.apellidos}
                      <button onClick={() => handleRemoveTarefaInt(t.id, i.id)} className="hover:opacity-70">✕</button>
                    </span>
                  ))}
                </div>
                <div>
                  <input className="input-field text-sm" placeholder="Añadir integrante a tarea..." value={tSearch} onChange={e => setTarefaIntSearch(p => ({ ...p, [t.id]: e.target.value }))} />
                  {tSearch && filteredTInt.length > 0 && (
                    <div className="border border-grey rounded-card mt-1 max-h-32 overflow-y-auto bg-white">
                      {filteredTInt.slice(0, 6).map(i => (
                        <button key={i.id} type="button" onClick={() => handleAddTarefaInt(t.id, i.id)} className="w-full text-left px-3 py-2 text-sm hover:bg-background">{i.nombre} {i.apellidos}</button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )
          })}
          {(!ministerio.tarefas || ministerio.tarefas.length === 0) && <p className="text-sm text-grey-dark text-center py-2">Sin tareas registradas.</p>}
        </div>
      </div>

      <button onClick={openEdit} className="btn-primary w-full">EDITAR MINISTERIO</button>

      {showEditModal && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="card max-w-sm w-full">
            <h3 className="font-bold text-dark mb-3">Editar Ministerio</h3>
            <form onSubmit={handleEdit} className="flex flex-col gap-3">
              <input className="input-field" value={editNombre} onChange={e => setEditNombre(e.target.value)} placeholder="Nombre" />
              <textarea className="input-field" rows={3} value={editDescripcion} onChange={e => setEditDescripcion(e.target.value)} placeholder="Descripción..." />
              <div className="flex gap-3">
                <button type="submit" disabled={saving} className="btn-primary flex-1">{saving ? 'Guardando...' : 'Guardar'}</button>
                <button type="button" onClick={() => setShowEditModal(false)} className="btn-outline flex-1">Cancelar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
