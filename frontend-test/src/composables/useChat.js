import { ref } from 'vue'
import axios from 'axios'

export function useChat() {
  const loading = ref(false)
  const error = ref(null)

  // Simple token for test — in real app comes from Keycloak
  const getAuthHeader = () => {
    const token = localStorage.getItem('test_token') || 'test-token'
    return { Authorization: `Bearer ${token}` }
  }

  const sendMessageSSE = (message, sessionId, onDelta, onDone, onCards) => {
    const token = localStorage.getItem('test_token') || ''
    const params = new URLSearchParams({ message, session_id: sessionId })
    if (token) params.set('token', token)
    const url = `/chat/stream?${params}`

    const eventSource = new EventSource(url)
    loading.value = true

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'text_delta') onDelta(data.delta)
      if (data.type === 'cards') onCards?.(data.cards)
      if (data.type === 'done') {
        loading.value = false
        onDone()
        eventSource.close()
      }
      if (data.type === 'error') {
        error.value = data.message
        loading.value = false
        eventSource.close()
      }
    }

    eventSource.onerror = () => {
      loading.value = false
      eventSource.close()
    }

    return eventSource
  }

  const sendMessagePost = async (message, sessionId) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post('/chat',
        { message, session_id: sessionId },
        { headers: getAuthHeader() }
      )
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return { loading, error, sendMessageSSE, sendMessagePost }
}
