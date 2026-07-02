import type { Metadata } from 'next'
import { ClerkProvider } from '@clerk/nextjs'
import './globals.css'

export const metadata: Metadata = {
  title: 'Luxe v4.0 - AI Customer Support',
  description: 'AI-native helpdesk platform for e-commerce',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <body className="bg-white">
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
