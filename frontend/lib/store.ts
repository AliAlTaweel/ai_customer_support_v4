import { create } from 'zustand'

interface Tenant {
  id: string
  name: string
  logo?: string
  colors?: Record<string, string>
  systemPrompt: string
  tone: string
  supportEmail: string
  apiKey: string
  status: string
  plan: string
}

interface TenantStore {
  currentTenant: Tenant | null
  setCurrentTenant: (tenant: Tenant) => void
  clearCurrentTenant: () => void
}

export const useTenantStore = create<TenantStore>((set) => ({
  currentTenant: null,
  setCurrentTenant: (tenant: Tenant) => set({ currentTenant: tenant }),
  clearCurrentTenant: () => set({ currentTenant: null }),
}))

interface UIStore {
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

export const useUIStore = create<UIStore>((set) => ({
  isLoading: false,
  setIsLoading: (loading: boolean) => set({ isLoading: loading }),
}))
