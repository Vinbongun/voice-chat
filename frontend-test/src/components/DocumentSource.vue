<template>
  <div class="bg-white rounded-xl border border-blue-100 shadow-sm p-3">
    <div class="flex items-start gap-2">
      <div class="w-7 h-7 rounded-lg bg-blue-50 flex items-center justify-center flex-shrink-0 mt-0.5">
        <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
        </svg>
      </div>
      <div class="flex-1 min-w-0">
        <a v-if="url" :href="url" class="font-semibold text-blue-600 text-sm hover:underline leading-snug block">{{ title }}</a>
        <p v-else class="font-semibold text-gray-900 text-sm leading-snug">{{ title }}</p>
        <p v-if="snippet" class="text-gray-500 text-xs mt-1 leading-relaxed line-clamp-3">{{ snippet }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ title: String, url: String, snippet: String, relevance: Number })
</script>
