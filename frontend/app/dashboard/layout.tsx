'use client'

import { SignedIn, SignedOut, RedirectToSignIn, UserButton } from '@clerk/nextjs'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import React from 'react'

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
    <>
      <SignedIn>
        <div className="flex h-screen bg-gray-100">
          {/* Sidebar */}
          <div className="w-64 bg-white shadow-lg">
            <div className="p-6 border-b">
              <h1 className="text-2xl font-bold text-blue-600">Wilmo</h1>
              <p className="text-sm text-gray-500">AI Customer Support</p>
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
              <UserButton afterSignOutUrl="/" />
            </div>

            {/* Content */}
            <div className="flex-1 overflow-auto p-8">
              {children}
            </div>
          </div>
        </div>
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  )
}
