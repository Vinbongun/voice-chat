<template>
  <div class="bg-white border border-gray-100 rounded-2xl p-4 flex items-start gap-4 shadow-sm hover:shadow-md transition-all duration-200">
    <!-- Avatar -->
    <div class="flex-shrink-0">
      <img
        v-if="photo_url"
        :src="photo_url"
        class="w-14 h-14 rounded-full object-cover ring-2 ring-blue-100"
      />
      <div
        v-else
        class="w-14 h-14 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-inner"
        :style="{ background: avatarGradient }"
      >
        {{ initials }}
      </div>
    </div>

    <!-- Info -->
    <div class="flex-1 min-w-0">
      <p class="font-semibold text-gray-900 text-sm leading-tight truncate">{{ name }}</p>
      <p class="text-blue-600 text-xs mt-0.5 truncate">{{ position }}</p>

      <div class="flex flex-wrap items-center gap-x-3 gap-y-0.5 mt-1.5">
        <span v-if="department" class="flex items-center gap-1 text-xs text-gray-500">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-2 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
          {{ department }}
        </span>
        <span v-if="city" class="flex items-center gap-1 text-xs text-gray-500">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          {{ city }}
        </span>
      </div>

      <!-- Contact buttons -->
      <div class="flex flex-wrap gap-2 mt-3">
        <a
          v-if="phone"
          :href="`tel:${phone}`"
          class="inline-flex items-center gap-1.5 bg-gray-50 border border-gray-200 text-gray-700 text-xs px-3 py-1.5 rounded-full hover:bg-gray-100 transition-colors font-medium"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
          {{ phone }}
        </a>
        <a
          v-if="email"
          :href="`mailto:${email}`"
          class="inline-flex items-center gap-1.5 bg-blue-500 text-white text-xs px-3 py-1.5 rounded-full hover:bg-blue-600 transition-colors font-medium"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          Написать
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: String,
  position: String,
  department: String,
  phone: String,
  email: String,
  photo_url: String,
  city: String,
})

const initials = computed(() => {
  if (!props.name) return '?'
  return props.name.split(' ').slice(0, 2).map(w => w[0]).join('')
})

const GRADIENTS = [
  'linear-gradient(135deg, #667eea, #764ba2)',
  'linear-gradient(135deg, #f093fb, #f5576c)',
  'linear-gradient(135deg, #4facfe, #00f2fe)',
  'linear-gradient(135deg, #43e97b, #38f9d7)',
  'linear-gradient(135deg, #fa709a, #fee140)',
  'linear-gradient(135deg, #a18cd1, #fbc2eb)',
  'linear-gradient(135deg, #fd7943, #fda085)',
]

const avatarGradient = computed(() => {
  const idx = (props.name?.charCodeAt(0) || 0) % GRADIENTS.length
  return GRADIENTS[idx]
})
</script>
