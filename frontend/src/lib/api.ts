import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000/api' })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  r => r,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api

export const login = (email: string, password: string) => {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)
  return api.post('/auth/login', form)
}
export const getMe = () => api.get('/auth/me')
export const register = (data: object) => api.post('/auth/register', data)

export const getDashboardStats = () => api.get('/stats/dashboard')

export const getIntegrantes = (params?: object) => api.get('/integrantes', { params })
export const getIntegrantesMapa = () => api.get('/integrantes/mapa')
export const getIntegrante = (id: number) => api.get(`/integrantes/${id}`)
export const createIntegrante = (data: object) => api.post('/integrantes', data)
export const updateIntegrante = (id: number, data: object) => api.put(`/integrantes/${id}`, data)
export const deleteIntegrante = (id: number) => api.delete(`/integrantes/${id}`)
export const getIntegranteAsistencia = (id: number) => api.get(`/integrantes/${id}/asistencia`)

export const getGrupos = (params?: object) => api.get('/grupos', { params })
export const getGruposMapa = () => api.get('/grupos/mapa')
export const getGrupo = (id: number) => api.get(`/grupos/${id}`)
export const createGrupo = (data: object) => api.post('/grupos', data)
export const updateGrupo = (id: number, data: object) => api.put(`/grupos/${id}`, data)
export const deleteGrupo = (id: number) => api.delete(`/grupos/${id}`)
export const getGrupoIntegrantes = (id: number) => api.get(`/grupos/${id}/integrantes`)
export const addGrupoIntegrante = (id: number, data: object) => api.post(`/grupos/${id}/integrantes`, data)
export const removeGrupoIntegrante = (grupoId: number, integranteId: number) => api.delete(`/grupos/${grupoId}/integrantes/${integranteId}`)

export const getReuniones = (params?: object) => api.get('/reuniones', { params })
export const getReunion = (id: number) => api.get(`/reuniones/${id}`)
export const createReunion = (data: object) => api.post('/reuniones', data)
export const updateReunion = (id: number, data: object) => api.put(`/reuniones/${id}`, data)
export const deleteReunion = (id: number) => api.delete(`/reuniones/${id}`)
export const updateAsistencia = (id: number, data: object[]) => api.post(`/reuniones/${id}/asistencia`, data)
export const getOracionesReunion = (id: number) => api.get(`/reuniones/${id}/oraciones`)
export const addOracionReunion = (id: number, data: object) => api.post(`/reuniones/${id}/oraciones`, data)
export const updateOracionReunion = (reunionId: number, oracaoId: number, data: object) => api.put(`/reuniones/${reunionId}/oraciones/${oracaoId}`, data)
export const deleteOracionReunion = (reunionId: number, oracaoId: number) => api.delete(`/reuniones/${reunionId}/oraciones/${oracaoId}`)

export const getTestimonios = (params?: object) => api.get('/testimonios', { params })
export const getTestimonio = (id: number) => api.get(`/testimonios/${id}`)
export const createTestimonio = (data: object) => api.post('/testimonios', data)
export const updateTestimonio = (id: number, data: object) => api.put(`/testimonios/${id}`, data)
export const deleteTestimonio = (id: number) => api.delete(`/testimonios/${id}`)

export const getMinisterios = () => api.get('/ministerios')
export const getMinisterio = (id: number) => api.get(`/ministerios/${id}`)
export const createMinisterio = (data: object) => api.post('/ministerios', data)
export const updateMinisterio = (id: number, data: object) => api.put(`/ministerios/${id}`, data)
export const deleteMinisterio = (id: number) => api.delete(`/ministerios/${id}`)
export const addMinisterioIntegrante = (id: number, data: object) => api.post(`/ministerios/${id}/integrantes`, data)
export const removeMinisterioIntegrante = (ministerioId: number, integranteId: number) => api.delete(`/ministerios/${ministerioId}/integrantes/${integranteId}`)
export const addMinisterioTarefa = (id: number, data: object) => api.post(`/ministerios/${id}/tarefas`, data)
export const deleteMinisterioTarefa = (tarefaId: number) => api.delete(`/ministerios/tarefas/${tarefaId}`)
export const addTarefaIntegrante = (tarefaId: number, data: object) => api.post(`/ministerios/tarefas/${tarefaId}/integrantes`, data)
export const removeTarefaIntegrante = (tarefaId: number, integranteId: number) => api.delete(`/ministerios/tarefas/${tarefaId}/integrantes/${integranteId}`)

export const getServicios = (params?: object) => api.get('/servicios', { params })
export const getServicio = (id: number) => api.get(`/servicios/${id}`)
