<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { notificationApi } from '@/api/notifications'
import { relativeTime } from '@/utils/time'

const router = useRouter()
const authStore = useAuthStore()
const notifications = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await notificationApi.list({ page: 1, page_size: 20 })
    notifications.value = res.data?.results || []
  } catch { /* ignore */ } finally {
    loading.value = false
  }
})

async function refreshUnreadCount() {
  const res = await notificationApi.unreadCount()
  authStore.setUnreadCount(res.data?.count || 0)
}

async function markRead(notification) {
  try {
    if (!notification.is_read) {
      await notificationApi.read(notification.id)
      notification.is_read = true
      await refreshUnreadCount()
    }
    if (notification.link && notification.link !== '#') {
      router.push(notification.link)
    }
  } catch { /* ignore */ }
}

async function markAllRead() {
  try {
    await notificationApi.readAll()
    notifications.value.forEach(n => n.is_read = true)
    authStore.setUnreadCount(0)
  } catch { /* ignore */ }
}

function notificationIcon(type) {
  const icons = { like: '❤️', comment: '💬', friend_request: '👥', system: '🔔' }
  return icons[type] || '🔔'
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-maple-700">通知</h1>
      <button
        @click="markAllRead"
        class="text-sm text-maple-600 hover:text-maple-700 cursor-pointer"
      >
        全部已读
      </button>
    </div>

    <div v-if="loading" class="text-center text-text-secondary py-12">加载中...</div>

    <div v-else-if="!notifications.length" class="text-center text-text-secondary py-12">
      暂无通知
    </div>

    <div v-else class="space-y-2">
        <div
          v-for="n in notifications"
          :key="n.id"
          @click="markRead(n)"
          class="rounded-2xl shadow-sm border p-4 flex items-start gap-3 transition-colors"
          :class="n.is_read
            ? 'bg-maple-50/50 border-maple-100/50 cursor-default'
            : 'bg-white border-border cursor-pointer hover:border-maple-200 hover:shadow-md'"
        >
        <span class="text-lg mt-0.5">{{ notificationIcon(n.type) }}</span>
        <div class="flex-1 min-w-0">
          <p class="text-sm text-text-primary">{{ n.title }}</p>
          <p v-if="n.content" class="text-xs text-text-secondary mt-1">{{ n.content }}</p>
          <span class="text-xs text-text-secondary mt-1 block">{{ relativeTime(n.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
