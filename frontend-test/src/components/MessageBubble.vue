<template>
  <div :class="['flex', message.role === 'user' ? 'justify-end' : 'justify-start']">
    <div :class="[
      'max-w-xs lg:max-w-md px-4 py-2 rounded-2xl text-sm',
      message.role === 'user'
        ? 'bg-blue-500 text-white rounded-tr-none'
        : 'bg-gray-100 text-gray-800 rounded-tl-none'
    ]">
      <p class="whitespace-pre-wrap">{{ message.text }}</p>
      <CardRenderer v-if="message.cards?.length" :cards="message.cards" class="mt-2" />
    </div>
  </div>
</template>

<script setup>
import CardRenderer from './CardRenderer.vue'
defineProps({ message: Object })
</script>
