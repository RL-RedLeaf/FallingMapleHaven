<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { notificationApi } from '@/api/notifications'
import { relativeTime } from '@/utils/time'
import AvatarImage from '@/components/AvatarImage.vue'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const notifications = ref([])
const loading = ref(true)
const unreadCount = ref(0)
const page = ref(1)
const hasMore = ref(true)
const pollingInterval = ref(null)

const POLL_INTERVAL = 30000

onMounted(() => {
  fetchNotifications(true)
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})

function startPolling() {
  pollingInterval.value = setInterval(() => {
    fetchUnreadCount()
  }, POLL_INTERVAL)
}

function stopPolling() {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
}

async function fetchUnreadCount() {
  try {
    const res = await notificationApi.pending()
    if (res.data) {
      unreadCount.value = res.data.count || 0
      notifications.value = res.data?.results || res.data || []
      page.value = 1
    }
  } catch { /* ignore */ }
}

async function fetchNotifications(reset = false) {
  if (loading.value) return
  loading.value = true
  try {
    if (reset) page.value = 1
    const res = await notificationApi.list({ page: page.value, page_size: 20 })
    const results = res.data?.results || res.data || []
    if (reset) {
      notifications.value = results
    } else {
      notifications.value.push(...results)
    }
    if (res.data) {
      hasMore.value = res.data.page * res.data.page_size < res.data.total
    } else {
      hasMore.value = false
    }
    if (!reset) page.value += 1
  } catch { /* ignore */ } finally {
    loading.value = false
  }
}

async function markAsRead(notif) {
  if (notif.is_read) return
  try {
    await notificationApi.markRead(notif.id)
    notif.is_read = true
    unreadCount.value = Math.max(0, unreadCount.value - 1)
  } catch { /* ignore */ }
}

async function markAllRead() {
  try {
    await notificationApi.markAllRead()
    notifications.value.forEach(n => n.is_read = true)
    unreadCount.value = 0
  } catch { /* ignore */ }
}

function handleNotificationClick(notif) {
  markAsRead(notif)
  if (notif.data?.url) {
    router.push(notif.data.url)
  }
}

function getNotificationIcon(type) {
  switch (type) {
    case 'like': return '❤️'
    case 'comment': return '💬'
    case 'follow': return '👤'
    default: return '🔔'
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="page-title mb-0">通知</h1>
      <button
        v-if="notifications.some(n => !n.is_read)"
        @click="markAllRead"
        class="text-sm text-maple-600 hover:text-maple-700 transition-colors cursor-pointer"
      >
        全部标为已读
      </button>
    </div>

    <div v-if="loading && !notifications.length" class="text-center text-text-secondary py-12">
      加载中...
    </div>

    <div v-else-if="!notifications.length" class="text-center py-16 text-text-secondary">
      暂无通知
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="notif in notifications"
        :key="notif.id"
        @click="handleNotificationClick(notif)"
        class="flex items-center gap-3 p-4 bg-white rounded-xl border border-border hover:border-maple-300 transition-colors cursor-pointer"
        :class="{ 'border-l-4 border-l-maple-500': !notif.is_read }"
      >
        <AvatarImage :user="notif.actor" size="sm" />
        <div class="flex-1 min-w-0">
          <p class="text-sm text-text-primary" :class="{ 'font-semibold': !notif.is_read }">
            <span class="font-medium">{{ notif.actor?.nickname || '用户' }}</span>
            {{ notif.verb }}
            <span v-if="notif.action_object" class="text-text-secondary">{{ notif.action_object }}</span>
          </p>
          <p v-if="notif.description" class="text-xs text-text-secondary mt-0.5 truncate">{{ notif.description }}</p>
          <p class="text-xs text-text-tertiary mt-1">{{ relativeTime(notif.created_at) }}</p>
        </div>
        <span v-if="!notif.is_read" class="w-2 h-2 rounded-full bg-maple-500 flex-shrink-0" />
      </div>

      <button
        v-if="hasMore"
        @click="fetchNotifications(false)"
        :disabled="loading"
        class="w-full text-center text-sm text-maple-600 hover:text-maple-700 py-3 cursor-pointer"
      >
        {{ loading ? '加载中...' : '加载更多' }}
      </button>
    </div>
  </div>
</template>
