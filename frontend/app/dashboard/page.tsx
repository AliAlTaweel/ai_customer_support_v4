'use client'

import { useEffect, useState } from 'react'
import { useTenantStore } from '@/lib/store'
import { tenantApi } from '@/lib/api'
import toast from 'react-hot-toast'

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
    const fetchMetrics = async () => {
      if (!currentTenant) {
        setLoading(false)
        return
      }

      try {
        const response = await tenantApi.getMetrics(currentTenant.id)
        setMetrics(response.data)
      } catch (error) {
        console.error('Failed to fetch metrics:', error)
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
        <div className="card p-6">
          <div className="text-sm text-gray-600 font-medium">Total Cases</div>
          <div className="text-3xl font-bold text-gray-900 mt-2">
            {metrics?.totalCases ?? 0}
          </div>
        </div>

        <div className="card p-6">
          <div className="text-sm text-gray-600 font-medium">Resolved</div>
          <div className="text-3xl font-bold text-green-600 mt-2">
            {metrics?.resolvedCases ?? 0}
          </div>
        </div>

        <div className="card p-6">
          <div className="text-sm text-gray-600 font-medium">Autopilot Rate</div>
          <div className="text-3xl font-bold text-blue-600 mt-2">
            {metrics?.autopilotRate ?? 0}%
          </div>
        </div>

        <div className="card p-6">
          <div className="text-sm text-gray-600 font-medium">Avg Response Time</div>
          <div className="text-3xl font-bold text-purple-600 mt-2">
            {metrics?.avgResponseTime ?? 0}s
          </div>
        </div>
      </div>

      {/* Getting Started */}
      <div className="card p-8 bg-gradient-to-br from-blue-50 to-indigo-50">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Getting Started</h2>
        <p className="text-gray-700 mb-6">
          Get your first AI support agent running in minutes:
        </p>
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
      </div>
    </div>
  )
}
