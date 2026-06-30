'use client'

import { useEffect, useState } from 'react'
import { useTenantStore } from '@/lib/store'
import { integrationApi } from '@/lib/api'
import toast from 'react-hot-toast'

interface Integration {
  id: string
  tenantId: string
  type: string
  status: string
  createdAt: string
}

export default function IntegrationsPage() {
  const { currentTenant } = useTenantStore()
  const [integrations, setIntegrations] = useState<Integration[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    type: 'shopify',
    shopifyStoreName: '',
    shopifyAccessToken: '',
  })

  useEffect(() => {
    if (currentTenant) {
      fetchIntegrations()
    }
  }, [currentTenant])

  const fetchIntegrations = async () => {
    if (!currentTenant) return

    try {
      const response = await integrationApi.list(currentTenant.id)
      setIntegrations(response.data)
    } catch (error) {
      console.error('Failed to fetch integrations:', error)
      toast.error('Failed to load integrations')
    } finally {
      setLoading(false)
    }
  }

  const handleConnect = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!currentTenant) {
      toast.error('No tenant selected')
      return
    }

    try {
      await integrationApi.create(currentTenant.id, formData)
      toast.success('Integration connected')
      setShowForm(false)
      setFormData({
        type: 'shopify',
        shopifyStoreName: '',
        shopifyAccessToken: '',
      })
      await fetchIntegrations()
    } catch (error) {
      console.error('Failed to connect integration:', error)
      toast.error('Failed to connect integration')
    }
  }

  const handleDisconnect = async (integrationId: string) => {
    if (!currentTenant) return

    if (!confirm('Are you sure you want to disconnect this integration?')) return

    try {
      await integrationApi.delete(currentTenant.id, integrationId)
      toast.success('Integration disconnected')
      await fetchIntegrations()
    } catch (error) {
      console.error('Failed to disconnect integration:', error)
      toast.error('Failed to disconnect integration')
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Integrations</h1>
          <p className="text-gray-600 mt-2">Connect to your e-commerce platform</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary"
        >
          {showForm ? 'Cancel' : '+ Connect'}
        </button>
      </div>

      {showForm ? (
        <div className="card p-8">
          <h2 className="text-2xl font-bold mb-6">Connect Integration</h2>
          <form onSubmit={handleConnect} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Platform
              </label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="input-field"
              >
                <option value="shopify">Shopify</option>
                <option value="woocommerce">WooCommerce</option>
                <option value="stripe">Stripe</option>
              </select>
            </div>

            {formData.type === 'shopify' && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Store Name (e.g., mystore.myshopify.com)
                  </label>
                  <input
                    type="text"
                    value={formData.shopifyStoreName}
                    onChange={(e) => setFormData({ ...formData, shopifyStoreName: e.target.value })}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Access Token
                  </label>
                  <input
                    type="password"
                    value={formData.shopifyAccessToken}
                    onChange={(e) => setFormData({ ...formData, shopifyAccessToken: e.target.value })}
                    className="input-field"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    Get this from your Shopify admin dashboard
                  </p>
                </div>
              </>
            )}

            <button type="submit" className="btn-primary">
              Connect {formData.type}
            </button>
          </form>
        </div>
      ) : (
        <div className="grid gap-6">
          {integrations.length > 0 ? (
            integrations.map((integration) => (
              <div key={integration.id} className="card p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold text-lg capitalize">{integration.type}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      Status: <span className="font-medium capitalize">{integration.status}</span>
                    </p>
                  </div>
                  <button
                    onClick={() => handleDisconnect(integration.id)}
                    className="btn-secondary text-sm"
                  >
                    Disconnect
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="card p-8 text-center">
              <p className="text-gray-600">No integrations connected yet</p>
              <p className="text-sm text-gray-500 mt-2">
                Connect your e-commerce platform to get started
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
