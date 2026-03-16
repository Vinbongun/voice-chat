<template>
  <div class="bg-white border rounded-lg p-3 shadow-sm">
    <div class="flex gap-3">
      <img v-if="photo_url" :src="photo_url" class="w-16 h-16 object-cover rounded" />
      <div v-else class="w-16 h-16 bg-gray-100 rounded flex items-center justify-center text-2xl">🛒</div>
      <div class="flex-1 min-w-0">
        <p class="font-medium text-gray-900 text-sm">{{ name }}</p>
        <p v-if="brand" class="text-xs text-gray-500">{{ brand }}</p>
        <p v-if="price" class="text-sm font-semibold text-blue-600 mt-1">{{ formatPrice(price) }} ₽</p>
        <p v-else class="text-xs text-gray-400 mt-1">Цена по запросу</p>
      </div>
    </div>
    <p v-if="description" class="text-xs text-gray-600 mt-2 line-clamp-2">{{ description }}</p>
    <div v-if="availability?.length" class="mt-2">
      <p class="text-xs text-gray-400 font-medium mb-1">Наличие:</p>
      <div class="flex flex-wrap gap-1">
        <span
          v-for="a in availability"
          :key="a.branch"
          :class="['text-xs px-2 py-0.5 rounded-full', a.qty > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']"
        >
          {{ a.branch }}: {{ a.qty > 0 ? a.qty + ' шт' : 'нет' }}
        </span>
      </div>
    </div>
    <a v-if="url" :href="url" class="text-xs text-blue-500 hover:underline mt-2 block">Подробнее →</a>
  </div>
</template>

<script setup>
defineProps({
  name: String, brand: String, description: String,
  photo_url: String, price: Number, availability: Array, url: String
})

const formatPrice = (p) => new Intl.NumberFormat('ru-RU').format(p)
</script>
