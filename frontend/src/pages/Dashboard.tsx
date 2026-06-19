import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getDashboardStats, getGruposMapa, getIntegrantesMapa } from '../lib/api'
import type { DashboardStats, MapPoint } from '../lib/types'
import MapaComponent from '../components/MapaComponent'

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

function StatCard2({ label, value, sub }: { label: string; value: number | string; sub?: string }) {
  return (
    <div className="bg-background rounded-card p-3 flex flex-col gap-1">
      <span className="text-2xl font-bold text-dark">{value}</span>
      <span className="text-xs text-grey-dark">{label}</span>
      {sub && <span className="text-xs text-grey-dark">{sub}</span>}
    </div>
  )
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [mapMode, setMapMode] = useState<'grupos' | 'integrantes'>('grupos')
  const [mapPoints, setMapPoints] = useState<MapPoint[]>([])
  const [mapLoading, setMapLoading] = useState(false)

  useEffect(() => {
    getDashboardStats()
      .then(r => setStats(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    setMapLoading(true)
    const fn = mapMode === 'grupos' ? getGruposMapa : getIntegrantesMapa
    fn().then(r => setMapPoints(r.data)).catch(() => setMapPoints([])).finally(() => setMapLoading(false))
  }, [mapMode])

  if (loading) return <div className="animate-pulse p-8 text-center text-grey-dark">Cargando...</div>
  if (!stats) return <div className="p-8 text-center text-red-500">Error al cargar estadísticas</div>

  const totalReuniones = stats.reuniones_periodicas + stats.reuniones_comunhao + stats.reuniones_evangelisticas
  const totalFrecuencia = stats.reuniones_semanais + stats.reuniones_quinzenais + stats.reuniones_mensais

  const formRows = [
    { label: 'Discipulado inicial', ni: stats.discipulado_no_iniciado, c: stats.discipulado_cursando, t: stats.discipulado_terminado },
    { label: 'Pre-bautismo', ni: stats.pre_batismo_no_iniciado, c: stats.pre_batismo_cursando, t: stats.pre_batismo_terminado },
    { label: 'Escuela bíblica', ni: stats.escuela_biblica_no_iniciado, c: stats.escuela_biblica_cursando, t: stats.escuela_biblica_terminado },
    { label: 'Escuela discipulado', ni: stats.escuela_discipulado_no_iniciado, c: stats.escuela_discipulado_cursando, t: stats.escuela_discipulado_terminado },
    { label: 'Entrenamiento', ni: stats.treinamento_no_iniciado, c: stats.treinamento_cursando, t: stats.treinamento_terminado },
  ]

  return (
    <div className="flex flex-col gap-4 pb-8">
      {/* Bloco 1: Welcome + testimonios */}
      <div className="card">
        <h1 className="font-bold text-dark text-base mb-3">Bienvenido a la gestión y seguimiento de Grupos de Hogar</h1>
        {stats.testimonios_destacados && stats.testimonios_destacados.length > 0 && (
          <div className="grid grid-cols-2 gap-3 mt-2">
            {stats.testimonios_destacados.slice(0, 4).map(t => (
              <div key={t.id} className="bg-background rounded-card p-3 flex flex-col gap-1">
                <span className="text-xs text-grey-dark">{t.fecha}</span>
                <span className="font-bold text-dark text-sm">{t.titulo}</span>
                {t.grupo_nombre && (
                  <span className="text-xs px-2 py-0.5 rounded-badge bg-[#72E6EA] text-dark w-fit">{t.grupo_nombre}</span>
                )}
                <p className="text-xs text-grey-dark line-clamp-2">{t.contenido}</p>
                <button onClick={() => navigate(`/testimonios/${t.id}`)} className="text-xs text-primary underline text-left mt-1">Leer más →</button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Bloco 2: Grupos de Hogar stats */}
      <div className="card">
        <h2 className="font-bold text-dark text-base mb-3">Grupos de Hogar</h2>
        <div className="grid grid-cols-2 gap-2">
          <StatCard2 label="Grupos" value={stats.total_grupos} />
          <StatCard2 label="Integrantes" value={stats.total_integrantes} />
          <StatCard2 label="Miembros" value={stats.total_membros} />
          <StatCard2 label="Sin grupo" value={stats.integrantes_sin_grupo} sub={`${stats.integrantes_sin_grupo_pct ?? 0}%`} />
          <StatCard2 label="En ministerio" value={stats.total_en_ministerio} />
          <div className="bg-background rounded-card p-3 flex flex-col gap-1">
            <span className="text-xs text-grey-dark">Roles</span>
            <span className="text-xs text-dark">Supervisores: <b>{stats.supervisores_count}</b></span>
            <span className="text-xs text-dark">Responsables: <b>{stats.responsables_count}</b></span>
            <span className="text-xs text-dark">Ayudantes: <b>{stats.ayudantes_count}</b></span>
          </div>
        </div>
      </div>

      {/* Bloco 3: Fe */}
      <div className="card">
        <h2 className="font-bold text-dark text-base mb-3">Fe</h2>
        <div className="grid grid-cols-2 gap-2">
          <StatCard2 label="Visitantes" value={stats.total_visitantes} sub={`~${stats.avg_visitantes_por_grupo ?? 0} por grupo`} />
          <StatCard2 label="Novos crentes" value={stats.total_novos_crentes} sub={`~${stats.avg_novos_crentes_por_grupo ?? 0} por grupo`} />
          <StatCard2 label="Bautizados" value={stats.total_batizados} />
          <StatCard2 label="De otra iglesia" value={stats.total_de_outra_igreja} />
        </div>
      </div>

      {/* Bloco 4: Reuniones */}
      <div className="card">
        <h2 className="font-bold text-dark text-base mb-3">Reuniones</h2>
        <div className="mb-2">
          <span className="text-xs text-grey-dark mb-1 block">Por tipo</span>
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 rounded-badge bg-[#66B97B] text-white text-xs">Periódica: {stats.reuniones_periodicas} {totalReuniones > 0 ? `(${Math.round(stats.reuniones_periodicas/totalReuniones*100)}%)` : ''}</span>
            <span className="px-2 py-1 rounded-badge bg-[#45C1EE] text-white text-xs">Comunhão: {stats.reuniones_comunhao} {totalReuniones > 0 ? `(${Math.round(stats.reuniones_comunhao/totalReuniones*100)}%)` : ''}</span>
            <span className="px-2 py-1 rounded-badge bg-[#BCD11A] text-dark text-xs">Evangelística: {stats.reuniones_evangelisticas} {totalReuniones > 0 ? `(${Math.round(stats.reuniones_evangelisticas/totalReuniones*100)}%)` : ''}</span>
          </div>
        </div>
        <div>
          <span className="text-xs text-grey-dark mb-1 block">Por frecuencia</span>
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 rounded-badge bg-[#66B97B] text-white text-xs">Semanal: {stats.reuniones_semanais} {totalFrecuencia > 0 ? `(${Math.round(stats.reuniones_semanais/totalFrecuencia*100)}%)` : ''}</span>
            <span className="px-2 py-1 rounded-badge bg-[#BCD11A] text-dark text-xs">Quinzenal: {stats.reuniones_quinzenais} {totalFrecuencia > 0 ? `(${Math.round(stats.reuniones_quinzenais/totalFrecuencia*100)}%)` : ''}</span>
            <span className="px-2 py-1 rounded-badge bg-[#45C1EE] text-white text-xs">Mensual: {stats.reuniones_mensais} {totalFrecuencia > 0 ? `(${Math.round(stats.reuniones_mensais/totalFrecuencia*100)}%)` : ''}</span>
          </div>
        </div>
      </div>

      {/* Bloco 5: Mapa */}
      <div className="card">
        <h2 className="font-bold text-dark text-base mb-3">Ubicación</h2>
        <div className="flex gap-2 mb-3">
          <button onClick={() => setMapMode('grupos')} className={`px-4 py-1 rounded-button text-sm font-bold border transition-colors ${mapMode === 'grupos' ? 'bg-primary text-white border-primary' : 'bg-white text-primary border-primary'}`}>Grupos</button>
          <button onClick={() => setMapMode('integrantes')} className={`px-4 py-1 rounded-button text-sm font-bold border transition-colors ${mapMode === 'integrantes' ? 'bg-primary text-white border-primary' : 'bg-white text-primary border-primary'}`}>Integrantes</button>
        </div>
        {mapLoading ? <div className="animate-pulse h-[280px] bg-background rounded-lg flex items-center justify-center text-grey-dark">Cargando mapa...</div> : <MapaComponent points={mapPoints} height="280px" />}
      </div>

      {/* Bloco 6: Asistencia */}
      <div className="card">
        <h2 className="font-bold text-dark text-base mb-3">Asistencia</h2>
        <ProgressBar label="Último mes" value={stats.asistencia_ultimo_mes} total={stats.asistencia_total || 1} />
        <ProgressBar label="Último año" value={stats.asistencia_ultimo_ano} total={stats.asistencia_total || 1} />
        <ProgressBar label="Total histórico" value={stats.asistencia_total} total={stats.asistencia_total || 1} />
      </div>

      {/* Bloco 7: Formación */}
      <div className="card overflow-x-auto">
        <h2 className="font-bold text-dark text-base mb-3">Formación</h2>
        <table className="w-full text-xs">
          <thead>
            <tr className="text-grey-dark">
              <th className="text-left py-1 pr-2">Formación</th>
              <th className="text-center py-1">No iniciado</th>
              <th className="text-center py-1">Cursando</th>
              <th className="text-center py-1">Terminado</th>
            </tr>
          </thead>
          <tbody>
            {formRows.map(row => {
              const total = row.ni + row.c + row.t
              return (
                <tr key={row.label} className="border-t border-background">
                  <td className="py-1 pr-2 text-dark">{row.label}</td>
                  <td className="text-center py-1"><span className="bg-[#CBCBCB] text-dark px-1 rounded">{row.ni}{total > 0 ? ` (${Math.round(row.ni/total*100)}%)` : ''}</span></td>
                  <td className="text-center py-1"><span className="bg-[#BCD11A] text-dark px-1 rounded">{row.c}{total > 0 ? ` (${Math.round(row.c/total*100)}%)` : ''}</span></td>
                  <td className="text-center py-1"><span className="bg-[#66B97B] text-white px-1 rounded">{row.t}{total > 0 ? ` (${Math.round(row.t/total*100)}%)` : ''}</span></td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Bloco 8: Oración */}
      <div className="card">
        <h2 className="font-bold text-dark text-base mb-3">Oración</h2>
        <div className="flex gap-6">
          <div className="text-center">
            <div className="text-4xl font-bold text-dark">{stats.total_oraciones}</div>
            <div className="text-xs text-grey-dark mt-1">Total pedidos</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-primary">{stats.oraciones_respondidas}</div>
            <div className="text-xs text-grey-dark mt-1">Respondidas {stats.total_oraciones > 0 ? `(${Math.round(stats.oraciones_respondidas/stats.total_oraciones*100)}%)` : ''}</div>
          </div>
        </div>
      </div>
    </div>
  )
}
