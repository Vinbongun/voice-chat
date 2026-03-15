<template>
  <div class="bg-white border rounded-lg p-3 flex items-start gap-3 shadow-sm">
    <img v-if="photo_url" :src="photo_url" class="w-10 h-10 rounded-full object-cover" />
    <div v-else class="w-10 h-10 rounded-full bg-blue-200 flex items-center justify-center text-blue-600 font-bold text-sm">
      {{ name?.[0] }}
    </div>
    <div class="flex-1 min-w-0">
      <p class="font-medium text-gray-900 text-sm">{{ name }}</p>
      <p class="text-xs text-gray-500">{{ position }}</p>
      <p class="text-xs text-gray-400">{{ department }} · {{ city }}</p>
      <div class="flex gap-2 mt-2">
        <a v-if="phone" :href="`tel:${phone}`" class="text-xs text-blue-500 hover:underline">📞 {{ phone }}</a>
        <a v-if="email" :href="`mailto:${email}`" class="text-xs text-blue-500 hover:underline">✉ Написать</a>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ name: String, position: String, department: String, phone: String, email: String, photo_url: String, city: String })
</script>
