import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const SESSION_KEY = 'chat_session_id'

export const useChatStore = defineStore('chat', () => {
  const sessionId = ref(null)
  const messages = ref([])
  const isLoading = ref(false)

  async function initSession() {
    // Restore or create session ID
    sessionId.value = localStorage.getItem(SESSION_KEY) || _uuid()
    localStorage.setItem(SESSION_KEY, sessionId.value)

    // Load history from DB
    try {
      const { data } = await axios.get(`/chat/history?session_id=${sessionId.value}`)
      if (data.messages?.length) {
        messages.value = data.messages
      }
    } catch {
      // DB history unavailable — start fresh
    }
  }

  function addUserMessage(text) {
    messages.value.push({ role: 'user', text, cards: [], timestamp: Date.now() })
  }

  function appendDelta(delta) {
    const last = messages.value[messages.value.length - 1]
    if (last?.role === 'assistant') {
      last.text += delta
    } else {
      messages.value.push({ role: 'assistant', text: delta, cards: [], timestamp: Date.now() })
    }
  }

  function saveAssistantMessage() {
    // No-op — messages are saved to DB by the backend on each request
  }

  function clearHistory() {
    messages.value = []
    sessionId.value = _uuid()
    localStorage.setItem(SESSION_KEY, sessionId.value)
  }

  function _uuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16)
    })
  }

  return { sessionId, messages, isLoading, initSession, addUserMessage, appendDelta, saveAssistantMessage, clearHistory }
})
