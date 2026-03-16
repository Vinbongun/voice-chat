<template>
  <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-3 flex items-start gap-3">
    <!-- Avatar -->
    <div
      class="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white text-sm font-bold"
      :style="{ background: avatarGradient }"
    >
      <img v-if="photo_url" :src="photo_url" class="w-10 h-10 rounded-full object-cover" />
      <span v-else>{{ initials }}</span>
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <p class="font-semibold text-gray-900 text-sm leading-snug">{{ name }}</p>
      <p class="text-blue-600 text-xs mt-0.5">{{ position }}</p>
      <p class="text-gray-400 text-xs mt-0.5">{{ [department, city].filter(Boolean).join(' · ') }}</p>

      <!-- Contacts -->
      <div class="flex flex-wrap gap-1.5 mt-2">
        <a
          v-if="phone"
          :href="`tel:${phone}`"
          class="inline-flex items-center gap-1 text-xs text-gray-600 bg-gray-50 border border-gray-200 px-2.5 py-1 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <svg class="w-3 h-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
          </svg>
          {{ phone }}
        </a>
        <a
          v-if="email"
          :href="`mailto:${email}`"
          class="inline-flex items-center gap-1 text-xs text-white bg-blue-500 px-2.5 py-1 rounded-lg hover:bg-blue-600 transition-colors"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          Написать
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ name: String, position: String, department: String, phone: String, email: String, photo_url: String, city: String })

const initials = computed(() =>
  (props.name || '?').split(' ').slice(0, 2).map(w => w[0]?.toUpperCase() || '').join('')
)

const GRADIENTS = [
  'linear-gradient(135deg,#667eea,#764ba2)',
  'linear-gradient(135deg,#4facfe,#00f2fe)',
  'linear-gradient(135deg,#43e97b,#38f9d7)',
  'linear-gradient(135deg,#fa709a,#fee140)',
  'linear-gradient(135deg,#f093fb,#f5576c)',
  'linear-gradient(135deg,#fd7943,#fda085)',
  'linear-gradient(135deg,#a18cd1,#fbc2eb)',
]
const avatarGradient = computed(() => GRADIENTS[(props.name?.charCodeAt(0) || 0) % GRADIENTS.length])
</script>
