'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import React from 'react'
import { UserButton } from '@clerk/nextjs'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  const navItems = [
    { href: '/dashboard', label: 'Overview', icon: '📊' },
    { href: '/dashboard/cases', label: 'Cases', icon: '📋' },
    { href: '/dashboard/integrations', label: 'Integrations', icon: '🔗' },
    { href: '/dashboard/settings', label: 'Settings', icon: '⚙️' },
  ]

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-blue-600">Luxe v4.0</h1>
          <p className="text-sm text-gray-500">AI Helpdesk</p>
        </div>

        <nav className="mt-8">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-3 px-6 py-3 border-l-4 transition-colors ${
                pathname === item.href
                  ? 'border-blue-600 bg-blue-50 text-blue-600'
                  : 'border-transparent text-gray-600 hover:bg-gray-50'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </Link>
          ))}
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b px-8 py-4 flex justify-between items-center">
          <h2 className="text-lg font-semibold text-gray-900">Dashboard</h2>
          <UserButton />
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-8">
          {children}
        </div>
      </div>
    </div>
  )
}
