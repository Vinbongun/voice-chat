import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './style.css'

// Dev: pre-populate test token so SSE auth works without Keycloak
if (!localStorage.getItem('test_token')) {
  localStorage.setItem('test_token',
    'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9' +
    '.eyJzdWIiOiAidGVzdC11c2VyLTAwMSIsICJuYW1lIjogIlRlc3QgVXNlciIsICJlbWFpbCI6ICJ0ZXN0QGV4YW1wbGUuY29tIiwgImV4cCI6IDE4MDUxODIyMzgsICJpYXQiOiAxNzczNjQ2MjM4fQ' +
    '.FBuy4dp7ar3mFXcuBUNDizWN15EWPpvgcdZH8rd3QoY'
  )
}

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
