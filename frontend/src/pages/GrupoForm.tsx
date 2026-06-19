import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getGrupo, createGrupo, updateGrupo, getGrupos, getIntegrantes, getGrupoIntegrantes } from '../lib/api'
import type { Grupo, Integrante, DiaSemana, Frecuencia } from '../lib/types'

interface GrupoIntegranteEntry { id: number; nombre: string; apellidos: string; rol_en_grupo: string }

export default function GrupoForm() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  const [gruposList, setGruposList] = useState<Grupo[]>([])
  const [intList, setIntList] = useState<Integrante[]>([])
  const [saving, setSaving] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [nombre, setNombre] = useState('')
  const [grupoPaiId, setGrupoPaiId] = useState('')
  const [responsableId, setResponsableId] = useState('')
  const [responsableSearch, setResponsableSearch] = useState('')
  const [ayudanteId, setAyudanteId] = useState('')
  const [ayudanteSearch, setAyudanteSearch] = useState('')
  const [supervisorId, setSupervisorId] = useState('')
  const [supervisorSearch, setSupervisorSearch] = useState('')
  const [diaSemana, setDiaSemana] = useState<DiaSemana | ''>('')
  const [hora, setHora] = useState('')
  const [frecuencia, setFrecuencia] = useState<Frecuencia | ''>('')
  const [endereco, setEndereco] = useState('')
  const [observaciones, setObservaciones] = useState('')
  const [integrantes, setIntegrantes] = useState<GrupoIntegranteEntry[]>([])
  const [intSearch, setIntSearch] = useState('')

  useEffect(() => {
    Promise.all([
      getGrupos({ activo: true }),
      getIntegrantes({ activo: true }),
    ]).then(([g, i]) => {
      setGruposList(g.data)
      setIntList(i.data)
    }).catch(() => {})

    if (isEdit) {
      setLoading(true)
      Promise.all([
        getGrupo(Number(id)),
        getGrupoIntegrantes(Number(id)),
      ]).then(([g, gi]) => {
        const d: Grupo = g.data
        setNombre(d.nombre)
        setGrupoPaiId(d.grupo_pai_id ? String(d.grupo_pai_id) : '')
        setResponsableId(d.responsable_id ? String(d.responsable_id) : '')
        setAyudanteId(d.ayudante_id ? String(d.ayudante_id) : '')
        setSupervisorId(d.supervisor_id ? String(d.supervisor_id) : '')
        setDiaSemana(d.dia_semana ?? '')
        setHora(d.hora ?? '')
        setFrecuencia(d.frecuencia ?? '')
        setEndereco(d.endereco ?? '')
        setObservaciones(d.observaciones ?? '')
        if (gi.data) setIntegrantes(gi.data.map((i: any) => ({ id: i.id, nombre: i.nombre, apellidos: i.apellidos, rol_en_grupo: i.rol_en_grupo ?? '' })))
      }).catch(() => navigate('/grupos')).finally(() => setLoading(false))
    }
  }, [id])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!nombre.trim()) { setError('El nombre es obligatorio'); return }
    setSaving(true); setError('')
    try {
      const payload = {
        nombre,
        grupo_pai_id: grupoPaiId ? Number(grupoPaiId) : null,
        responsable_id: responsableId ? Number(responsableId) : null,
        ayudante_id: ayudanteId ? Number(ayudanteId) : null,
        supervisor_id: supervisorId ? Number(supervisorId) : null,
        dia_semana: diaSemana || null,
        hora: hora || null,
        frecuencia: frecuencia || null,
        endereco: endereco || null,
        observaciones: observaciones || null,
        integrantes: integrantes.map(i => ({ integrante_id: i.id, rol_en_grupo: i.rol_en_grupo })),
      }
      if (isEdit) {
        await updateGrupo(Number(id), payload)
        navigate(`/grupos/${id}`)
      } else {
        const r = await createGrupo(payload)
        navigate(`/grupos/${r.data.id}`)
      }
    } catch {
      setError('Error al guardar. Revisa los datos.')
    } finally { setSaving(false) }
  }

  const addIntegrante = (i: Integrante) => {
    if (!integrantes.find(ei => ei.id === i.id)) {
      setIntegrantes(prev => [...prev, { id: i.id, nombre: i.nombre, apellidos: i.apellidos, rol_en_grupo: '' }])
    }
    setIntSearch('')
  }
  const removeIntegrante = (iid: number) => setIntegrantes(prev => prev.filter(i => i.id !== iid))
  const updateIntRol = (iid: number, rol: string) => setIntegrantes(prev => prev.map(i => i.id === iid ? { ...i, rol_en_grupo: rol } : i))

  const filteredIntList = intList.filter(i => {
    const q = intSearch.toLowerCase()
    return (i.nombre.toLowerCase().includes(q) || i.apellidos.toLowerCase().includes(q)) && !integrantes.find(ei => ei.id === i.id)
  })

  const selectedResponsable = intList.find(i => String(i.id) === responsableId)
  const selectedAyudante = intList.find(i => String(i.id) === ayudanteId)
  const selectedSupervisor = intList.find(i => String(i.id) === supervisorId)

  const filteredForRol = (search: string, excludeIds: string[]) => intList.filter(i => {
    const q = search.toLowerCase()
    return (i.nombre.toLowerCase().includes(q) || i.apellidos.toLowerCase().includes(q)) && !excludeIds.includes(String(i.id))
  })

  if (loading) return <div className="animate-pulse text-center py-20 text-grey-dark">Cargando...</div>

  return (
    <div className="flex flex-col gap-4 pb-24">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-grey-dark hover:text-primary w-fit">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" /></svg>
        Volver
      </button>
      <h2 className="section-title">{isEdit ? 'Editar Grupo' : 'Nuevo Grupo'}</h2>

      {error && <div className="bg-red-100 border border-red-300 text-red-700 rounded-card p-3 text-sm">{error}</div>}

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Datos del grupo</h3>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Nombre *</label>
            <input className="input-field" value={nombre} onChange={e => setNombre(e.target.value)} placeholder="Nombre del grupo" />
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Grupo padre</label>
            <select className="input-field" value={grupoPaiId} onChange={e => setGrupoPaiId(e.target.value)}>
              <option value="">Sin grupo padre</option>
              {gruposList.filter(g => !isEdit || g.id !== Number(id)).map(g => <option key={g.id} value={g.id}>{g.nombre}</option>)}
            </select>
          </div>
        </div>

        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Responsables</h3>
          {[
            { label: 'Responsable', search: responsableSearch, setSearch: setResponsableSearch, selected: selectedResponsable, setId: setResponsableId, currentId: responsableId },
            { label: 'Ayudante', search: ayudanteSearch, setSearch: setAyudanteSearch, selected: selectedAyudante, setId: setAyudanteId, currentId: ayudanteId },
            { label: 'Supervisor', search: supervisorSearch, setSearch: setSupervisorSearch, selected: selectedSupervisor, setId: setSupervisorId, currentId: supervisorId },
          ].map(({ label, search, setSearch, selected, setId }) => (
            <div key={label}>
              <label className="text-xs text-grey-dark mb-1 block">{label}</label>
              {selected ? (
                <div className="flex items-center gap-2 bg-background rounded-card p-2">
                  <span className="flex-1 text-sm">{selected.nombre} {selected.apellidos}</span>
                  <button type="button" onClick={() => { setId(''); setSearch('') }} className="text-xs text-red-500">✕</button>
                </div>
              ) : (
                <div>
                  <input className="input-field" placeholder={`Buscar ${label.toLowerCase()}...`} value={search} onChange={e => setSearch(e.target.value)} />
                  {search && (
                    <div className="border border-grey rounded-card mt-1 max-h-32 overflow-y-auto bg-white">
                      {filteredForRol(search, [responsableId, ayudanteId, supervisorId].filter(Boolean)).slice(0, 8).map(i => (
                        <button key={i.id} type="button" onClick={() => { setId(String(i.id)); setSearch('') }} className="w-full text-left px-3 py-2 text-sm hover:bg-background">{i.nombre} {i.apellidos}</button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Horario</h3>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Día de la semana</label>
            <select className="input-field" value={diaSemana} onChange={e => setDiaSemana(e.target.value as DiaSemana)}>
              <option value="">Sin día fijo</option>
              {['lunes','martes','miercoles','jueves','viernes','sabado','domingo'].map(d => <option key={d} value={d} className="capitalize">{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
            </select>
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Hora</label>
            <input type="time" className="input-field" value={hora} onChange={e => setHora(e.target.value)} />
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Frecuencia</label>
            <select className="input-field" value={frecuencia} onChange={e => setFrecuencia(e.target.value as Frecuencia)}>
              <option value="">Sin frecuencia fija</option>
              <option value="semanal">Semanal</option>
              <option value="quincenal">Quincenal</option>
              <option value="mensual">Mensual</option>
            </select>
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Dirección</label>
            <input className="input-field" value={endereco} onChange={e => setEndereco(e.target.value)} placeholder="Calle, ciudad..." />
          </div>
        </div>

        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Integrantes</h3>
          <div>
            <input className="input-field" placeholder="Buscar integrante..." value={intSearch} onChange={e => setIntSearch(e.target.value)} />
            {intSearch && filteredIntList.length > 0 && (
              <div className="border border-grey rounded-card mt-1 max-h-40 overflow-y-auto bg-white">
                {filteredIntList.slice(0, 10).map(i => (
                  <button key={i.id} type="button" onClick={() => addIntegrante(i)} className="w-full text-left px-3 py-2 text-sm hover:bg-background">{i.nombre} {i.apellidos}</button>
                ))}
              </div>
            )}
          </div>
          {integrantes.map(i => (
            <div key={i.id} className="flex items-center gap-2 bg-background rounded-card p-2">
              <span className="flex-1 text-sm">{i.nombre} {i.apellidos}</span>
              <select className="text-xs border border-grey rounded px-1 py-0.5" value={i.rol_en_grupo} onChange={e => updateIntRol(i.id, e.target.value)}>
                <option value="">Sin rol</option>
                <option value="ayudante">Ayudante</option>
                <option value="responsable">Responsable</option>
                <option value="supervisor">Supervisor</option>
              </select>
              <button type="button" onClick={() => removeIntegrante(i.id)} className="text-red-500 text-xs">✕</button>
            </div>
          ))}
        </div>

        <div className="card">
          <h3 className="font-bold text-dark mb-2">Observaciones</h3>
          <textarea className="input-field" rows={4} value={observaciones} onChange={e => setObservaciones(e.target.value)} placeholder="Notas..." />
        </div>

        <div className="fixed bottom-4 right-4 left-4 z-10 flex flex-col gap-2">
          <button type="submit" disabled={saving} className="btn-primary w-full">{saving ? 'Guardando...' : isEdit ? 'GUARDAR CAMBIOS' : 'CREAR GRUPO'}</button>
          <button type="button" onClick={() => navigate(-1)} className="btn-outline w-full">CANCELAR</button>
        </div>
      </form>
    </div>
  )
}
