<script setup>
import { computed } from 'vue'

const props = defineProps({
  user: { type: Object, default: null },
  size: { type: String, default: 'md' },
  clickable: { type: Boolean, default: false },
})

const emit = defineEmits(['click'])

const sizeMap = {
  xs: { container: 'w-7 h-7', text: 'text-xs' },
  sm: { container: 'w-8 h-8', text: 'text-xs' },
  md: { container: 'w-9 h-9', text: 'text-sm' },
  lg: { container: 'w-10 h-10', text: 'text-sm' },
  xl: { container: 'w-12 h-12', text: 'text-base' },
  '2xl': { container: 'w-24 h-24', text: 'text-2xl' },
}

const classes = computed(() => {
  const s = sizeMap[props.size] || sizeMap.md
  return `${s.container} ${s.text}`
})

const initial = computed(() => {
  if (!props.user) return '?'
  return (props.user.nickname || props.user.username || '?')[0].toUpperCase()
})
</script>

<template>
  <div
    class="rounded-full bg-maple-200 overflow-hidden flex-shrink-0 flex items-center justify-center font-bold text-maple-600"
    :class="[classes, clickable ? 'cursor-pointer' : '']"
    @click="$emit('click', $event)"
  >
    <img v-if="user?.avatar_url" :src="user.avatar_url" :alt="user?.nickname || 'avatar'" class="w-full h-full object-cover" />
    <span v-else>{{ initial }}</span>
  </div>
</template>