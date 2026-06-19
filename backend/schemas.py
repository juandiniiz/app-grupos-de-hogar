from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime


# ---- Integrante ----
class IntegranteBase(BaseModel):
    nombre: str
    apellidos: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    foto_url: Optional[str] = None
    endereco: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_membro: bool = False
    numero_membro: Optional[int] = None
    novo_crente: bool = False
    novo_batizado: bool = False
    bautizado: bool = False
    data_batismo: Optional[date] = None
    iglesia_procedente: bool = False
    iglesia_procedente_nome: Optional[str] = None
    data_iglesia_procedente: Optional[date] = None
    discipulado_inicial: str = "no_iniciado"
    pre_batismo: str = "no_iniciado"
    escuela_biblica: str = "no_iniciado"
    escuela_discipulado: str = "no_iniciado"
    treinamento: str = "no_iniciado"
    observaciones: Optional[str] = None


class IntegranteCreate(IntegranteBase):
    grupos: Optional[List[dict]] = []  # [{grupo_id, rol_en_grupo}]
    ministerios: Optional[List[dict]] = []  # [{ministerio_id, es_responsable}]


class IntegranteUpdate(IntegranteBase):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    activo: Optional[bool] = None
    grupos: Optional[List[dict]] = None
    ministerios: Optional[List[dict]] = None


class IntegranteGrupoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    grupo_id: int
    grupo_nombre: str
    rol_en_grupo: Optional[str] = None


class IntegranteMinisterioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    es_responsable: bool = False


