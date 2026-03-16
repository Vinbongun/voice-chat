import { defineStore } from 'pinia'
import { ref } from 'vue'

const STORAGE_KEY = 'chat_history'

export const useChatStore = defineStore('chat', () => {
  const sessionId = ref(null)
  const messages = ref([])
  const isLoading = ref(false)

  function initSession() {
    const saved = _loadFromStorage()
    if (saved) {
      sessionId.value = saved.sessionId
      messages.value = saved.messages
    }
    if (!sessionId.value) {
      sessionId.value = _uuid()
    }
  }

  function addUserMessage(text) {
    messages.value.push({ role: 'user', text, timestamp: Date.now() })
    _saveToStorage()
  }

  function appendDelta(delta) {
    const last = messages.value[messages.value.length - 1]
    if (last?.role === 'assistant') {
      last.text += delta
    } else {
      messages.value.push({ role: 'assistant', text: delta, cards: [], sources: [], timestamp: Date.now() })
    }
    _saveToStorage()
  }

  function saveAssistantMessage() {
    _saveToStorage()
  }

  function clearHistory() {
    messages.value = []
    sessionId.value = _uuid()
    localStorage.removeItem(STORAGE_KEY)
  }

  function _saveToStorage() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        sessionId: sessionId.value,
        messages: messages.value.slice(-50), // keep last 50
      }))
    } catch {}
  }

  function _loadFromStorage() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      return raw ? JSON.parse(raw) : null
    } catch {
      return null
    }
  }

  function _uuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16)
    })
  }

  return { sessionId, messages, isLoading, initSession, addUserMessage, appendDelta, saveAssistantMessage, clearHistory }
})
