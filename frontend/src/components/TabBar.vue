<script setup>
defineProps({
  tabs: { type: Array, required: true },
  activeKey: { type: String, required: true },
})

const emit = defineEmits(['update:activeKey'])
</script>

<template>
  <div class="flex gap-1 bg-maple-100 rounded-xl p-1">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      @click="emit('update:activeKey', tab.key)"
      class="flex-1 py-2 text-sm font-medium rounded-lg transition-colors cursor-pointer"
      :class="activeKey === tab.key ? 'bg-white text-maple-600 shadow-sm' : 'text-text-secondary hover:text-maple-600'"
    >
      {{ tab.label }}
    </button>
  </div>
</template>