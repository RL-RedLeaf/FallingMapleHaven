<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { profileApi } from '@/api/profiles'
import { relativeTime } from '@/utils/time'
import PostCard from '@/components/PostCard.vue'
import FriendButton from '@/components/FriendButton.vue'
import AvatarImage from '@/components/AvatarImage.vue'
import TabBar from '@/components/TabBar.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const profile = ref(null)
const loading = ref(true)
const activeTab = ref('posts')
const posts = ref([])
const visitors = ref([])
const guestbookEntries = ref([])
const guestbookContent = ref('')
const submittingGuestbook = ref(false)
const postsLoading = ref(false)

const userId = computed(() => {
  const raw = route.params.userId
  const num = Number(raw)
  return isNaN(num) ? raw : num
})
const isGuest = computed(() => !authStore.isAuthenticated)
const isOwner = computed(() => authStore.user?.user_id === userId.value)

const tabs = computed(() => {
  const items = [
    { key: 'posts', label: '动态' },
    { key: 'guestbook', label: '留言板' },
  ]
  if (!isGuest.value) {
    items.splice(1, 0, { key: 'visitors', label: '访客' })
  }
  return items
})

const iconMap = { 'help-circle': '❓', 'message-question': '📬' }
const pluginCards = computed(() => {
  const cards = (profile.value?.plugins || []).map(p => ({
    name: p.name,
    icon: iconMap[p.icon] || '🔌',
    desc: p.description,
    route: p.route,
  }))
  cards.push({
    name: '留言板', icon: '✍️', desc: '给我留言',
    route: `/profile/${userId.value}/guestbook`,
  })
  return cards
})

onMounted(async () => {
  await Promise.all([fetchProfile(), fetchPosts()])
})

async function fetchProfile() {
  loading.value = true
  try {
    const res = await profileApi.get(userId.value)
    profile.value = res.data
  } catch { /* ignore */ } finally {
    loading.value = false
  }
}

async function fetchPosts() {
  postsLoading.value = true
  try {
    const res = await profileApi.posts(userId.value, { page: 1, page_size: 20 })
    posts.value = res.data?.results || []
  } catch { /* ignore */ } finally {
    postsLoading.value = false
  }
}

async function fetchVisitors() {
  if (visitors.value.length) return
  try {
    const res = await profileApi.visitors(userId.value, { page: 1, page_size: 20 })
    visitors.value = res.data?.results || []
  } catch { /* ignore */ }
}

async function fetchGuestbook() {
  if (guestbookEntries.value.length) return
  try {
    const res = await profileApi.guestbook(userId.value, { page: 1, page_size: 20 })
    guestbookEntries.value = res.data?.results || []
  } catch { /* ignore */ }
}

function onTabChange(tab) {
  activeTab.value = tab
  if (tab === 'visitors') fetchVisitors()
  if (tab === 'guestbook') fetchGuestbook()
}

async function submitGuestbook() {
  if (!guestbookContent.value.trim()) return
  submittingGuestbook.value = true
  try {
    const res = await profileApi.createGuestbook(userId.value, guestbookContent.value.trim())
    guestbookEntries.value.unshift(res.data)
    guestbookContent.value = ''
  } catch { /* ignore */ } finally {
    submittingGuestbook.value = false
  }
}

async function replyGuestbook(entryId, replyText) {
  if (!replyText.trim()) return
  try {
    const res = await profileApi.replyGuestbook(entryId, replyText.trim())
    const entry = guestbookEntries.value.find(e => e.id === entryId)
    if (entry) entry.reply = res.data.reply
  } catch { /* ignore */ }
}

async function deleteGuestbook(entryId) {
  if (!confirm('确认删除这条留言？')) return
  try {
    await profileApi.deleteGuestbook(entryId)
    guestbookEntries.value = guestbookEntries.value.filter(e => e.id !== entryId)
  } catch { /* ignore */ }
}

function goToPlugin(plugin) {
  if (authStore.isAuthenticated) {
    router.push(plugin.route)
  } else {
    router.push(`/login?next=${plugin.route}`)
  }
}

function onFriendStatusChanged(status) {
  if (profile.value) profile.value.friend_status = status
}

function goToChat() {
  router.push('/chat')
}
</script>

