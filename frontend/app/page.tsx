'use client'

import { SignedIn, SignedOut, RedirectToSignIn } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Redirect signed-in users to dashboard
    const checkAuth = async () => {
      try {
        const response = await fetch('/api/check-auth')
        if (response.ok) {
          router.push('/dashboard')
        }
      } catch (error) {
        console.error('Auth check failed:', error)
      }
    }

    checkAuth()
  }, [router])

  return (
    <>
      <SignedIn>
        <div>Loading...</div>
      </SignedIn>
      <SignedOut>
        <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-900 flex items-center justify-center px-4">
          <div className="max-w-lg w-full text-center text-white">
            <h1 className="text-5xl font-bold mb-4">AI Customer Support</h1>
            <p className="text-xl mb-8 opacity-90">
              Zendesk without the support team. Let AI handle 80%+ of tickets.
            </p>
            <div className="space-y-4">
              <a
                href="/sign-up"
                className="inline-block px-8 py-3 bg-white text-blue-600 font-bold rounded-lg hover:bg-gray-100 transition-colors"
              >
                Start Free Trial
              </a>
              <p className="text-sm opacity-75">
                No credit card required • 14-day trial
              </p>
            </div>
          </div>
        </div>
      </SignedOut>
    </>
  )
}
