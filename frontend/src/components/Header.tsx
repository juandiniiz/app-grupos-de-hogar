import React from 'react'

interface HeaderProps {
  onMenuOpen: () => void
}

export default function Header({ onMenuOpen }: HeaderProps) {
  return (
    <header className="bg-white shadow-card sticky top-0 z-30 h-16 flex items-center justify-between px-4">
      {/* Logo */}
      <div className="flex flex-col leading-none">
        <span className="text-[10px] font-roboto tracking-[0.2em] uppercase text-dark font-light">
          seguimiento
        </span>
        <span className="font-marker text-[#66B97B] text-xl leading-tight">GRUPOS DE HOGAR</span>
        <span className="text-[9px] text-grey-dark tracking-widest uppercase font-light">
          Punto de Encuentro
        </span>
      </div>

      {/* Hamburger */}
      <button
        onClick={onMenuOpen}
        className="p-2 rounded-md hover:bg-background transition-colors"
        aria-label="Abrir menú"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="3" y="6" width="18" height="2" rx="1" fill="#222323" />
          <rect x="3" y="11" width="18" height="2" rx="1" fill="#222323" />
          <rect x="3" y="16" width="18" height="2" rx="1" fill="#222323" />
        </svg>
      </button>
    </header>
  )
}
