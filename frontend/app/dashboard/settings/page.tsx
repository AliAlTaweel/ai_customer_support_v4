'use client'

import { useEffect, useState } from 'react'
import { tenantApi, apiKeyApi } from '@/lib/api'
import toast from 'react-hot-toast'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'

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

  const deleteTenant = async (tenantId: string) => {
    if (!tenantId) return

    try {
      await tenantApi.delete(tenantId)
      toast.success('Tenant deleted successfully')
      setSelectedTenant(null)
      setShowNewTenantForm(false)
      await fetchTenants()
    } catch (error) {
      console.error('Failed to delete tenant:', error)
      toast.error('Failed to delete tenant')
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
          <Card>
            <CardHeader>
              <CardTitle>Tenants</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
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
              <Button
                onClick={() => setShowNewTenantForm(!showNewTenantForm)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
              >
                {showNewTenantForm ? 'Cancel' : '+ New Tenant'}
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Settings Form */}
        <div className="lg:col-span-3">
          {showNewTenantForm ? (
            <Card>
              <CardHeader>
                <CardTitle>Create New Tenant</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCreateTenant} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Organization Name *
                    </label>
                    <Input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                      placeholder="Your company name"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Support Email *
                    </label>
                    <Input
                      type="email"
                      value={formData.supportEmail}
                      onChange={(e) => setFormData({ ...formData, supportEmail: e.target.value })}
                      required
                      placeholder="support@example.com"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Brand Tone
                    </label>
                    <select
                      value={formData.tone}
                      onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md"
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
                      className="w-full px-3 py-2 border border-gray-300 rounded-md h-32 resize-none"
                      placeholder="Custom instructions for the AI agent..."
                    />
                  </div>

                  <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white">
                    Create Tenant
                  </Button>
                </form>
              </CardContent>
            </Card>
          ) : selectedTenant ? (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Tenant Settings</CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleUpdateTenant} className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Organization Name
                      </label>
                      <Input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Support Email
                      </label>
                      <Input
                        type="email"
                        value={formData.supportEmail}
                        onChange={(e) => setFormData({ ...formData, supportEmail: e.target.value })}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Brand Tone
                      </label>
                      <select
                        value={formData.tone}
                        onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
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
                        className="w-full px-3 py-2 border border-gray-300 rounded-md h-32 resize-none"
                      />
                    </div>

                    <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white">
                      Save Changes
                    </Button>
                  </form>
                </CardContent>
              </Card>

              {/* API Key Section */}
              <Card>
                <CardHeader>
                  <CardTitle>API Key</CardTitle>
                  <CardDescription>Use this key to authenticate API requests</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="bg-gray-50 p-4 rounded-lg font-mono text-sm break-all">
                    {apiKeyMasked}
                  </div>
                  <Button onClick={generateNewApiKey} className="bg-blue-600 hover:bg-blue-700 text-white">
                    Generate New Key
                  </Button>
                </CardContent>
              </Card>

              {/* Danger Zone */}
              <Card className="border-red-200 bg-red-50">
                <CardHeader>
                  <CardTitle className="text-red-600">Danger Zone</CardTitle>
                  <CardDescription>Irreversible actions</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">
                    Deleting this tenant will permanently remove all data including cases, integrations, and configurations.
                  </p>
                  <Button
                    onClick={() => {
                      if (confirm(`Are you sure you want to delete "${selectedTenant?.name}"? This cannot be undone.`)) {
                        deleteTenant(selectedTenant?.id || '')
                      }
                    }}
                    className="bg-red-600 hover:bg-red-700 text-white"
                  >
                    Delete Tenant
                  </Button>
                </CardContent>
              </Card>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}
