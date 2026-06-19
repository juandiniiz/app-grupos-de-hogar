export type Rol = 'admin' | 'supervisor' | 'responsable' | 'ayudante'
export type EstadoFormacion = 'no_iniciado' | 'cursando' | 'terminado'
export type Frecuencia = 'semanal' | 'quincenal' | 'mensual'
export type TipoReunion = 'periodica' | 'comunhao' | 'evangelistica'
export type DiaSemana = 'lunes' | 'martes' | 'miercoles' | 'jueves' | 'viernes' | 'sabado' | 'domingo'

export interface User {
  id: number
  email: string
  nombre: string
  rol: Rol
  integrante_id?: number
}

export interface IntegranteGrupo {
  grupo_id: number
  grupo_nombre: string
  rol_en_grupo?: string
}

export interface IntegranteMinisterio {
  id: number
  nombre: string
  es_responsable: boolean
}

export interface Integrante {
  id: number
  nombre: string
  apellidos: string
  email?: string
  telefono?: string
  fecha_nacimiento?: string
  edad?: number
  foto_url?: string
  endereco?: string
  latitude?: number
  longitude?: number
  is_membro: boolean
  numero_membro?: number
  novo_crente: boolean
  novo_batizado: boolean
  bautizado: boolean
  data_batismo?: string
  iglesia_procedente: boolean
  iglesia_procedente_nome?: string
  data_iglesia_procedente?: string
  discipulado_inicial: EstadoFormacion
  pre_batismo: EstadoFormacion
  escuela_biblica: EstadoFormacion
  escuela_discipulado: EstadoFormacion
  treinamento: EstadoFormacion
  observaciones?: string
  activo: boolean
  created_at: string
  grupos: IntegranteGrupo[]
  ministerios: IntegranteMinisterio[]
}

export interface Grupo {
  id: number
  nombre: string
  grupo_pai_id?: number
  grupo_pai_nombre?: string
  responsable_id?: number
  responsable_nombre?: string
  ayudante_id?: number
  ayudante_nombre?: string
  supervisor_id?: number
  supervisor_nombre?: string
  dia_semana?: DiaSemana
  hora?: string
  frecuencia?: Frecuencia
  endereco?: string
  latitude?: number
  longitude?: number
  observaciones?: string
  activo: boolean
  created_at: string
  integrantes_count: number
}

export interface GrupoIntegrante {
  id: number
  nombre: string
  apellidos: string
  telefono?: string
  email?: string
  rol_en_grupo?: string
  asistencia_pct: number
  novo_crente: boolean
  bautizado: boolean
  novo_batizado: boolean
}

export interface OracaoReunion {
  id: number
  reunion_id: number
  texto: string
  respondida: boolean
  fecha_respondida?: string
  created_at: string
}

export interface Reunion {
  id: number
  grupo_id: number
  fecha: string
  hora?: string
  tipo: TipoReunion
  asistentes_count: number
  visitantes_count: number
  novos_crentes_count: number
  notas?: string
  observaciones?: string
  created_at: string
}

export interface AsistenciaItem {
  id: number
  integrante_id: number
  integrante_nombre: string
  presente: boolean
}

export interface ReunionDetalle extends Reunion {
  asistencia: AsistenciaItem[]
  oraciones: OracaoReunion[]
}

export interface Testimonio {
  id: number
  titulo: string
  contenido: string
  integrante_id?: number
  grupo_id?: number
  reunion_id?: number
  fecha: string
  destacado: boolean
  created_at: string
  integrante_nombre?: string
  grupo_nombre?: string
}

export interface MinisterioTarefaIntegrante {
  id: number
  nombre: string
  apellidos: string
}

export interface MinisterioTarefa {
  id: number
  ministerio_id: number
  nombre: string
  integrantes: MinisterioTarefaIntegrante[]
}

export interface MinisterioResponsable {
  id: number
  nombre: string
  apellidos: string
  es_responsable: boolean
}

export interface Ministerio {
  id: number
  nombre: string
  descripcion?: string
  created_at: string
  integrantes_count: number
  responsables: MinisterioResponsable[]
  tarefas: MinisterioTarefa[]
}

export interface Servicio {
  id: number
  titulo: string
  fecha: string
  descripcion?: string
  created_at: string
  integrantes: { id: number; nombre: string; apellidos: string }[]
}

export interface MapPoint {
  id: number
  nombre: string
  apellidos?: string
  latitude: number
  longitude: number
  tipo?: string
  grupo_nombre?: string
}

export interface DashboardStats {
  total_grupos: number
  total_integrantes: number
  total_membros: number
  integrantes_sin_grupo: number
  integrantes_sin_grupo_pct: number
  membros_sin_grupo: number
  membros_sin_grupo_pct: number
  total_en_ministerio: number
  supervisores_count: number
  responsables_count: number
  ayudantes_count: number
  total_visitantes: number
  avg_visitantes_por_grupo: number
  total_novos_crentes: number
  avg_novos_crentes_por_grupo: number
  total_batizados: number
  total_de_outra_igreja: number
  reuniones_periodicas: number
  reuniones_comunhao: number
  reuniones_evangelisticas: number
  reuniones_semanais: number
  reuniones_quinzenais: number
  reuniones_mensais: number
  asistencia_ultimo_mes: number
  asistencia_ultimo_ano: number
  asistencia_total: number
  discipulado_no_iniciado: number
  discipulado_cursando: number
  discipulado_terminado: number
  pre_batismo_no_iniciado: number
  pre_batismo_cursando: number
  pre_batismo_terminado: number
  escuela_biblica_no_iniciado: number
  escuela_biblica_cursando: number
  escuela_biblica_terminado: number
  escuela_discipulado_no_iniciado: number
  escuela_discipulado_cursando: number
  escuela_discipulado_terminado: number
  treinamento_no_iniciado: number
  treinamento_cursando: number
  treinamento_terminado: number
  total_oraciones: number
  oraciones_respondidas: number
  testimonios_destacados: Testimonio[]
}
