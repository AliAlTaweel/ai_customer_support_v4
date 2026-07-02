'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { caseApi } from '@/lib/api'
import { useTenantStore } from '@/lib/store'
import { logger } from '@/lib/logger'
import toast from 'react-hot-toast'

interface Case {
  id: string
  tenantId: string
  integrationId: string
  customerEmail: string
  customerName?: string
  subject: string
  description: string
  status: string
  priority: string
  assignedTo?: string
  aiResponse?: string
  humanResponse?: string
  aiConfidence: string
  createdAt: string
  updatedAt: string
}

const statusColors: Record<string, string> = {
  open: 'bg-blue-100 text-blue-800',
  pending_review: 'bg-yellow-100 text-yellow-800',
  resolved: 'bg-green-100 text-green-800',
  closed: 'bg-gray-100 text-gray-800',
}

const priorityColors: Record<string, string> = {
  low: 'bg-green-50 border-green-200',
  medium: 'bg-yellow-50 border-yellow-200',
  high: 'bg-orange-50 border-orange-200',
  urgent: 'bg-red-50 border-red-200',
}

export default function CasesPage() {
  const currentTenant = useTenantStore((state) => state.currentTenant)
  const [cases, setCases] = useState<Case[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState<string>('')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    if (!currentTenant?.id) return
    loadCases()
  }, [currentTenant?.id, statusFilter])

  const loadCases = async () => {
    try {
      setLoading(true)
      const response = await caseApi.list(currentTenant!.id, statusFilter)
      setCases(response.data)
      logger.success(`Loaded ${response.data.length} cases`)
    } catch (error) {
      logger.error('Failed to load cases', error)
      toast.error('Failed to load cases')
    } finally {
      setLoading(false)
    }
  }

  const filteredCases = cases.filter((c) =>
    c.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.customerEmail.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const stats = {
    total: cases.length,
    open: cases.filter((c) => c.status === 'open').length,
    pending: cases.filter((c) => c.status === 'pending_review').length,
    resolved: cases.filter((c) => c.status === 'resolved').length,
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Support Cases</h1>
          <p className="text-gray-500">Phase 2: Case management and AI responses</p>
        </div>
        <Button onClick={() => toast.success('Create case form - coming soon!')}>+ New Case</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Cases</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-blue-600">Open</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.open}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-yellow-600">Pending Review</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pending}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-green-600">Resolved</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.resolved}</div>
          </CardContent>
        </Card>
      </div>

      <div className="flex gap-4">
        <Input
          placeholder="Search by subject or customer email..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md"
        >
          <option value="">All Statuses</option>
          <option value="open">Open</option>
          <option value="pending_review">Pending Review</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </select>
      </div>

      {loading ? (
        <div className="text-center py-8 text-gray-500">Loading cases...</div>
      ) : filteredCases.length === 0 ? (
        <Card>
          <CardContent className="py-8 text-center text-gray-500">
            {cases.length === 0 ? 'No cases yet. Create your first case to get started.' : 'No cases match your search.'}
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {filteredCases.map((c) => (
            <Card
              key={c.id}
              className={`cursor-pointer border-2 transition-all ${priorityColors[c.priority] || priorityColors.medium}`}
            >
              <CardContent className="p-4">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold">{c.subject}</h3>
                      <span className={`px-2 py-1 text-xs rounded-full font-medium ${statusColors[c.status]}`}>
                        {c.status.replace('_', ' ').toUpperCase()}
                      </span>
                      <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full font-medium">
                        {c.priority.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">From: {c.customerEmail}</p>
                    <p className="text-sm text-gray-600 mt-1">{c.description.substring(0, 100)}...</p>
                    {c.aiResponse && (
                      <div className="mt-2 p-2 bg-blue-50 rounded">
                        <p className="text-xs font-semibold text-blue-900">AI Response:</p>
                        <p className="text-sm text-blue-800">{c.aiResponse.substring(0, 80)}...</p>
                      </div>
                    )}
                  </div>
                  <div className="text-right text-sm text-gray-500">
                    <p>{new Date(c.createdAt).toLocaleDateString()}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Card className="bg-blue-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-blue-900">Phase 2 Features Coming Soon</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-blue-800 space-y-2">
          <p>✓ Case creation from customer messages</p>
          <p>✓ AI-powered response generation</p>
          <p>✓ Human review and approval workflow</p>
          <p>✓ Message threading and history</p>
          <p>✓ Agent assignment and routing</p>
          <p>✓ Analytics and metrics dashboard</p>
        </CardContent>
      </Card>
    </div>
  )
}
