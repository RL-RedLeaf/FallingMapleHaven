<script setup>
import { useFeedStore } from '@/stores/feed'

const props = defineProps({
  postId: { type: Number, required: true },
  isLiked: { type: Boolean, default: false },
  likeCount: { type: Number, default: 0 },
  commentCount: { type: Number, default: 0 },
})

const emit = defineEmits(['toggle-comments'])
const feedStore = useFeedStore()

function handleLike() {
  feedStore.toggleLike(props.postId)
}
</script>

<template>
  <div class="flex items-center gap-6 text-text-secondary text-sm">
    <button
      @click="handleLike"
      class="flex items-center gap-1.5 hover:text-maple-600 transition-colors cursor-pointer"
      :class="{ 'text-red-500': isLiked }"
    >
      <span class="text-lg">{{ isLiked ? '❤️' : '🤍' }}</span>
      <span>{{ likeCount || '' }}</span>
    </button>
    <button
      @click="emit('toggle-comments')"
      class="flex items-center gap-1.5 hover:text-maple-600 transition-colors cursor-pointer"
    >
      <span class="text-lg">💬</span>
      <span>{{ commentCount || '' }}</span>
    </button>
  </div>
</template>
