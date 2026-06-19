import React, { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Header from './Header'
import SideMenu from './SideMenu'

export default function Layout() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header onMenuOpen={() => setMenuOpen(true)} />
      <SideMenu open={menuOpen} onClose={() => setMenuOpen(false)} />
      <main className="flex-1 px-4 py-5 max-w-2xl mx-auto w-full">
        <Outlet />
      </main>
    </div>
  )
}
