import React from 'react'
import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-4 text-center">
      <div className="w-20 h-20 rounded-full bg-grey flex items-center justify-center text-4xl font-bold text-grey-dark">
        404
      </div>
      <h2 className="text-[24px] font-bold text-dark">Página no encontrada</h2>
      <p className="text-sm text-grey-dark">La página que buscas no existe o fue movida.</p>
      <Link to="/">
        <button className="btn-primary">Volver al inicio</button>
      </Link>
    </div>
  )
}
