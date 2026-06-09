import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Document Intelligence',
  description: 'Intelligent Q&A system for document analysis using AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        {children}
      </body>
    </html>
  )
}
