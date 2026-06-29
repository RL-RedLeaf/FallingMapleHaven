<script setup>
import Icon from './Icon.vue'

defineProps({
  plugins: { type: Array, default: () => [] },
})

const emit = defineEmits(['navigate'])

const iconMap = {
  'help-circle': 'helpCircle',
  'message-question': 'messageCircleMore',
}
</script>

<template>
  <div class="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
    <button
      v-for="plugin in plugins"
      :key="plugin.route"
      @click="emit('navigate', plugin)"
      class="flex items-center gap-2.5 px-4 py-3 bg-white rounded-xl border border-border shadow-card hover:border-maple-300 hover:shadow-float transition-all flex-shrink-0 cursor-pointer min-h-[44px]"
    >
      <Icon :name="iconMap[plugin.icon] || plugin.icon || 'gift'" :size="20" class="text-maple-600" />
      <div class="text-left">
        <div class="text-sm font-medium text-text-primary">{{ plugin.name }}</div>
        <div class="text-tag text-text-secondary">{{ plugin.desc }}</div>
      </div>
      <Icon name="chevronRight" :size="16" class="text-text-secondary flex-shrink-0" />
    </button>
  </div>
</template>
