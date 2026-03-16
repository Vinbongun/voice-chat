<template>
  <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-3">
    <div class="flex items-start gap-2">
      <div class="w-7 h-7 rounded-lg bg-orange-50 flex items-center justify-center flex-shrink-0 mt-0.5">
        <svg class="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/>
        </svg>
      </div>
      <div class="flex-1 min-w-0">
        <p class="font-semibold text-gray-900 text-sm leading-snug">{{ title }}</p>
        <p v-if="published_at" class="text-gray-400 text-xs mt-0.5">{{ formatDate(published_at) }}</p>
      </div>
    </div>
    <p class="text-gray-600 text-xs mt-2 leading-relaxed">{{ content }}</p>
  </div>
</template>

<script setup>
const props = defineProps({ id: String, title: String, content: String, published_at: String })

const formatDate = (d) => {
  try { return new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }) }
  catch { return d }
}
</script>
