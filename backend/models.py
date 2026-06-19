from sqlalchemy import Column, Integer, String, Boolean, Float, Text, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    rol = Column(String, default="responsable")  # admin/supervisor/responsable/ayudante
    activo = Column(Boolean, default=True)
    integrante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    integrante = relationship("Integrante", foreign_keys=[integrante_id])


class Integrante(Base):
    __tablename__ = "integrantes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    foto_url = Column(String, nullable=True)
    endereco = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_membro = Column(Boolean, default=False)
    numero_membro = Column(Integer, nullable=True)
    novo_crente = Column(Boolean, default=False)
    novo_batizado = Column(Boolean, default=False)
    bautizado = Column(Boolean, default=False)
    data_batismo = Column(Date, nullable=True)
    iglesia_procedente = Column(Boolean, default=False)
    iglesia_procedente_nome = Column(String, nullable=True)
    data_iglesia_procedente = Column(Date, nullable=True)
    discipulado_inicial = Column(String, default="no_iniciado")
    pre_batismo = Column(String, default="no_iniciado")
    escuela_biblica = Column(String, default="no_iniciado")
    escuela_discipulado = Column(String, default="no_iniciado")
    treinamento = Column(String, default="no_iniciado")
    observaciones = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    grupo_integrantes = relationship("GrupoIntegrante", back_populates="integrante")
    ministerio_integrantes = relationship("MinisterioIntegrante", back_populates="integrante")
    reuniones_asistencia = relationship("IntegranteReunion", back_populates="integrante")


class Grupo(Base):
    __tablename__ = "grupos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    grupo_pai_id = Column(Integer, ForeignKey("grupos.id"), nullable=True)
    responsable_id = Column(Integer, ForeignKey("integrantes.id"), nullable=True)
    ayudante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=True)
    supervisor_id = Column(Integer, ForeignKey("integrantes.id"), nullable=True)
    dia_semana = Column(String, nullable=True)
    hora = Column(String, nullable=True)
    frecuencia = Column(String, nullable=True)  # semanal/quincenal/mensual
    endereco = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    observaciones = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    responsable = relationship("Integrante", foreign_keys=[responsable_id])
    ayudante = relationship("Integrante", foreign_keys=[ayudante_id])
    supervisor = relationship("Integrante", foreign_keys=[supervisor_id])
    grupo_pai = relationship("Grupo", foreign_keys=[grupo_pai_id], remote_side="Grupo.id")
    integrantes = relationship("GrupoIntegrante", back_populates="grupo")
    reuniones = relationship("Reunion", back_populates="grupo")


class GrupoIntegrante(Base):
    __tablename__ = "grupo_integrantes"
    __table_args__ = (UniqueConstraint("grupo_id", "integrante_id"),)
    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    integrante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=False)
    rol_en_grupo = Column(String, nullable=True)  # responsable/supervisor/ayudante/member

    grupo = relationship("Grupo", back_populates="integrantes")
    integrante = relationship("Integrante", back_populates="grupo_integrantes")


class Ministerio(Base):
    __tablename__ = "ministerios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    integrantes = relationship("MinisterioIntegrante", back_populates="ministerio")
    tarefas = relationship("MinisterioTarefa", back_populates="ministerio")


class MinisterioIntegrante(Base):
    __tablename__ = "ministerio_integrantes"
    __table_args__ = (UniqueConstraint("ministerio_id", "integrante_id"),)
    id = Column(Integer, primary_key=True, index=True)
    ministerio_id = Column(Integer, ForeignKey("ministerios.id"), nullable=False)
    integrante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=False)
    es_responsable = Column(Boolean, default=False)

    ministerio = relationship("Ministerio", back_populates="integrantes")
    integrante = relationship("Integrante", back_populates="ministerio_integrantes")


class MinisterioTarefa(Base):
    __tablename__ = "ministerio_tarefas"
    id = Column(Integer, primary_key=True, index=True)
    ministerio_id = Column(Integer, ForeignKey("ministerios.id"), nullable=False)
    nombre = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    ministerio = relationship("Ministerio", back_populates="tarefas")
    integrantes = relationship("MinisterioTarefaIntegrante", back_populates="tarefa")


class MinisterioTarefaIntegrante(Base):
    __tablename__ = "ministerio_tarefa_integrantes"
    id = Column(Integer, primary_key=True, index=True)
    tarefa_id = Column(Integer, ForeignKey("ministerio_tarefas.id"), nullable=False)
    integrante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=False)

    tarefa = relationship("MinisterioTarefa", back_populates="integrantes")
    integrante = relationship("Integrante")


class Reunion(Base):
    __tablename__ = "reuniones"
    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(String, nullable=True)
    tipo = Column(String, default="periodica")  # periodica/comunhao/evangelistica
    asistentes_count = Column(Integer, default=0)
    visitantes_count = Column(Integer, default=0)
    novos_crentes_count = Column(Integer, default=0)
    notas = Column(Text, nullable=True)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    grupo = relationship("Grupo", back_populates="reuniones")
    asistencia = relationship("IntegranteReunion", back_populates="reunion")
    oraciones = relationship("OracaoReunion", back_populates="reunion")
    testimonios = relationship("Testimonio", back_populates="reunion")


class IntegranteReunion(Base):
    __tablename__ = "integrante_reuniones"
    __table_args__ = (UniqueConstraint("integrante_id", "reunion_id"),)
    id = Column(Integer, primary_key=True, index=True)
    integrante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=False)
    reunion_id = Column(Integer, ForeignKey("reuniones.id"), nullable=False)
    presente = Column(Boolean, default=False)

    integrante = relationship("Integrante", back_populates="reuniones_asistencia")
    reunion = relationship("Reunion", back_populates="asistencia")


class OracaoReunion(Base):
    __tablename__ = "oracao_reuniones"
    id = Column(Integer, primary_key=True, index=True)
    reunion_id = Column(Integer, ForeignKey("reuniones.id"), nullable=False)
    texto = Column(Text, nullable=False)
    respondida = Column(Boolean, default=False)
    fecha_respondida = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    reunion = relationship("Reunion", back_populates="oraciones")


class Testimonio(Base):
    __tablename__ = "testimonios"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    contenido = Column(Text, nullable=False)
    integrante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=True)
    reunion_id = Column(Integer, ForeignKey("reuniones.id"), nullable=True)
    fecha = Column(Date, nullable=False)
    destacado = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    integrante = relationship("Integrante")
    grupo = relationship("Grupo")
    reunion = relationship("Reunion", back_populates="testimonios")


class Servicio(Base):
    __tablename__ = "servicios"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)
    descripcion = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    integrantes = relationship("ServicioIntegrante", back_populates="servicio")


class ServicioIntegrante(Base):
    __tablename__ = "servicio_integrantes"
    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    integrante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=False)

    servicio = relationship("Servicio", back_populates="integrantes")
    integrante = relationship("Integrante")


class Oracion(Base):
    __tablename__ = "oraciones"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    integrante_id = Column(Integer, ForeignKey("integrantes.id"), nullable=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=True)
    fecha = Column(Date, nullable=False)
    respondida = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