class IntegranteOut(IntegranteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    activo: bool
    created_at: datetime
    edad: Optional[int] = None
    grupos: List[IntegranteGrupoOut] = []
    ministerios: List[IntegranteMinisterioOut] = []


class IntegranteMapaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    apellidos: str
    latitude: Optional[float]
    longitude: Optional[float]
    grupo_nombre: Optional[str] = None


# ---- Grupo ----
class GrupoBase(BaseModel):
    nombre: str
    grupo_pai_id: Optional[int] = None
    responsable_id: Optional[int] = None
    ayudante_id: Optional[int] = None
    supervisor_id: Optional[int] = None
    dia_semana: Optional[str] = None
    hora: Optional[str] = None
    frecuencia: Optional[str] = None
    endereco: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    observaciones: Optional[str] = None


class GrupoCreate(GrupoBase):
    integrantes: Optional[List[dict]] = []  # [{integrante_id, rol_en_grupo}]


class GrupoUpdate(GrupoBase):
    nombre: Optional[str] = None
    activo: Optional[bool] = None
    integrantes: Optional[List[dict]] = None


class GrupoOut(GrupoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    activo: bool
    created_at: datetime
    responsable_nombre: Optional[str] = None
    ayudante_nombre: Optional[str] = None
    supervisor_nombre: Optional[str] = None
    grupo_pai_nombre: Optional[str] = None
    integrantes_count: int = 0


class GrupoMapaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    latitude: Optional[float]
    longitude: Optional[float]


# ---- Reunion ----
class ReunionBase(BaseModel):
    grupo_id: int
    fecha: date
    hora: Optional[str] = None
    tipo: str = "periodica"
    asistentes_count: int = 0
    visitantes_count: int = 0
    novos_crentes_count: int = 0
    notas: Optional[str] = None
    observaciones: Optional[str] = None


class ReunionCreate(ReunionBase):
    pass


class ReunionUpdate(BaseModel):
    fecha: Optional[date] = None
    hora: Optional[str] = None
    tipo: Optional[str] = None
    asistentes_count: Optional[int] = None
    visitantes_count: Optional[int] = None
    novos_crentes_count: Optional[int] = None
    notas: Optional[str] = None
    observaciones: Optional[str] = None


class IntegranteReunionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    integrante_id: int
    integrante_nombre: str
    presente: bool


class OracaoReunionBase(BaseModel):
    texto: str
    respondida: bool = False
    fecha_respondida: Optional[date] = None


class OracaoReunionCreate(OracaoReunionBase):
    pass


class OracaoReunionUpdate(OracaoReunionBase):
    texto: Optional[str] = None


class OracaoReunionOut(OracaoReunionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    reunion_id: int
    created_at: datetime


class ReunionOut(ReunionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class ReunionDetalleOut(ReunionOut):
    asistencia: List[IntegranteReunionOut] = []
    oraciones: List[OracaoReunionOut] = []


# ---- Testimonio ----
class TestimonioBase(BaseModel):
    titulo: str
    contenido: str
    integrante_id: Optional[int] = None
    grupo_id: Optional[int] = None
    reunion_id: Optional[int] = None
    fecha: date
    destacado: bool = False


class TestimonioCreate(TestimonioBase):
    pass


class TestimonioUpdate(TestimonioBase):
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    fecha: Optional[date] = None


class TestimonioOut(TestimonioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    integrante_nombre: Optional[str] = None
    grupo_nombre: Optional[str] = None


# ---- Ministerio ----
class MinisterioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class MinisterioCreate(MinisterioBase):
    pass


class MinisterioUpdate(MinisterioBase):
    nombre: Optional[str] = None


class TarefaIntegranteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    apellidos: str


class TarefaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    ministerio_id: int
    integrantes: List[TarefaIntegranteOut] = []


class MinisterioResponsableOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    apellidos: str
    es_responsable: bool = True


class MinisterioOut(MinisterioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    integrantes_count: int = 0
    responsables: List[MinisterioResponsableOut] = []
    tarefas: List[TarefaOut] = []


# ---- Servicio ----
class ServicioBase(BaseModel):
    titulo: str
    fecha: datetime
    descripcion: Optional[str] = None


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(ServicioBase):
    titulo: Optional[str] = None
    fecha: Optional[datetime] = None


class ServicioIntegranteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    apellidos: str


class ServicioOut(ServicioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    integrantes: List[ServicioIntegranteOut] = []


# ---- Oracion ----
class OracionBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    integrante_id: Optional[int] = None
    grupo_id: Optional[int] = None
    fecha: date
    respondida: bool = False


class OracionCreate(OracionBase):
    pass


class OracionUpdate(OracionBase):
    titulo: Optional[str] = None
    fecha: Optional[date] = None


class OracionOut(OracionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ---- Auth ----
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: str
    password: str
    nombre: str
    rol: str = "responsable"
    integrante_id: Optional[int] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    nombre: str
    rol: str
    activo: bool
    integrante_id: Optional[int]


# ---- Dashboard ----
class DashboardStats(BaseModel):
    total_grupos: int = 0
    total_integrantes: int = 0
    total_membros: int = 0
    integrantes_sin_grupo: int = 0
    integrantes_sin_grupo_pct: float = 0.0
    membros_sin_grupo: int = 0
    membros_sin_grupo_pct: float = 0.0
    total_en_ministerio: int = 0
    supervisores_count: int = 0
    responsables_count: int = 0
    ayudantes_count: int = 0
    total_visitantes: int = 0
    avg_visitantes_por_grupo: float = 0.0
    total_novos_crentes: int = 0
    avg_novos_crentes_por_grupo: float = 0.0
    total_batizados: int = 0
    total_de_outra_igreja: int = 0
    reuniones_periodicas: int = 0
    reuniones_comunhao: int = 0
    reuniones_evangelisticas: int = 0
    reuniones_semanais: int = 0
    reuniones_quinzenais: int = 0
    reuniones_mensais: int = 0
    asistencia_ultimo_mes: float = 0.0
    asistencia_ultimo_ano: float = 0.0
    asistencia_total: float = 0.0
    discipulado_no_iniciado: int = 0
    discipulado_cursando: int = 0
    discipulado_terminado: int = 0
    pre_batismo_no_iniciado: int = 0
    pre_batismo_cursando: int = 0
    pre_batismo_terminado: int = 0
    escuela_biblica_no_iniciado: int = 0
    escuela_biblica_cursando: int = 0
    escuela_biblica_terminado: int = 0
    escuela_discipulado_no_iniciado: int = 0
    escuela_discipulado_cursando: int = 0
    escuela_discipulado_terminado: int = 0
    treinamento_no_iniciado: int = 0
    treinamento_cursando: int = 0
    treinamento_terminado: int = 0
    total_oraciones: int = 0
    oraciones_respondidas: int = 0
    testimonios_destacados: List[TestimonioOut] = []
