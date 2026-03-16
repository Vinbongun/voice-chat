<template>
  <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-3">
    <div class="flex items-start justify-between gap-2">
      <div class="flex items-start gap-2 flex-1 min-w-0">
        <div class="w-7 h-7 rounded-lg bg-indigo-50 flex items-center justify-center flex-shrink-0 mt-0.5">
          <svg class="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
        </div>
        <div class="flex-1 min-w-0">
          <p class="font-semibold text-gray-900 text-sm leading-snug">{{ title || 'Заявка #' + id }}</p>
          <p v-if="category" class="text-gray-400 text-xs mt-0.5">{{ category }}</p>
        </div>
      </div>
      <span :class="['text-xs px-2 py-0.5 rounded-full font-medium flex-shrink-0', statusStyle]">
        {{ statusLabel }}
      </span>
    </div>
    <div v-if="created_at" class="mt-2 text-gray-400 text-xs">
      Создана: {{ formatDate(created_at) }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ id: String, title: String, status: String, category: String, created_at: String, updated_at: String })

const STATUS_MAP = {
  active:   { label: 'В работе',  cls: 'bg-blue-100 text-blue-700' },
  open:     { label: 'Открыта',   cls: 'bg-yellow-100 text-yellow-700' },
  closed:   { label: 'Закрыта',   cls: 'bg-gray-100 text-gray-500' },
  resolved: { label: 'Решена',    cls: 'bg-green-100 text-green-700' },
  created:  { label: 'Создана',   cls: 'bg-purple-100 text-purple-700' },
}
const statusLabel = computed(() => STATUS_MAP[props.status]?.label || props.status || 'Неизвестно')
const statusStyle = computed(() => STATUS_MAP[props.status]?.cls || 'bg-gray-100 text-gray-500')

const formatDate = (d) => {
  try { return new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' }) }
  catch { return d }
}
</script>
