<template>
  <div class="bg-purple-50 border border-purple-200 rounded-lg p-3">
    <p class="text-sm font-medium text-purple-800 mb-2">{{ title }}</p>
    <p class="text-sm text-gray-700">{{ content }}</p>
    <div v-if="Object.keys(fields || {}).length" class="mt-2 space-y-1">
      <div v-for="(val, key) in fields" :key="key" class="flex justify-between text-xs">
        <span class="text-gray-500">{{ key }}</span>
        <span class="font-medium text-gray-800">{{ val }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ title: String, content: String, fields: Object })
</script>
