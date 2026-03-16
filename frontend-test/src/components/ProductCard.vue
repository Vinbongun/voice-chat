<template>
  <div class="bg-white rounded-xl border border-gray-100 shadow-sm p-3">
    <div class="flex gap-3">
      <!-- Image / placeholder -->
      <div class="w-14 h-14 rounded-lg overflow-hidden flex-shrink-0 bg-gray-50 flex items-center justify-center">
        <img v-if="photo_url" :src="photo_url" class="w-full h-full object-cover" />
        <svg v-else class="w-7 h-7 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
        </svg>
      </div>

      <div class="flex-1 min-w-0">
        <p class="font-semibold text-gray-900 text-sm leading-snug">{{ name }}</p>
        <p v-if="brand" class="text-gray-400 text-xs mt-0.5">{{ brand }}</p>
        <p v-if="price" class="text-blue-600 font-bold text-sm mt-1">{{ formatPrice(price) }} ₽</p>
        <p v-else class="text-gray-400 text-xs mt-1">Цена по запросу</p>
      </div>
    </div>

    <p v-if="description" class="text-gray-500 text-xs mt-2 leading-relaxed line-clamp-2">{{ description }}</p>

    <!-- Availability -->
    <div v-if="availability?.length" class="mt-2 flex flex-wrap gap-1">
      <span
        v-for="a in availability" :key="a.branch"
        :class="['text-xs px-2 py-0.5 rounded-full', a.qty > 0 ? 'bg-green-50 text-green-700 border border-green-100' : 'bg-red-50 text-red-600 border border-red-100']"
      >
        {{ a.branch }}: {{ a.qty > 0 ? a.qty + ' шт' : 'нет' }}
      </span>
    </div>

    <a v-if="url" :href="url" class="inline-flex items-center gap-1 text-xs text-blue-500 hover:underline mt-2">
      Подробнее
      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
    </a>
  </div>
</template>

<script setup>
defineProps({ name: String, brand: String, description: String, photo_url: String, price: Number, availability: Array, url: String })
const formatPrice = (p) => new Intl.NumberFormat('ru-RU').format(p)
</script>
