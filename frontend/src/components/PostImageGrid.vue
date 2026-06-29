<script setup>
defineProps({
  images: { type: Array, required: true },
})
</script>

<template>
  <div v-if="images.length === 1" class="max-w-[400px]">
    <img :src="images[0]" class="w-full h-auto max-h-[400px] object-cover rounded-lg" />
  </div>
  <div v-else-if="images.length === 2" class="grid grid-cols-2 gap-2">
    <img v-for="(img, i) in images" :key="i" :src="img" class="w-full h-48 object-cover rounded-lg" />
  </div>
  <div v-else-if="images.length === 3" class="grid grid-cols-2 gap-2">
    <img :src="images[0]" class="w-full h-64 object-cover rounded-lg row-span-2" />
    <img :src="images[1]" class="w-full h-[7.5rem] object-cover rounded-lg" />
    <img :src="images[2]" class="w-full h-[7.5rem] object-cover rounded-lg" />
  </div>
  <div v-else-if="images.length === 4" class="grid grid-cols-2 gap-2">
    <img v-for="(img, i) in images" :key="i" :src="img" class="w-full h-36 object-cover rounded-lg" />
  </div>
  <div v-else class="grid grid-cols-3 gap-2">
    <img v-for="(img, i) in images" :key="i" :src="img" class="w-full h-32 object-cover rounded-lg" />
  </div>
</template>
