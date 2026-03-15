import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const sessionId = ref(null)
  const messages = ref([])
  const isLoading = ref(false)

  function initSession() {
    if (!sessionId.value) {
      // Simple UUID generation without external dep
      sessionId.value = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = Math.random() * 16 | 0
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16)
      })
    }
  }

  function addUserMessage(text) {
    messages.value.push({ role: 'user', text, timestamp: Date.now() })
  }

  function addAssistantMessage(text, cards = [], sources = []) {
    messages.value.push({ role: 'assistant', text, cards, sources, timestamp: Date.now() })
  }

  function appendDelta(delta) {
    const last = messages.value[messages.value.length - 1]
    if (last?.role === 'assistant') {
      last.text += delta
    } else {
      messages.value.push({ role: 'assistant', text: delta, cards: [], sources: [], timestamp: Date.now() })
    }
  }

  function clearHistory() {
    messages.value = []
    sessionId.value = null
  }

  return { sessionId, messages, isLoading, initSession, addUserMessage, addAssistantMessage, appendDelta, clearHistory }
})
