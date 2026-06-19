import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getGrupos, getGruposMapa } from '../lib/api'
import type { Grupo, MapPoint } from '../lib/types'
import MapaComponent from '../components/MapaComponent'

export default function Grupos() {
  const [grupos, setGrupos] = useState<Grupo[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [showFilter, setShowFilter] = useState(false)
  const [showMap, setShowMap] = useState(false)
  const [mapPoints, setMapPoints] = useState<MapPoint[]>([])
  const [frecuenciaFilter, setFrecuenciaFilter] = useState('')
  const [diaFilter, setDiaFilter] = useState('')
  const [appliedFrecuencia, setAppliedFrecuencia] = useState('')
  const [appliedDia, setAppliedDia] = useState('')

  useEffect(() => {
    const params: Record<string, string> = {}
    if (appliedFrecuencia) params.frecuencia = appliedFrecuencia
    if (appliedDia) params.dia_semana = appliedDia
    setLoading(true)
    getGrupos(params).then(r => setGrupos(r.data)).catch(() => setGrupos([])).finally(() => setLoading(false))
  }, [appliedFrecuencia, appliedDia])

  useEffect(() => {
    if (showMap) {
      getGruposMapa().then(r => setMapPoints(r.data)).catch(() => setMapPoints([]))
    }
  }, [showMap])

  const filtered = grupos.filter(g => {
    const q = search.toLowerCase()
    return g.nombre.toLowerCase().includes(q) || (g.responsable_nombre ?? '').toLowerCase().includes(q) || (g.supervisor_nombre ?? '').toLowerCase().includes(q)
  })

  const frecBadge = (f?: string) => {
    if (f === 'semanal') return 'bg-[#66B97B] text-white'
    if (f === 'quincenal') return 'bg-[#BCD11A] text-dark'
    if (f === 'mensual') return 'bg-[#45C1EE] text-white'
    return 'bg-grey text-dark'
  }

  return (
    <div className="flex flex-col gap-4 pb-20">
      <input type="search" placeholder="Buscar grupo..." value={search} onChange={e => setSearch(e.target.value)} className="input-field" />
      <div className="flex gap-2">
        <button onClick={() => setShowFilter(!showFilter)} className={`px-3 py-1.5 rounded-button text-sm font-bold border ${showFilter ? 'bg-primary text-white border-primary' : 'bg-white text-primary border-primary'}`}>FILTRAR</button>
        <button onClick={() => setShowMap(!showMap)} className={`px-3 py-1.5 rounded-button text-sm font-bold border ${showMap ? 'bg-primary text-white border-primary' : 'bg-white text-primary border-primary'}`}>MAPA</button>
      </div>

      {showFilter && (
        <div className="card border-2 border-primary">
          <h3 className="font-bold text-dark mb-3">Filtros</h3>
          <div className="flex flex-col gap-2">
            <select className="input-field" value={frecuenciaFilter} onChange={e => setFrecuenciaFilter(e.target.value)}>
              <option value="">Frecuencia: todas</option>
              <option value="semanal">Semanal</option>
              <option value="quincenal">Quincenal</option>
              <option value="mensual">Mensual</option>
            </select>
            <select className="input-field" value={diaFilter} onChange={e => setDiaFilter(e.target.value)}>
              <option value="">Día: todos</option>
              <option value="lunes">Lunes</option>
              <option value="martes">Martes</option>
              <option value="miercoles">Miércoles</option>
              <option value="jueves">Jueves</option>
              <option value="viernes">Viernes</option>
              <option value="sabado">Sábado</option>
              <option value="domingo">Domingo</option>
            </select>
            <button onClick={() => { setAppliedFrecuencia(frecuenciaFilter); setAppliedDia(diaFilter); setShowFilter(false) }} className="btn-primary w-full">APLICAR</button>
          </div>
        </div>
      )}

      {showMap && <MapaComponent points={mapPoints} height="300px" />}

      {loading ? (
        <div className="animate-pulse text-center py-8 text-grey-dark">Cargando...</div>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map(g => (
            <Link to={`/grupos/${g.id}`} key={g.id}>
              <div className="card hover:shadow-lg transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-dark">{g.nombre}</h3>
                  <span className="px-2 py-0.5 rounded-full bg-primary text-white text-xs font-bold">{g.integrantes_count}</span>
                </div>
                <div className="flex flex-wrap items-center gap-2 text-sm text-grey-dark">
                  {g.dia_semana && <span className="capitalize">{g.dia_semana}</span>}
                  {g.hora && <span>{g.hora}</span>}
                  {g.frecuencia && <span className={`px-2 py-0.5 rounded-badge text-xs font-bold ${frecBadge(g.frecuencia)}`}>{g.frecuencia}</span>}
                </div>
                {g.responsable_nombre && <p className="text-xs text-dark mt-1">Responsable: <span className="text-primary font-bold">{g.responsable_nombre}</span></p>}
                {g.supervisor_nombre && <p className="text-xs text-dark">Supervisor: <span className="font-bold">{g.supervisor_nombre}</span></p>}
              </div>
            </Link>
          ))}
          {filtered.length === 0 && <div className="card text-center py-8 text-grey-dark">No se encontraron grupos.</div>}
        </div>
      )}

      <Link to="/grupos/nuevo" className="fixed bottom-4 right-4 left-4 z-10">
        <button className="btn-primary w-full">NUEVO GRUPO</button>
      </Link>
    </div>
  )
}
