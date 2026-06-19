import React from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

interface SideMenuProps {
  open: boolean
  onClose: () => void
}

const menuItems = [
  { label: 'Inicio', path: '/', icon: HomeIcon },
  { label: 'Grupos de Hogar', path: '/grupos', icon: GroupIcon },
  { label: 'Integrantes', path: '/integrantes', icon: PeopleIcon },
  { label: 'Ministerios', path: '/ministerios', icon: ChurchIcon },
  { label: 'Testimonios', path: '/testimonios', icon: HeartIcon },
]

function HomeIcon() {
  return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" /></svg>
}
function GroupIcon() {
  return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" /></svg>
}
function PeopleIcon() {
  return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" /></svg>
}
function ChurchIcon() {
  return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M11 2v3H9v2h2v2.07C7.06 9.56 4 12.92 4 17h16c0-4.08-3.06-7.44-7-7.93V7h2V5h-2V2h-2z" /></svg>
}
function HeartIcon() {
  return <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" /></svg>
}
function PowerIcon() {
  return <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M13 3h-2v10h2V3zm4.83 2.17l-1.42 1.42C17.99 7.86 19 9.81 19 12c0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.19 1.01-4.14 2.58-5.42L6.17 5.17C4.23 6.82 3 9.26 3 12c0 4.97 4.03 9 9 9s9-4.03 9-9c0-2.74-1.23-5.18-3.17-6.83z" /></svg>
}

export default function SideMenu({ open, onClose }: SideMenuProps) {
  const location = useLocation()
  const navigate = useNavigate()

  const user = (() => {
    try { return JSON.parse(localStorage.getItem('user') ?? '{}') } catch { return {} }
  })()

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate('/login')
    onClose()
  }

  return (
    <>
      <div
        className={`fixed inset-0 z-40 bg-black/40 transition-opacity duration-300 ${open ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}
        onClick={onClose}
      />
      <aside className={`fixed top-0 right-0 h-full w-[260px] bg-[#222323] z-50 flex flex-col shadow-card transition-transform duration-300 ${open ? 'translate-x-0' : 'translate-x-full'}`}>
        <div className="flex items-center justify-between px-5 py-4 border-b border-[#444]">
          <div className="flex flex-col leading-none">
            <span className="font-marker text-primary text-lg">GRUPOS DE HOGAR</span>
            <span className="text-[9px] text-grey tracking-widest uppercase">Seguimiento</span>
          </div>
          <button onClick={onClose} className="p-1 text-grey hover:text-white transition-colors">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" /></svg>
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto py-4">
          {menuItems.map(({ label, path, icon: Icon }) => {
            const active = location.pathname === path || (path !== '/' && location.pathname.startsWith(path))
            return (
              <React.Fragment key={path}>
                <Link
                  to={path}
                  onClick={onClose}
                  className={`flex items-center gap-3 px-5 py-3 transition-colors text-[18px] ${active ? 'text-primary font-bold' : 'text-white font-light hover:text-primary'}`}
                >
                  <span className={active ? 'text-primary' : 'text-grey'}><Icon /></span>
                  {label}
                </Link>
                <div className="border-b border-[#444] mx-5" />
              </React.Fragment>
            )
          })}
        </nav>

        <div className="border-t border-[#444] px-5 py-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
            {user?.nombre?.charAt(0)?.toUpperCase() ?? 'U'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-white truncate">{user?.nombre ?? 'Usuario'}</p>
            <p className="text-xs text-grey capitalize">{user?.email ?? ''}</p>
          </div>
        </div>

        <div className="border-t border-[#444] px-5 py-3">
          <button onClick={handleLogout} className="flex items-center gap-2 font-light text-[18px] hover:opacity-80 transition-opacity w-full py-2" style={{ color: '#F21D61' }}>
            <PowerIcon />
            Cerrar Sesión
          </button>
        </div>
      </aside>
    </>
  )
}
