<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
    <div class="w-full max-w-2xl">
      <h1 class="text-2xl font-bold text-center mb-4 text-gray-800">Чат-бот сотрудника</h1>
      <ChatWindow />
    </div>
  </div>
</template>

<script setup>
import ChatWindow from './components/ChatWindow.vue'
</script>
