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
  employee: defineAsyncComponent(() => import('./EmployeeCard.vue')),
  document: defineAsyncComponent(() => import('./DocumentSource.vue')),
  action_button: defineAsyncComponent(() => import('./ActionButtons.vue')),
}
defineProps({ cards: Array })
</script>
