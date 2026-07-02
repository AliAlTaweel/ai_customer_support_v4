'use client'

import { useEffect } from 'react'
import { SignedIn, SignedOut, SignInButton, SignUpButton } from '@clerk/nextjs'
import { logger } from '@/lib/logger'
import { Button } from '@/components/ui/button'

export default function Home() {
  useEffect(() => {
    logger.info('🏠 Home page loaded')
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-900 flex items-center justify-center px-4">
      <div className="max-w-lg w-full text-center text-white">
        <h1 className="text-5xl font-bold mb-2">Luxe v4.0</h1>
        <p className="text-2xl mb-8 opacity-90">AI-Native Helpdesk</p>
        <p className="text-lg mb-8 opacity-80">
          Let AI handle 80%+ of support tickets automatically.
        </p>
        <div className="space-y-4">
          <SignedIn>
            <a
              href="/dashboard"
              className="inline-block px-8 py-3 bg-white text-blue-600 font-bold rounded-lg hover:bg-gray-100 transition-colors"
            >
              Launch Dashboard
            </a>
          </SignedIn>

          <SignedOut>
            <div className="flex gap-3 justify-center">
              <SignInButton mode="modal">
                <Button className="bg-white text-blue-600 hover:bg-gray-100">
                  Sign In
                </Button>
              </SignInButton>
              <SignUpButton mode="modal">
                <Button className="bg-blue-500 hover:bg-blue-400 text-white">
                  Sign Up
                </Button>
              </SignUpButton>
            </div>
          </SignedOut>

          <p className="text-sm opacity-75">
            Phase 1: Multi-Tenant Foundation ✓
          </p>
        </div>
      </div>
    </div>
  )
}
