import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getIntegrantes, getIntegrantesMapa, getGrupos, getMinisterios } from '../lib/api'
import type { Integrante, Grupo, Ministerio, MapPoint } from '../lib/types'
import MapaComponent from '../components/MapaComponent'

function Avatar({ nombre, apellidos, foto_url }: { nombre: string; apellidos: string; foto_url?: string }) {
  if (foto_url) return <img src={foto_url} alt={nombre} className="w-12 h-12 rounded-full object-cover flex-shrink-0" />
  const initials = `${nombre} ${apellidos}`.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
  return <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-white font-bold text-lg flex-shrink-0">{initials}</div>
}

export default function Integrantes() {
  const [integrantes, setIntegrantes] = useState<Integrante[]>([])
  const [grupos, setGrupos] = useState<Grupo[]>([])
  const [ministerios, setMinisterios] = useState<Ministerio[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [showFilter, setShowFilter] = useState(false)
  const [showMap, setShowMap] = useState(false)
  const [mapPoints, setMapPoints] = useState<MapPoint[]>([])

  const [filters, setFilters] = useState({
    is_membro: '',
    rol: '',
    grupo_id: '',
    ministerio_id: '',
    novo_crente: '',
    bautizado: '',
    novo_batizado: '',
    iglesia_procedente: '',
    discipulado_inicial: '',
    pre_batismo: '',
    escuela_biblica: '',
    escuela_discipulado: '',
    treinamento: '',
  })
  const [appliedFilters, setAppliedFilters] = useState(filters)

  useEffect(() => {
    Promise.all([
      getGrupos(),
      getMinisterios(),
    ]).then(([g, m]) => {
      setGrupos(g.data)
      setMinisterios(m.data)
    }).catch(() => {})
  }, [])

  useEffect(() => {
    setLoading(true)
    const params: Record<string, string> = {}
    Object.entries(appliedFilters).forEach(([k, v]) => { if (v) params[k] = v })
    getIntegrantes(params)
      .then(r => setIntegrantes(r.data))
      .catch(() => setIntegrantes([]))
      .finally(() => setLoading(false))
  }, [appliedFilters])

  useEffect(() => {
    if (showMap) {
      getIntegrantesMapa().then(r => setMapPoints(r.data)).catch(() => setMapPoints([]))
    }
  }, [showMap])

  const filtered = integrantes.filter(i => {
    const q = search.toLowerCase()
    return i.nombre.toLowerCase().includes(q) || i.apellidos.toLowerCase().includes(q) || (i.email ?? '').toLowerCase().includes(q)
  })

  const setF = (k: string, v: string) => setFilters(p => ({ ...p, [k]: v }))

  return (
    <div className="flex flex-col gap-4 pb-20">
      <div className="flex items-center gap-2">
        <input type="search" placeholder="Buscar integrante..." value={search} onChange={e => setSearch(e.target.value)} className="input-field flex-1" />
      </div>
      <div className="flex gap-2">
        <button onClick={() => setShowFilter(!showFilter)} className={`px-3 py-1.5 rounded-button text-sm font-bold border ${showFilter ? 'bg-primary text-white border-primary' : 'bg-white text-primary border-primary'}`}>FILTRAR</button>
        <button onClick={() => setShowMap(!showMap)} className={`px-3 py-1.5 rounded-button text-sm font-bold border ${showMap ? 'bg-primary text-white border-primary' : 'bg-white text-primary border-primary'}`}>MAPA</button>
      </div>

      {/* Filter panel */}
      {showFilter && (
        <div className="card border-2 border-primary">
          <h3 className="font-bold text-dark mb-3">Filtros</h3>
          <div className="flex flex-col gap-3">
            <div>
              <span className="text-xs text-grey-dark font-bold uppercase mb-1 block">Generales</span>
              <div className="flex flex-col gap-2">
                <select className="input-field" value={filters.is_membro} onChange={e => setF('is_membro', e.target.value)}>
                  <option value="">Todos (miembro/no miembro)</option>
                  <option value="true">Solo miembros</option>
                  <option value="false">No miembros</option>
                </select>
                <select className="input-field" value={filters.grupo_id} onChange={e => setF('grupo_id', e.target.value)}>
                  <option value="">Todos los grupos</option>
                  {grupos.map(g => <option key={g.id} value={g.id}>{g.nombre}</option>)}
                </select>
                <select className="input-field" value={filters.ministerio_id} onChange={e => setF('ministerio_id', e.target.value)}>
                  <option value="">Todos los ministerios</option>
                  {ministerios.map(m => <option key={m.id} value={m.id}>{m.nombre}</option>)}
                </select>
              </div>
            </div>
            <div>
              <span className="text-xs text-grey-dark font-bold uppercase mb-1 block">Fe</span>
              <div className="flex flex-col gap-2">
                <select className="input-field" value={filters.novo_crente} onChange={e => setF('novo_crente', e.target.value)}>
                  <option value="">Novo crente: todos</option>
                  <option value="true">Sí</option>
                  <option value="false">No</option>
                </select>
                <select className="input-field" value={filters.bautizado} onChange={e => setF('bautizado', e.target.value)}>
                  <option value="">Bautizado: todos</option>
                  <option value="true">Sí</option>
                  <option value="false">No</option>
                </select>
                <select className="input-field" value={filters.novo_batizado} onChange={e => setF('novo_batizado', e.target.value)}>
                  <option value="">Novo bautizado: todos</option>
                  <option value="true">Sí</option>
                  <option value="false">No</option>
                </select>
                <select className="input-field" value={filters.iglesia_procedente} onChange={e => setF('iglesia_procedente', e.target.value)}>
                  <option value="">Iglesia procedente: todos</option>
                  <option value="true">Sí</option>
                  <option value="false">No</option>
                </select>
              </div>
            </div>
            <div>
              <span className="text-xs text-grey-dark font-bold uppercase mb-1 block">Formación</span>
              {[
                { key: 'discipulado_inicial', label: 'Discipulado inicial' },
                { key: 'pre_batismo', label: 'Pre-bautismo' },
                { key: 'escuela_biblica', label: 'Escuela bíblica' },
                { key: 'escuela_discipulado', label: 'Escuela discipulado' },
                { key: 'treinamento', label: 'Entrenamiento' },
              ].map(({ key, label }) => (
                <select key={key} className="input-field mb-2" value={filters[key as keyof typeof filters]} onChange={e => setF(key, e.target.value)}>
                  <option value="">{label}: todos</option>
                  <option value="no_iniciado">No iniciado</option>
                  <option value="cursando">Cursando</option>
                  <option value="terminado">Terminado</option>
                </select>
              ))}
            </div>
            <button onClick={() => { setAppliedFilters(filters); setShowFilter(false) }} className="btn-primary w-full">APLICAR</button>
          </div>
        </div>
      )}

      {showMap && <MapaComponent points={mapPoints} height="300px" />}

      {loading ? (
        <div className="animate-pulse text-center py-8 text-grey-dark">Cargando...</div>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map(i => (
            <Link to={`/integrantes/${i.id}`} key={i.id}>
              <div className="card flex items-center gap-3">
                <Avatar nombre={i.nombre} apellidos={i.apellidos} foto_url={i.foto_url} />
                <div className="flex-1 min-w-0">
                  <p className="font-bold text-dark truncate">{i.nombre} {i.apellidos}</p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {i.grupos?.map(g => (
                      <span key={g.grupo_id} className="px-1.5 py-0.5 rounded-badge text-xs bg-[#72E6EA] text-dark">{g.grupo_nombre}</span>
                    ))}
                    {i.novo_crente && <span className="px-1.5 py-0.5 rounded-badge text-xs bg-[#45C1EE] text-white">Novo crente</span>}
                    {i.bautizado && <span className="px-1.5 py-0.5 rounded-badge text-xs bg-[#66B97B] text-white">Bautizado</span>}
                    {i.novo_batizado && <span className="px-1.5 py-0.5 rounded-badge text-xs bg-[#BCD11A] text-dark">Novo bautizado</span>}
                  </div>
                </div>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="#CBCBCB"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" /></svg>
              </div>
            </Link>
          ))}
          {filtered.length === 0 && <div className="card text-center py-8 text-grey-dark">No se encontraron integrantes.</div>}
        </div>
      )}

      <Link to="/integrantes/nuevo" className="fixed bottom-4 right-4 left-4 z-10">
        <button className="btn-primary w-full">NUEVO INTEGRANTE</button>
      </Link>
    </div>
  )
}
