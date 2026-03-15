<template>
  <button
    @click="$emit('action', action, payload)"
    class="bg-blue-100 text-blue-700 rounded-lg px-3 py-1.5 text-sm font-medium hover:bg-blue-200"
  >
    {{ label }}
  </button>
</template>

<script setup>
defineProps({ label: String, action: String, payload: Object })
defineEmits(['action'])
</script>
