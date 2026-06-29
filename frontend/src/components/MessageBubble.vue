<script setup>
import { relativeTime } from '@/utils/time'

const props = defineProps({
  message: { type: Object, required: true },
  isSelf: { type: Boolean, default: false },
})
</script>

<template>
  <div class="flex" :class="isSelf ? 'justify-end' : 'justify-start'">
    <div class="flex gap-2 max-w-[75%]" :class="isSelf ? 'flex-row-reverse' : 'flex-row'">
      <img
        v-if="!isSelf && message.sender_avatar"
        :src="message.sender_avatar"
        class="w-6 h-6 rounded-full flex-shrink-0 mt-1 object-cover"
      />
      <div v-if="!isSelf && !message.sender_avatar" class="w-6 h-6 rounded-full bg-maple-200 flex items-center justify-center text-xs font-bold text-maple-600 flex-shrink-0 mt-1">
        {{ (message.sender_nickname || '?')[0].toUpperCase() }}
      </div>
      <div class="flex flex-col" :class="isSelf ? 'items-end' : 'items-start'">
        <span v-if="!isSelf && message.sender_nickname" class="text-xs text-text-secondary mb-0.5 ml-1">
          {{ message.sender_nickname }}
        </span>
        <div
          class="px-3.5 py-2 text-sm leading-relaxed whitespace-pre-wrap break-words"
          :class="isSelf
            ? 'bg-maple-600 text-white rounded-[16px_16px_4px_16px]'
            : 'bg-white text-text-primary border border-border rounded-[16px_16px_16px_4px]'"
        >
          {{ message.content }}
        </div>
        <span class="text-[12px] text-text-secondary mt-0.5 px-1">
          {{ relativeTime(message.created_at) }}
        </span>
      </div>
    </div>
  </div>
</template>
