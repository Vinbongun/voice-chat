<template>
  <div class="p-4 border-t">
    <p class="text-xs text-gray-400 mb-2">Быстрые действия:</p>
    <div class="flex flex-wrap gap-2">
      <button
        v-for="action in quickActions"
        :key="action.action"
        @click="$emit('action', action.action)"
        class="bg-gray-100 text-gray-700 rounded-full px-3 py-1 text-xs hover:bg-gray-200"
      >
        {{ action.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['action'])
const quickActions = [
  { label: '🏖 Мой отпуск', action: 'my_vacation' },
  { label: '🎫 Мои заявки', action: 'my_tickets' },
  { label: '👥 Найти сотрудника', action: 'find_employee' },
  { label: '📦 Найти товар', action: 'find_product' },
  { label: '🖥 IT помощь', action: 'it_help' },
]
</script>
