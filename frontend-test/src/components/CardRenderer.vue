<template>
  <div class="space-y-2">
    <component
      v-for="(card, i) in cards"
      :key="i"
      :is="CARD_COMPONENTS[card.type]"
      v-bind="card"
    />
  </div>
</template>

<script setup>
import { defineAsyncComponent } from 'vue'

const CARD_COMPONENTS = {
  employee:      defineAsyncComponent(() => import('./EmployeeCard.vue')),
  product:       defineAsyncComponent(() => import('./ProductCard.vue')),
  hr_info:       defineAsyncComponent(() => import('./HRInfoCard.vue')),
  document:      defineAsyncComponent(() => import('./DocumentSource.vue')),
  news:          defineAsyncComponent(() => import('./NewsCard.vue')),
  ticket:        defineAsyncComponent(() => import('./TicketCard.vue')),
  action_button: defineAsyncComponent(() => import('./ActionButtons.vue')),
}

defineProps({ cards: Array })
</script>
