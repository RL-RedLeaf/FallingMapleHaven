<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useFeedStore } from '@/stores/feed'
import { useAuthStore } from '@/stores/auth'
import { postApi } from '@/api/posts'
import PostCard from '@/components/PostCard.vue'
import AvatarImage from '@/components/AvatarImage.vue'
import { useToast } from '@/composables/useToast'

const feedStore = useFeedStore()
const authStore = useAuthStore()

const isGuest = computed(() => !authStore.isAuthenticated)
const toast = useToast()
const showCreateForm = ref(false)
const newContent = ref('')
const newImages = ref([])
const newVisibility = ref('public')
const newTag = ref('')
const submitting = ref(false)
const imageInput = ref(null)
const activeTag = ref('all')

const tags = [
  { key: 'all', label: '全部' },
  { key: 'chat', label: '#闲聊' },
  { key: 'share', label: '#分享' },
  { key: 'help', label: '#求助' },
  { key: 'question', label: '#提问' },
  { key: 'daily', label: '#日常' },
]

const tagParams = computed(() => {
  if (activeTag.value === 'all') return {}
  return { topic: activeTag.value }
})

onMounted(async () => {
  feedStore.currentPage = 1
  feedStore.hasMore = true
  await feedStore.fetchPosts(tagParams.value)
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

function handleScroll() {
  if (feedStore.loading || !feedStore.hasMore) return
  const scrollBottom = window.innerHeight + window.scrollY
  const threshold = document.documentElement.scrollHeight - 200
  if (scrollBottom >= threshold) {
    feedStore.currentPage++
    feedStore.fetchPosts(tagParams.value)
  }
}

function switchTag(tag) {
  if (activeTag.value === tag) return
  activeTag.value = tag
  feedStore.currentPage = 1
  feedStore.hasMore = true
  feedStore.posts = []
  feedStore.fetchPosts(tagParams.value)
}

function triggerImagePick() {
  imageInput.value?.click()
}

function handleImagePick(e) {
  const files = Array.from(e.target.files || [])
  for (const file of files) {
    if (newImages.value.length >= 9) break
    const url = URL.createObjectURL(file)
    newImages.value.push({ file, url })
  }
  e.target.value = ''
}

function removeImage(index) {
  URL.revokeObjectURL(newImages.value[index].url)
  newImages.value.splice(index, 1)
}

async function submitPost() {
  if (!newContent.value.trim() && !newImages.value.length) return
  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('content', newContent.value.trim())
    formData.append('visibility', newVisibility.value)
    if (newTag.value) formData.append('topic_tag', newTag.value)
    for (const img of newImages.value) {
      formData.append('images', img.file)
    }
    await feedStore.createPost(formData)
    newContent.value = ''
    newVisibility.value = 'public'
    newTag.value = ''
    for (const img of newImages.value) URL.revokeObjectURL(img.url)
    newImages.value = []
    showCreateForm.value = false
    toast.success('发布成功')
  } catch { /* ignore */ } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-maple-700 mb-6">广场</h1>

    <div v-if="isGuest" class="bg-white rounded-2xl shadow-sm border border-border p-6 mb-6 text-center">
      <p class="text-text-secondary mb-4">登录后即可发布动态、点赞和评论</p>
      <div class="flex items-center justify-center gap-3">
        <RouterLink
          to="/login?next=/"
          class="px-6 py-2 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors"
        >
          登录
        </RouterLink>
        <RouterLink
          to="/register?next=/"
          class="px-6 py-2 border border-maple-600 text-maple-600 text-sm rounded-lg hover:bg-maple-50 transition-colors"
        >
          注册
        </RouterLink>
      </div>
    </div>

    <div v-else class="bg-white rounded-2xl shadow-sm border border-border p-5 mb-6">
      <div v-if="!showCreateForm" class="flex items-center gap-3">
        <AvatarImage :user="authStore.user" size="md" />

        <button
          @click="showCreateForm = true"
          class="flex-1 text-left px-4 py-2.5 border border-border rounded-full text-sm text-text-secondary hover:border-maple-300 hover:text-maple-600 transition-colors cursor-pointer"
        >
          分享你的想法...
        </button>
      </div>

      <div v-else class="space-y-4">
        <div class="flex items-center gap-3">
          <AvatarImage :user="authStore.user" size="md" />

          <span class="text-sm font-medium text-text-primary">{{ authStore.user?.nickname || authStore.user?.username }}</span>
        </div>

        <textarea
          v-model="newContent"
          rows="4"
          placeholder="分享你的想法..."
          class="w-full px-4 py-3 border border-border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600 resize-none"
        />

        <div v-if="newImages.length" class="flex flex-wrap gap-2">
          <div v-for="(img, i) in newImages" :key="i" class="relative w-20 h-20 rounded-lg overflow-hidden group">
            <img :src="img.url" class="w-full h-full object-cover" />
            <button
              @click="removeImage(i)"
              class="absolute top-1 right-1 w-5 h-5 bg-black/50 text-white rounded-full text-xs flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
            >
              ×
            </button>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="triggerImagePick"
            class="text-sm text-text-secondary hover:text-maple-600 transition-colors cursor-pointer"
          >
            📷 图片
          </button>
          <input ref="imageInput" type="file" accept="image/*" multiple class="hidden" @change="handleImagePick" />

          <select
            v-model="newVisibility"
            class="text-sm border border-border rounded-lg px-2 py-1 focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600"
          >
            <option value="public">公开</option>
            <option value="friends">仅好友</option>
            <option value="private">私密</option>
          </select>

          <select v-model="newTag" class="text-sm border border-border rounded-lg px-2 py-1 focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600">
            <option value="">选择话题</option>
            <option v-for="tag in tags.filter(t => t.key !== 'all')" :key="tag.key" :value="tag.key">{{ tag.label }}</option>
          </select>

          <div class="flex-1" />

          <button
            @click="showCreateForm = false"
            class="px-3 py-1.5 text-sm text-text-secondary hover:text-maple-600 transition-colors cursor-pointer"
          >
            取消
          </button>
          <button
            @click="submitPost"
            :disabled="submitting || (!newContent.trim() && !newImages.length)"
            class="px-5 py-1.5 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors disabled:opacity-50 cursor-pointer"
          >
            {{ submitting ? '发布中...' : '发布' }}
          </button>
        </div>
      </div>
    </div>

    <div class="flex gap-2 mb-6 overflow-x-auto pb-2 scrollbar-hide">
      <button
        v-for="tag in tags"
        :key="tag.key"
        @click="switchTag(tag.key)"
        class="px-4 py-1.5 text-sm rounded-full whitespace-nowrap transition-colors cursor-pointer"
        :class="activeTag === tag.key ? 'bg-maple-600 text-white' : 'bg-white text-text-secondary border border-border hover:border-maple-300'"
      >
        {{ tag.label }}
      </button>
    </div>

    <div v-if="feedStore.loading && !feedStore.posts.length" class="text-center text-text-secondary py-12">
      加载中...
    </div>

    <template v-if="!feedStore.loading || feedStore.posts.length">
      <div v-if="!feedStore.posts.length" class="text-center text-text-secondary py-12">
        {{ isGuest ? '暂无公开动态' : '暂无动态，快来发布第一条吧' }}
      </div>
      <div v-else class="space-y-4">
        <PostCard v-for="post in feedStore.posts" :key="post.id" :post="post" />
        <div v-if="feedStore.loading" class="text-center text-text-secondary py-4">
          加载更多...
        </div>
        <div v-if="!feedStore.hasMore && feedStore.posts.length" class="text-center text-text-secondary py-4 text-sm">
          没有更多了
        </div>
      </div>
    </template>
  </div>
</template>
