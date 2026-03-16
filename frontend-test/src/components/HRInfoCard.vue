<template>
  <div class="bg-white rounded-xl border border-purple-100 shadow-sm p-3">
    <div class="flex items-center gap-2 mb-2">
      <div class="w-6 h-6 rounded-lg bg-purple-100 flex items-center justify-center flex-shrink-0">
        <svg class="w-3.5 h-3.5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
      </div>
      <p class="font-semibold text-gray-900 text-sm">{{ title }}</p>
    </div>

    <p v-if="content" class="text-gray-600 text-xs leading-relaxed">{{ content }}</p>

    <div v-if="Object.keys(fields || {}).length" class="mt-2 space-y-1 border-t border-gray-50 pt-2">
      <div v-for="(val, key) in fields" :key="key" class="flex justify-between text-xs">
        <span class="text-gray-400">{{ key }}</span>
        <span class="font-medium text-gray-800">{{ val }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ title: String, content: String, fields: Object })
</script>
