<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { notificationApi } from '@/api/notifications'
import { relativeTime } from '@/utils/time'
import Icon from '@/components/Icon.vue'

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
  const icons = { like: 'heart', comment: 'messageCircle', friend_request: 'userPlus', system: 'bell' }
  return icons[type] || 'bell'
}
</script>

<template>
  <div class="page-container">
    <div class="flex items-center justify-between mb-6">
      <h1 class="page-title !mb-0">通知</h1>
      <button
        v-if="notifications.length"
        @click="markAllRead"
        class="btn-ghost px-3 py-1.5 flex items-center gap-1.5"
      >
        <Icon name="check" :size="14" /> 全部已读
      </button>
    </div>

    <Transition name="fade" mode="out-in">
      <div v-if="loading" key="loading" class="space-y-3">
        <div v-for="i in 5" :key="i" class="card-base p-4 flex items-start gap-3">
          <div class="w-10 h-10 rounded-full skeleton flex-shrink-0" />
          <div class="flex-1 space-y-2">
            <div class="h-3 w-3/4 skeleton" />
            <div class="h-2.5 w-1/2 skeleton" />
          </div>
        </div>
      </div>

      <div v-else-if="!notifications.length" key="empty" class="text-center py-16 animate-fade-in">
        <Icon name="bell" :size="48" class="text-maple-300 mx-auto mb-3" />
        <p class="text-text-secondary">暂无通知</p>
      </div>

      <div v-else key="list" class="space-y-2">
        <div
          v-for="n in notifications"
          :key="n.id"
          @click="markRead(n)"
          class="rounded-2xl border p-4 flex items-start gap-3 transition-all duration-150 cursor-pointer"
          :class="n.is_read
            ? 'bg-maple-50/50 border-maple-100/50 hover:bg-maple-50'
            : 'bg-white border-border shadow-card hover:shadow-float'"
        >
          <div class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0" :class="n.is_read ? 'bg-maple-100/50' : 'bg-maple-100'">
            <Icon :name="notificationIcon(n.type)" :size="18" :class="n.is_read ? 'text-maple-400' : 'text-maple-600'" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm" :class="n.is_read ? 'text-text-secondary' : 'text-text-primary font-medium'">{{ n.title }}</p>
            <p v-if="n.content" class="text-xs text-text-secondary mt-1">{{ n.content }}</p>
            <span class="text-xs text-text-secondary mt-1 block">{{ relativeTime(n.created_at) }}</span>
          </div>
          <div v-if="!n.is_read" class="w-2 h-2 rounded-full bg-maple-600 flex-shrink-0 mt-1.5" />
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
