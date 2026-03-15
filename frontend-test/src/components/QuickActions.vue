<template>
  <div class="p-4 border-t">
    <p class="text-xs text-gray-400 mb-2">Быстрые действия:</p>
    <div class="flex flex-wrap gap-2">
      <button
        v-for="action in quickActions"
        :key="action.label"
        @click="$emit('action', action.text)"
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
  { label: '🏖 Мой отпуск', text: 'Сколько у меня осталось дней отпуска?' },
  { label: '🎫 Мои заявки', text: 'Покажи мои активные заявки' },
  { label: '👥 Найти сотрудника', text: 'Помоги найти сотрудника' },
  { label: '📄 Найти документ', text: 'Найди документ' },
  { label: '🖥 IT помощь', text: 'Создай IT заявку' },
]
</script>
