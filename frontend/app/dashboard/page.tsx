'use client'

import { useEffect, useState } from 'react'
import { useTenantStore } from '@/lib/store'
import { tenantApi } from '@/lib/api'
import { logger } from '@/lib/logger'
import toast from 'react-hot-toast'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface Metrics {
  totalCases: number
  resolvedCases: number
  autopilotRate: number
  avgResponseTime: number
}

export default function DashboardPage() {
  const { currentTenant } = useTenantStore()
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    logger.navigation('Dashboard')
    logger.info('📊 Loading tenant metrics')

    const fetchMetrics = async () => {
      if (!currentTenant) {
        logger.warn('⚠️ No tenant selected')
        setLoading(false)
        return
      }

      try {
        logger.debug(`Fetching metrics for tenant: ${currentTenant.id}`)
        const response = await tenantApi.getMetrics(currentTenant.id)
        setMetrics(response.data)
        logger.success('✓ Metrics loaded')
      } catch (error) {
        logger.error('Failed to fetch metrics', error)
        toast.error('Failed to load metrics')
      } finally {
        setLoading(false)
      }
    }

    fetchMetrics()
  }, [currentTenant])

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  if (!currentTenant) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No tenant selected. Please select a tenant from settings.</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">{currentTenant.name}</h1>
        <p className="text-gray-600 mt-2">Welcome to your AI support dashboard</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total Cases</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-gray-900">
              {metrics?.totalCases ?? 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Resolved</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600">
              {metrics?.resolvedCases ?? 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Autopilot Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600">
              {metrics?.autopilotRate ?? 0}%
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Avg Response Time</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-purple-600">
              {metrics?.avgResponseTime ?? 0}s
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Getting Started */}
      <Card className="bg-gradient-to-br from-blue-50 to-indigo-50">
        <CardHeader>
          <CardTitle>Getting Started</CardTitle>
          <CardDescription>Get your first AI support agent running in minutes</CardDescription>
        </CardHeader>
        <CardContent>
          <ol className="space-y-3 text-gray-700">
            <li className="flex">
              <span className="font-bold text-blue-600 mr-4">1.</span>
              <span>Connect your e-commerce store (Shopify or WooCommerce)</span>
            </li>
            <li className="flex">
              <span className="font-bold text-blue-600 mr-4">2.</span>
              <span>Upload your FAQ and knowledge base</span>
            </li>
            <li className="flex">
              <span className="font-bold text-blue-600 mr-4">3.</span>
              <span>Set your brand tone and custom instructions</span>
            </li>
            <li className="flex">
              <span className="font-bold text-blue-600 mr-4">4.</span>
              <span>Review AI responses before they go live (Copilot mode)</span>
            </li>
          </ol>
        </CardContent>
      </Card>
    </div>
  )
}
