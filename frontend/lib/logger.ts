// Browser logger for development
type LogLevel = 'info' | 'warn' | 'error' | 'debug' | 'success'

const colors = {
  info: 'color: #3b82f6; font-weight: bold;',
  warn: 'color: #f59e0b; font-weight: bold;',
  error: 'color: #ef4444; font-weight: bold;',
  debug: 'color: #8b5cf6; font-weight: bold;',
  success: 'color: #10b981; font-weight: bold;',
}

const getTimestamp = () => new Date().toISOString().split('T')[1].slice(0, 8)

export const logger = {
  info: (message: string, data?: any) => {
    console.log(`%c[${getTimestamp()}] ℹ️  ${message}`, colors.info, data || '')
  },

  warn: (message: string, data?: any) => {
    console.warn(`%c[${getTimestamp()}] ⚠️  ${message}`, colors.warn, data || '')
  },

  error: (message: string, data?: any) => {
    console.error(`%c[${getTimestamp()}] ✗ ${message}`, colors.error, data || '')
  },

  debug: (message: string, data?: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.debug(`%c[${getTimestamp()}] 🔧 ${message}`, colors.debug, data || '')
    }
  },

  success: (message: string, data?: any) => {
    console.log(`%c[${getTimestamp()}] ✓ ${message}`, colors.success, data || '')
  },

  // API calls
  api: (method: string, endpoint: string, status?: number) => {
    const statusColor = status && status < 400 ? colors.success : colors.error
    console.log(
      `%c[${getTimestamp()}] 🌐 ${method} ${endpoint}${status ? ` (${status})` : ''}`,
      statusColor
    )
  },

  // Page navigation
  navigation: (page: string) => {
    console.log(`%c[${getTimestamp()}] 📄 Navigating to ${page}`, colors.info)
  },

  // User actions
  action: (action: string, details?: any) => {
    console.log(`%c[${getTimestamp()}] 👆 ${action}`, colors.debug, details || '')
  },
}

export default logger
