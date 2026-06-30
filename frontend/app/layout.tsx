import type { Metadata } from 'next'
import { ClerkProvider } from '@clerk/nextjs'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Customer Support',
  description: 'Wilmo-like AI helpdesk for e-commerce',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="bg-white">
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
