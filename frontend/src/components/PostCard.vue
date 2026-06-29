<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { postApi } from '@/api/posts'
import { useFeedStore } from '@/stores/feed'
import { useAuthStore } from '@/stores/auth'
import { relativeTime } from '@/utils/time'
import PostImageGrid from './PostImageGrid.vue'
import PostActions from './PostActions.vue'
import CommentSection from './CommentSection.vue'
import AvatarImage from './AvatarImage.vue'

const props = defineProps({
  post: { type: Object, required: true },
  showActions: { type: Boolean, default: true },
})

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const feedStore = useFeedStore()
const isGuest = computed(() => !authStore.isAuthenticated)
const showFullText = ref(false)
const showComments = ref(false)
const comments = ref([])
const commentsLoaded = ref(false)
const needsTruncation = props.post.content?.length > 150

function toggleComments() {
  showComments.value = !showComments.value
  if (showComments.value && !commentsLoaded.value) {
    loadComments()
  }
}

async function loadComments() {
  try {
    const res = await postApi.comments(props.post.id)
    comments.value = res.data || []
    commentsLoaded.value = true
  } catch { /* ignore */ }
}

function onCommentDeleted(commentId) {
  comments.value = comments.value.filter(comment => comment.id !== commentId)
  if (props.post.comment_count > 0) {
    props.post.comment_count -= 1
  }
}

function goToProfile() {
  const uid = props.post.user?.user_id || props.post.user?.id
  if (uid) router.push(`/profile/${uid}`)
}
</script>

<template>
  <div class="bg-white rounded-2xl shadow-sm border border-border p-5 space-y-3">
    <div class="flex items-center gap-3">
      <AvatarImage :user="post.user" size="sm" clickable @click="goToProfile" />
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium text-text-primary cursor-pointer hover:text-maple-600" @click="goToProfile">
            {{ post.user?.nickname || post.user?.username }}
          </span>
          <span v-if="post.visibility === 'friends'" class="text-[10px] px-1.5 py-0.5 bg-maple-100 text-maple-600 rounded">仅好友</span>
          <span v-if="post.visibility === 'private'" class="text-[10px] px-1.5 py-0.5 bg-gray-100 text-text-secondary rounded">私密</span>
        </div>
        <span class="text-xs text-text-secondary">{{ relativeTime(post.created_at) }}</span>
      </div>
    </div>

    <div v-if="post.content">
      <p class="text-sm text-text-primary leading-relaxed whitespace-pre-wrap break-words" :class="{ 'line-clamp-5': !showFullText && needsTruncation }">
        {{ post.content }}
      </p>
      <button
        v-if="needsTruncation"
        @click="showFullText = !showFullText"
        class="text-xs text-maple-600 hover:text-maple-700 mt-1 cursor-pointer"
      >
        {{ showFullText ? '收起' : '展开全文' }}
      </button>
    </div>

    <PostImageGrid v-if="post.image_urls?.length" :images="post.image_urls" />

    <div v-if="post.files?.length" class="space-y-1">
      <a
        v-for="file in post.files"
        :key="file.id"
        :href="file.file"
        target="_blank"
        class="flex items-center gap-2 text-sm text-maple-600 hover:text-maple-700"
      >
        <span>📎</span>
        <span class="truncate">{{ file.name }}</span>
      </a>
    </div>

    <template v-if="showActions">
      <div v-if="isGuest" class="flex items-center gap-6 text-text-secondary text-sm">
        <RouterLink
          :to="`/login?next=${encodeURIComponent(route.fullPath)}`"
          class="flex items-center gap-1.5 hover:text-maple-600 transition-colors"
        >
          <span class="text-lg">🤍</span>
          <span>{{ post.like_count || '' }}</span>
        </RouterLink>
        <RouterLink
          :to="`/login?next=${encodeURIComponent(route.fullPath)}`"
          class="flex items-center gap-1.5 hover:text-maple-600 transition-colors"
        >
          <span class="text-lg">💬</span>
          <span>{{ post.comment_count || '' }}</span>
        </RouterLink>
      </div>

      <template v-else>
        <PostActions
          :postId="post.id"
          :isLiked="post.is_liked"
          :likeCount="post.like_count"
          :commentCount="post.comment_count"
          @toggle-comments="toggleComments"
        />

        <CommentSection
          :postId="post.id"
          :postAuthorId="post.user?.user_id || post.user?.id"
          :comments="comments"
          :show="showComments"
          @load-comments="loadComments"
          @comment-added="loadComments"
          @comment-deleted="onCommentDeleted"
        />
      </template>
    </template>
  </div>
</template>
