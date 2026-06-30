'use client'

import { useEffect, useState } from 'react'
import { tenantApi, apiKeyApi } from '@/lib/api'
import toast from 'react-hot-toast'

interface Tenant {
  id: string
  name: string
  supportEmail: string
  tone: string
  systemPrompt: string
  apiKey: string
}

export default function SettingsPage() {
  const [tenants, setTenants] = useState<Tenant[]>([])
  const [selectedTenant, setSelectedTenant] = useState<Tenant | null>(null)
  const [showNewTenantForm, setShowNewTenantForm] = useState(false)
  const [loading, setLoading] = useState(true)
  const [apiKeyMasked, setApiKeyMasked] = useState('')

  const [formData, setFormData] = useState({
    name: '',
    supportEmail: '',
    tone: 'professional',
    systemPrompt: '',
  })

  useEffect(() => {
    fetchTenants()
  }, [])

  const fetchTenants = async () => {
    try {
      const response = await tenantApi.list()
      setTenants(response.data)
      if (response.data.length > 0) {
        selectTenant(response.data[0])
      }
    } catch (error) {
      console.error('Failed to fetch tenants:', error)
      toast.error('Failed to load tenants')
    } finally {
      setLoading(false)
    }
  }

  const selectTenant = async (tenant: Tenant) => {
    setSelectedTenant(tenant)
    setFormData({
      name: tenant.name,
      supportEmail: tenant.supportEmail,
      tone: tenant.tone,
      systemPrompt: tenant.systemPrompt,
    })

    // Fetch API key
    try {
      const response = await apiKeyApi.get(tenant.id)
      setApiKeyMasked(response.data.key)
    } catch (error) {
      console.error('Failed to fetch API key:', error)
    }
  }

  const handleCreateTenant = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!formData.name || !formData.supportEmail) {
      toast.error('Please fill in all required fields')
      return
    }

    try {
      const response = await tenantApi.create(formData)
      toast.success('Tenant created successfully')
      setShowNewTenantForm(false)
      setFormData({
        name: '',
        supportEmail: '',
        tone: 'professional',
        systemPrompt: '',
      })
      await fetchTenants()
    } catch (error) {
      console.error('Failed to create tenant:', error)
      toast.error('Failed to create tenant')
    }
  }

  const handleUpdateTenant = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!selectedTenant) return

    try {
      await tenantApi.update(selectedTenant.id, formData)
      toast.success('Tenant updated successfully')
      await fetchTenants()
    } catch (error) {
      console.error('Failed to update tenant:', error)
      toast.error('Failed to update tenant')
    }
  }

  const generateNewApiKey = async () => {
    if (!selectedTenant) return

    try {
      const response = await apiKeyApi.generate(selectedTenant.id)
      setApiKeyMasked(response.data.key)
      toast.success('New API key generated')
    } catch (error) {
      console.error('Failed to generate API key:', error)
      toast.error('Failed to generate API key')
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-2">Manage your tenant configuration and API keys</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Tenant List */}
        <div className="lg:col-span-1">
          <div className="card p-4">
            <h2 className="text-lg font-semibold mb-4">Tenants</h2>
            <div className="space-y-2 mb-4">
              {tenants.map((tenant) => (
                <button
                  key={tenant.id}
                  onClick={() => selectTenant(tenant)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    selectedTenant?.id === tenant.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  <div className="font-medium">{tenant.name}</div>
                  <div className="text-xs opacity-75">{tenant.supportEmail}</div>
                </button>
              ))}
            </div>
            <button
              onClick={() => setShowNewTenantForm(!showNewTenantForm)}
              className="w-full btn-primary text-sm"
            >
              {showNewTenantForm ? 'Cancel' : '+ New Tenant'}
            </button>
          </div>
        </div>

        {/* Settings Form */}
        <div className="lg:col-span-3">
          {showNewTenantForm ? (
            <div className="card p-8">
              <h2 className="text-2xl font-bold mb-6">Create New Tenant</h2>
              <form onSubmit={handleCreateTenant} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Organization Name *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Support Email *
                  </label>
                  <input
                    type="email"
                    value={formData.supportEmail}
                    onChange={(e) => setFormData({ ...formData, supportEmail: e.target.value })}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Brand Tone
                  </label>
                  <select
                    value={formData.tone}
                    onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                    className="input-field"
                  >
                    <option value="professional">Professional</option>
                    <option value="friendly">Friendly</option>
                    <option value="casual">Casual</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    System Prompt
                  </label>
                  <textarea
                    value={formData.systemPrompt}
                    onChange={(e) => setFormData({ ...formData, systemPrompt: e.target.value })}
                    className="input-field h-32 resize-none"
                    placeholder="Custom instructions for the AI agent..."
                  />
                </div>

                <button type="submit" className="btn-primary">
                  Create Tenant
                </button>
              </form>
            </div>
          ) : selectedTenant ? (
            <div className="card p-8">
              <h2 className="text-2xl font-bold mb-6">Tenant Settings</h2>
              <form onSubmit={handleUpdateTenant} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Organization Name
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Support Email
                  </label>
                  <input
                    type="email"
                    value={formData.supportEmail}
                    onChange={(e) => setFormData({ ...formData, supportEmail: e.target.value })}
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Brand Tone
                  </label>
                  <select
                    value={formData.tone}
                    onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                    className="input-field"
                  >
                    <option value="professional">Professional</option>
                    <option value="friendly">Friendly</option>
                    <option value="casual">Casual</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    System Prompt
                  </label>
                  <textarea
                    value={formData.systemPrompt}
                    onChange={(e) => setFormData({ ...formData, systemPrompt: e.target.value })}
                    className="input-field h-32 resize-none"
                  />
                </div>

                <button type="submit" className="btn-primary">
                  Save Changes
                </button>
              </form>

              {/* API Key Section */}
              <div className="mt-12 pt-12 border-t">
                <h3 className="text-xl font-bold mb-4">API Key</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-4">
                  <div className="font-mono text-sm break-all">{apiKeyMasked}</div>
                </div>
                <button
                  onClick={generateNewApiKey}
                  className="btn-secondary text-sm"
                >
                  Generate New Key
                </button>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}
