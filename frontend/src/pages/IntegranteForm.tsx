import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getIntegrante, createIntegrante, updateIntegrante, getGrupos, getMinisterios } from '../lib/api'
import type { Grupo, Ministerio, EstadoFormacion } from '../lib/types'

const FORMACION_OPTIONS = [
  { value: 'no_iniciado', label: 'No iniciado' },
  { value: 'cursando', label: 'Cursando' },
  { value: 'terminado', label: 'Terminado' },
]

interface GrupoEntry { grupo_id: number; grupo_nombre: string; rol_en_grupo: string }
interface MinisterioEntry { id: number; nombre: string; es_responsable: boolean }

export default function IntegranteForm() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  const [grupos, setGrupos] = useState<Grupo[]>([])
  const [ministeriosList, setMinisteriosList] = useState<Ministerio[]>([])
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const [nombre, setNombre] = useState('')
  const [apellidos, setApellidos] = useState('')
  const [email, setEmail] = useState('')
  const [telefono, setTelefono] = useState('')
  const [fechaNacimiento, setFechaNacimiento] = useState('')
  const [endereco, setEndereco] = useState('')
  const [isMembro, setIsMembro] = useState(false)
  const [numeroMembro, setNumeroMembro] = useState('')
  const [novoCrente, setNovoCrente] = useState(false)
  const [novoBatizado, setNovoBatizado] = useState(false)
  const [bautizado, setBautizado] = useState(false)
  const [dataBatismo, setDataBatismo] = useState('')
  const [iglejaProcedente, setIgrejaProcedente] = useState(false)
  const [igrejaNome, setIgrejaNome] = useState('')
  const [igrejaData, setIgrejaData] = useState('')
  const [discipulado, setDiscipulado] = useState<EstadoFormacion>('no_iniciado')
  const [preBatismo, setPreBatismo] = useState<EstadoFormacion>('no_iniciado')
  const [escuelaBiblica, setEscuelaBiblica] = useState<EstadoFormacion>('no_iniciado')
  const [escuelaDiscipulado, setEscuelaDiscipulado] = useState<EstadoFormacion>('no_iniciado')
  const [treinamento, setTreinamento] = useState<EstadoFormacion>('no_iniciado')
  const [observaciones, setObservaciones] = useState('')
  const [selectedGrupos, setSelectedGrupos] = useState<GrupoEntry[]>([])
  const [selectedMinisterios, setSelectedMinisterios] = useState<MinisterioEntry[]>([])
  const [grupoSearch, setGrupoSearch] = useState('')
  const [ministerioSearch, setMinisterioSearch] = useState('')

  useEffect(() => {
    Promise.all([
      getGrupos({ activo: true }),
      getMinisterios(),
    ]).then(([g, m]) => {
      setGrupos(g.data)
      setMinisteriosList(m.data)
    }).catch(() => {})

    if (isEdit) {
      setLoading(true)
      getIntegrante(Number(id)).then(r => {
        const d = r.data
        setNombre(d.nombre)
        setApellidos(d.apellidos)
        setEmail(d.email ?? '')
        setTelefono(d.telefono ?? '')
        setFechaNacimiento(d.fecha_nacimiento ?? '')
        setEndereco(d.endereco ?? '')
        setIsMembro(d.is_membro)
        setNumeroMembro(d.numero_membro ? String(d.numero_membro) : '')
        setNovoCrente(d.novo_crente)
        setNovoBatizado(d.novo_batizado)
        setBautizado(d.bautizado)
        setDataBatismo(d.data_batismo ?? '')
        setIgrejaProcedente(d.iglesia_procedente)
        setIgrejaNome(d.iglesia_procedente_nome ?? '')
        setIgrejaData(d.data_iglesia_procedente ?? '')
        setDiscipulado(d.discipulado_inicial)
        setPreBatismo(d.pre_batismo)
        setEscuelaBiblica(d.escuela_biblica)
        setEscuelaDiscipulado(d.escuela_discipulado)
        setTreinamento(d.treinamento)
        setObservaciones(d.observaciones ?? '')
        if (d.grupos) setSelectedGrupos(d.grupos.map((g: any) => ({ grupo_id: g.grupo_id, grupo_nombre: g.grupo_nombre, rol_en_grupo: g.rol_en_grupo ?? '' })))
        if (d.ministerios) setSelectedMinisterios(d.ministerios.map((m: any) => ({ id: m.id, nombre: m.nombre, es_responsable: m.es_responsable })))
      }).catch(() => navigate('/integrantes')).finally(() => setLoading(false))
    }
  }, [id])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!nombre.trim() || !apellidos.trim()) { setError('Nombre y apellidos son obligatorios'); return }
    setSaving(true); setError('')
    try {
      const payload = {
        nombre, apellidos, email: email || null, telefono: telefono || null,
        fecha_nacimiento: fechaNacimiento || null, endereco: endereco || null,
        is_membro: isMembro, numero_membro: numeroMembro ? Number(numeroMembro) : null,
        novo_crente: novoCrente, novo_batizado: novoBatizado, bautizado,
        data_batismo: dataBatismo || null, iglesia_procedente: iglejaProcedente,
        iglesia_procedente_nome: igrejaNome || null, data_iglesia_procedente: igrejaData || null,
        discipulado_inicial: discipulado, pre_batismo: preBatismo,
        escuela_biblica: escuelaBiblica, escuela_discipulado: escuelaDiscipulado,
        treinamento, observaciones: observaciones || null,
        grupos: selectedGrupos, ministerios: selectedMinisterios,
      }
      if (isEdit) {
        await updateIntegrante(Number(id), payload)
        navigate(`/integrantes/${id}`)
      } else {
        const r = await createIntegrante(payload)
        navigate(`/integrantes/${r.data.id}`)
      }
    } catch (err: any) {
      setError('Error al guardar. Revisa los datos e inténtalo de nuevo.')
    } finally { setSaving(false) }
  }

  const addGrupo = (g: Grupo) => {
    if (!selectedGrupos.find(sg => sg.grupo_id === g.id)) {
      setSelectedGrupos(prev => [...prev, { grupo_id: g.id, grupo_nombre: g.nombre, rol_en_grupo: '' }])
    }
    setGrupoSearch('')
  }

  const removeGrupo = (gid: number) => setSelectedGrupos(prev => prev.filter(g => g.grupo_id !== gid))
  const updateGrupoRol = (gid: number, rol: string) => setSelectedGrupos(prev => prev.map(g => g.grupo_id === gid ? { ...g, rol_en_grupo: rol } : g))

  const addMinisterio = (m: Ministerio) => {
    if (!selectedMinisterios.find(sm => sm.id === m.id)) {
      setSelectedMinisterios(prev => [...prev, { id: m.id, nombre: m.nombre, es_responsable: false }])
    }
    setMinisterioSearch('')
  }
  const removeMinisterio = (mid: number) => setSelectedMinisterios(prev => prev.filter(m => m.id !== mid))
  const toggleMinisterioResp = (mid: number) => setSelectedMinisterios(prev => prev.map(m => m.id === mid ? { ...m, es_responsable: !m.es_responsable } : m))

  const filteredGrupos = grupos.filter(g => g.nombre.toLowerCase().includes(grupoSearch.toLowerCase()) && !selectedGrupos.find(sg => sg.grupo_id === g.id))
  const filteredMinisterios = ministeriosList.filter(m => m.nombre.toLowerCase().includes(ministerioSearch.toLowerCase()) && !selectedMinisterios.find(sm => sm.id === m.id))

  if (loading) return <div className="animate-pulse text-center py-20 text-grey-dark">Cargando...</div>

  return (
    <div className="flex flex-col gap-4 pb-24">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1 text-sm text-grey-dark hover:text-primary w-fit">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" /></svg>
        Volver
      </button>
      <h2 className="section-title">{isEdit ? 'Editar Integrante' : 'Nuevo Integrante'}</h2>

      {error && <div className="bg-red-100 border border-red-300 text-red-700 rounded-card p-3 text-sm">{error}</div>}

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {/* Datos personales */}
        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Datos personales</h3>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Nombre *</label>
            <input className="input-field" value={nombre} onChange={e => setNombre(e.target.value)} placeholder="Nombre" />
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Apellidos *</label>
            <input className="input-field" value={apellidos} onChange={e => setApellidos(e.target.value)} placeholder="Apellidos" />
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Fecha de nacimiento</label>
            <input type="date" className="input-field" value={fechaNacimiento} onChange={e => setFechaNacimiento(e.target.value)} />
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Teléfono</label>
            <input type="tel" className="input-field" value={telefono} onChange={e => setTelefono(e.target.value)} placeholder="+34 600 000 000" />
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Email</label>
            <input type="email" className="input-field" value={email} onChange={e => setEmail(e.target.value)} placeholder="email@ejemplo.com" />
          </div>
          <div>
            <label className="text-xs text-grey-dark mb-1 block">Dirección</label>
            <input className="input-field" value={endereco} onChange={e => setEndereco(e.target.value)} placeholder="Calle, ciudad..." />
          </div>
        </div>

        {/* Miembro */}
        <div className="card flex flex-col gap-3">
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" checked={isMembro} onChange={e => setIsMembro(e.target.checked)} className="w-5 h-5 accent-primary" />
            <span className="font-bold text-dark">¿Es miembro?</span>
          </label>
          {isMembro && (
            <div>
              <label className="text-xs text-grey-dark mb-1 block">Número de miembro</label>
              <input className="input-field" value={numeroMembro} onChange={e => setNumeroMembro(e.target.value)} placeholder="001" />
            </div>
          )}
        </div>

        {/* Grupos */}
        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Grupo de Hogar</h3>
          <div>
            <input className="input-field" placeholder="Buscar grupo..." value={grupoSearch} onChange={e => setGrupoSearch(e.target.value)} />
            {grupoSearch && filteredGrupos.length > 0 && (
              <div className="border border-grey rounded-card mt-1 max-h-40 overflow-y-auto bg-white">
                {filteredGrupos.map(g => (
                  <button key={g.id} type="button" onClick={() => addGrupo(g)} className="w-full text-left px-3 py-2 text-sm hover:bg-background">{g.nombre}</button>
                ))}
              </div>
            )}
          </div>
          {selectedGrupos.map(sg => (
            <div key={sg.grupo_id} className="flex items-center gap-2 bg-background rounded-card p-2">
              <span className="flex-1 text-sm text-dark">{sg.grupo_nombre}</span>
              <select className="text-xs border border-grey rounded px-1 py-0.5" value={sg.rol_en_grupo} onChange={e => updateGrupoRol(sg.grupo_id, e.target.value)}>
                <option value="">Sin rol</option>
                <option value="ayudante">Ayudante</option>
                <option value="responsable">Responsable</option>
                <option value="supervisor">Supervisor</option>
              </select>
              <button type="button" onClick={() => removeGrupo(sg.grupo_id)} className="text-red-500 text-xs hover:opacity-70">✕</button>
            </div>
          ))}
        </div>

        {/* Formación */}
        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Formación</h3>
          {[
            { label: 'Discipulado inicial', value: discipulado, set: setDiscipulado },
            { label: 'Pre-bautismo', value: preBatismo, set: setPreBatismo },
            { label: 'Escuela bíblica', value: escuelaBiblica, set: setEscuelaBiblica },
            { label: 'Escuela discipulado', value: escuelaDiscipulado, set: setEscuelaDiscipulado },
            { label: 'Entrenamiento', value: treinamento, set: setTreinamento },
          ].map(({ label, value, set }) => (
            <div key={label}>
              <label className="text-xs text-grey-dark mb-1 block">{label}</label>
              <select className="input-field" value={value} onChange={e => set(e.target.value as EstadoFormacion)}>
                {FORMACION_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
              </select>
            </div>
          ))}
        </div>

        {/* Fe */}
        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Fe</h3>
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" checked={novoCrente} onChange={e => setNovoCrente(e.target.checked)} className="w-5 h-5 accent-primary" />
            <span className="text-sm text-dark">Novo crente</span>
          </label>
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" checked={novoBatizado} onChange={e => setNovoBatizado(e.target.checked)} className="w-5 h-5 accent-primary" />
            <span className="text-sm text-dark">Novo bautizado</span>
          </label>
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" checked={bautizado} onChange={e => setBautizado(e.target.checked)} className="w-5 h-5 accent-primary" />
            <span className="text-sm text-dark">Bautizado</span>
          </label>
          {bautizado && (
            <div>
              <label className="text-xs text-grey-dark mb-1 block">Fecha de bautismo</label>
              <input type="date" className="input-field" value={dataBatismo} onChange={e => setDataBatismo(e.target.value)} />
            </div>
          )}
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" checked={iglejaProcedente} onChange={e => setIgrejaProcedente(e.target.checked)} className="w-5 h-5 accent-primary" />
            <span className="text-sm text-dark">Iglesia de procedencia</span>
          </label>
          {iglejaProcedente && (
            <>
              <div>
                <label className="text-xs text-grey-dark mb-1 block">Nombre de la iglesia</label>
                <input className="input-field" value={igrejaNome} onChange={e => setIgrejaNome(e.target.value)} placeholder="Nombre de la iglesia..." />
              </div>
              <div>
                <label className="text-xs text-grey-dark mb-1 block">Fecha</label>
                <input type="date" className="input-field" value={igrejaData} onChange={e => setIgrejaData(e.target.value)} />
              </div>
            </>
          )}
        </div>

        {/* Ministerios */}
        <div className="card flex flex-col gap-3">
          <h3 className="font-bold text-dark">Ministerios</h3>
          <div>
            <input className="input-field" placeholder="Buscar ministerio..." value={ministerioSearch} onChange={e => setMinisterioSearch(e.target.value)} />
            {ministerioSearch && filteredMinisterios.length > 0 && (
              <div className="border border-grey rounded-card mt-1 max-h-40 overflow-y-auto bg-white">
                {filteredMinisterios.map(m => (
                  <button key={m.id} type="button" onClick={() => addMinisterio(m)} className="w-full text-left px-3 py-2 text-sm hover:bg-background">{m.nombre}</button>
                ))}
              </div>
            )}
          </div>
          {selectedMinisterios.map(sm => (
            <div key={sm.id} className="flex items-center gap-2 bg-background rounded-card p-2">
              <span className="flex-1 text-sm text-dark">{sm.nombre}</span>
              <label className="flex items-center gap-1 text-xs text-grey-dark cursor-pointer">
                <input type="checkbox" checked={sm.es_responsable} onChange={() => toggleMinisterioResp(sm.id)} className="accent-primary" />
                Responsable
              </label>
              <button type="button" onClick={() => removeMinisterio(sm.id)} className="text-red-500 text-xs hover:opacity-70">✕</button>
            </div>
          ))}
        </div>

        {/* Observaciones */}
        <div className="card">
          <h3 className="font-bold text-dark mb-2">Observaciones</h3>
          <textarea className="input-field" rows={4} value={observaciones} onChange={e => setObservaciones(e.target.value)} placeholder="Notas adicionales..." />
        </div>

        <div className="fixed bottom-4 right-4 left-4 z-10 flex flex-col gap-2">
          <button type="submit" disabled={saving} className="btn-primary w-full">{saving ? 'Guardando...' : isEdit ? 'GUARDAR CAMBIOS' : 'CREAR INTEGRANTE'}</button>
          <button type="button" onClick={() => navigate(-1)} className="btn-outline w-full">CANCELAR</button>
        </div>
      </form>
    </div>
  )
}
