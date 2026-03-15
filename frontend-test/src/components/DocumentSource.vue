<template>
  <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm">
    <a :href="url" class="font-medium text-blue-700 hover:underline">📄 {{ title }}</a>
    <p v-if="snippet" class="text-gray-600 text-xs mt-1 line-clamp-2">{{ snippet }}</p>
    <p v-if="page" class="text-gray-400 text-xs mt-1">Стр. {{ page }}</p>
  </div>
</template>

<script setup>
defineProps({ title: String, url: String, snippet: String, page: Number })
</script>
