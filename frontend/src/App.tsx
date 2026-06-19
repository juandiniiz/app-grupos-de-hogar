import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Integrantes from './pages/Integrantes'
import IntegranteDetalle from './pages/IntegranteDetalle'
import IntegranteForm from './pages/IntegranteForm'
import Grupos from './pages/Grupos'
import GrupoDetalle from './pages/GrupoDetalle'
import GrupoForm from './pages/GrupoForm'
import ReunionDetalle from './pages/ReunionDetalle'
import Ministerios from './pages/Ministerios'
import MinisterioDetalle from './pages/MinisterioDetalle'
import Testimonios from './pages/Testimonios'
import TestimonioDetalle from './pages/TestimonioDetalle'
import NotFound from './pages/NotFound'

function RequireAuth({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token')
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<RequireAuth><Layout /></RequireAuth>}>
          <Route index element={<Dashboard />} />
          <Route path="integrantes" element={<Integrantes />} />
          <Route path="integrantes/nuevo" element={<IntegranteForm />} />
          <Route path="integrantes/:id" element={<IntegranteDetalle />} />
          <Route path="integrantes/:id/editar" element={<IntegranteForm />} />
          <Route path="grupos" element={<Grupos />} />
          <Route path="grupos/nuevo" element={<GrupoForm />} />
          <Route path="grupos/:id" element={<GrupoDetalle />} />
          <Route path="grupos/:id/editar" element={<GrupoForm />} />
          <Route path="grupos/:id/reuniones/:reunionId" element={<ReunionDetalle />} />
          <Route path="ministerios" element={<Ministerios />} />
          <Route path="ministerios/:id" element={<MinisterioDetalle />} />
          <Route path="testimonios" element={<Testimonios />} />
          <Route path="testimonios/:id" element={<TestimonioDetalle />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
