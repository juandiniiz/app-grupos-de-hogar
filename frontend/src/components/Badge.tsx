import React from 'react'

type BadgeVariant =
  | 'responsable'
  | 'supervisor'
  | 'ayudante'
  | 'miembro'
  | 'nuevo'
  | 'sin-grupo'
  | 'grupo'
  | 'activo'
  | 'inactivo'
  | 'bautizado'
  | 'semanal'
  | 'quincenal'
  | 'mensual'

interface BadgeProps {
  variant?: BadgeVariant
  children: React.ReactNode
  className?: string
}

const variantClasses: Record<BadgeVariant, string> = {
  responsable: 'bg-[#CBCBCB] text-[#222323]',
  supervisor: 'bg-[#CBCBCB] text-[#222323]',
  ayudante: 'bg-[#CBCBCB] text-[#222323]',
  miembro: 'bg-[#F2F2F2] text-[#222323] border border-[#CBCBCB]',
  nuevo: 'bg-[#BCD11A] text-[#222323]',
  'sin-grupo': 'bg-[#F21D61] text-white',
  grupo: 'bg-[#72E6EA] text-[#222323]',
  activo: 'bg-[#66B97B] text-white',
  inactivo: 'bg-[#F21D61] text-white',
  bautizado: 'bg-[#45C1EE] text-white',
  semanal: 'bg-[#BCD11A] text-[#222323]',
  quincenal: 'bg-[#CBCBCB] text-[#222323]',
  mensual: 'bg-[#72E6EA] text-[#222323]',
}

export default function Badge({ variant = 'miembro', children, className = '' }: BadgeProps) {
  return (
    <span
      className={`rounded-[4px] px-[6px] py-[2px] font-bold text-xs inline-flex items-center gap-1 ${variantClasses[variant]} ${className}`}
    >
      {children}
    </span>
  )
}

export function RolBadge({ rol }: { rol: string }) {
  const map: Record<string, BadgeVariant> = {
    responsable: 'responsable',
    supervisor: 'supervisor',
    ayudante: 'ayudante',
    miembro: 'miembro',
  }
  const labels: Record<string, string> = {
    responsable: 'Responsable',
    supervisor: 'Supervisor',
    ayudante: 'Ayudante',
    miembro: 'Miembro',
  }
  return <Badge variant={map[rol] ?? 'miembro'}>{labels[rol] ?? rol}</Badge>
}