<template>
  <div v-if="loading" class="max-w-4xl mx-auto px-4 py-8 text-center text-text-secondary">
    加载中...
  </div>

  <div v-else-if="profile" class="max-w-4xl mx-auto px-4 pb-8">
    <div class="relative w-full rounded-b-2xl overflow-hidden" style="aspect-ratio: 3/1">
      <img
        v-if="profile.cover_url"
        :src="profile.cover_url"
        class="w-full h-full object-cover"
      />
      <div v-else class="w-full h-full bg-gradient-to-r from-maple-600 to-maple-400" />
    </div>

    <div class="relative px-4 -mt-12 z-10">
      <div class="flex items-end gap-4">
        <div class="rounded-full border-4 border-white flex-shrink-0 shadow-md overflow-hidden">
          <AvatarImage :user="profile" size="2xl" />
        </div>
        <div class="flex-1 min-w-0 pb-1">
          <h1 class="text-lg font-bold text-text-primary truncate">{{ profile.nickname || profile.username }}</h1>
          <p v-if="profile.bio" class="text-[13px] text-text-secondary mt-0.5 truncate">{{ profile.bio }}</p>
          <p v-if="profile.show_real_name && profile.real_name" class="text-[13px] text-text-secondary mt-0.5">真实姓名: {{ profile.real_name }}</p>
        </div>
      </div>

      <div class="flex items-center gap-4 mt-3">
        <span class="text-sm text-text-secondary">👤 {{ profile.visitor_count || 0 }} 次访问</span>
        <FriendButton
          v-if="!isGuest"
          :userId="userId"
          :friendStatus="profile.friend_status || 'none'"
          @status-changed="onFriendStatusChanged"
        />
      </div>
    </div>

    <div class="px-4 mt-6">
      <div class="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
        <button
          v-for="plugin in pluginCards"
          :key="plugin.route"
          @click="goToPlugin(plugin)"
          class="flex items-center gap-2 px-4 py-2.5 bg-white rounded-xl border border-border shadow-sm hover:border-maple-300 hover:shadow-md transition-all flex-shrink-0 cursor-pointer"
        >
          <span class="text-lg">{{ plugin.icon }}</span>
          <div class="text-left">
            <div class="text-sm font-medium text-text-primary">{{ plugin.name }}</div>
            <div class="text-[11px] text-text-secondary">{{ plugin.desc }}</div>
          </div>
          <span class="text-text-secondary ml-2">›</span>
        </button>
      </div>
    </div>

    <div class="px-4 mt-6">
      <TabBar :tabs="tabs" :activeKey="activeTab" @update:activeKey="onTabChange" />

      <div v-if="activeTab === 'posts'" class="mt-4 space-y-4">
        <div v-if="postsLoading" class="text-center text-text-secondary py-8">加载中...</div>
        <template v-else-if="posts.length">
          <PostCard v-for="post in posts" :key="post.id" :post="post" :showActions="false" />
        </template>
        <div v-else class="text-center text-text-secondary py-8">暂无动态</div>
      </div>

      <div v-if="activeTab === 'visitors'" class="mt-4 space-y-3">
        <div v-if="!visitors.length" class="text-center text-text-secondary py-8">暂无访客记录</div>
        <div
          v-for="visitor in visitors"
          :key="visitor.id || visitor.user_id"
          class="flex items-center gap-3 py-2"
        >
          <AvatarImage
            :user="visitor"
            size="md"
            clickable
            @click="router.push(`/profile/${visitor.user_id}`)"
          />
          <div class="flex-1 min-w-0">
            <span class="text-sm font-medium text-text-primary truncate cursor-pointer hover:text-maple-600" @click="router.push(`/profile/${visitor.user_id}`)">
              {{ visitor.nickname || visitor.username }}
            </span>
          </div>
          <span class="text-xs text-text-secondary flex-shrink-0">{{ relativeTime(visitor.visited_at) }}</span>
        </div>
      </div>

      <div v-if="activeTab === 'guestbook'" class="mt-4 space-y-4">
        <div v-if="!isOwner && !isGuest" class="flex gap-2">
          <input
            v-model="guestbookContent"
            type="text"
            placeholder="写点什么..."
            class="flex-1 px-4 py-2.5 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600"
            @keyup.enter="submitGuestbook"
          />
          <button
            @click="submitGuestbook"
            :disabled="submittingGuestbook || !guestbookContent.trim()"
            class="px-5 py-2.5 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors disabled:opacity-50 cursor-pointer flex-shrink-0"
          >
            发送
          </button>
        </div>
        <div v-if="isGuest" class="text-center py-4">
          <RouterLink :to="`/login?next=/profile/${route.params.userId}`" class="text-maple-600 hover:underline text-sm">登录后留言</RouterLink>
        </div>

        <div v-if="!guestbookEntries.length" class="text-center text-text-secondary py-8">暂无留言</div>
        <div v-for="entry in guestbookEntries" :key="entry.id" class="flex gap-3 py-3 border-b border-border last:border-0">
          <AvatarImage :user="entry.user" size="sm" />
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium text-text-primary">{{ entry.user?.nickname }}</span>
              <span class="text-xs text-text-secondary">{{ relativeTime(entry.created_at) }}</span>
            </div>
            <p class="text-sm text-text-primary mt-1 whitespace-pre-wrap break-words">{{ entry.content }}</p>
            <div v-if="entry.reply" class="mt-2 pl-3 border-l-2 border-maple-400">
              <span class="text-xs font-medium text-maple-600">主人回复: </span>
              <span class="text-sm text-text-primary">{{ entry.reply }}</span>
            </div>
            <div v-if="isOwner && !entry.reply" class="mt-2">
              <input
                type="text"
                placeholder="回复..."
                class="px-3 py-1.5 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600 w-48"
                @keyup.enter="replyGuestbook(entry.id, $event.target.value); $event.target.value = ''"
              />
            </div>
            <button
              v-if="isOwner"
              @click="deleteGuestbook(entry.id)"
              class="mt-1 text-xs text-red-400 hover:text-red-500 transition-colors cursor-pointer"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="max-w-4xl mx-auto px-4 py-8 text-center text-text-secondary">
    用户不存在
  </div>
</template>
