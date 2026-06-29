<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const tabs = computed(() => {
  const items = [
    { name: '首页', path: '/', icon: '🏠' },
    { name: '群组', path: '/groups', icon: '👥' },
    { name: '聊天', path: '/chat', icon: '💬' },
    { name: '好友', path: '/friends', icon: '🤝' },
    { name: '通知', path: '/notifications', icon: '🔔' },
    { name: '我的', path: authStore.user?.user_id ? `/profile/${authStore.user.user_id}` : '/login', icon: '👤' },
  ]
  if (authStore.isAdmin) {
    items.push({ name: '后台', path: '/admin', icon: '⚙️' })
  }
  return items
})

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<template>
  <nav v-if="authStore.isAuthenticated" class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-maple-100 z-50">
    <div class="flex items-center justify-around py-2">
      <RouterLink
        v-for="tab in tabs"
        :key="tab.name"
        :to="tab.path"
        class="flex flex-col items-center gap-0.5 text-xs relative"
        :class="isActive(tab.path) ? 'text-maple-600' : 'text-text-secondary'"
      >
        <span class="text-lg leading-none">{{ tab.icon }}</span>
        <span>{{ tab.name }}</span>
        <span
          v-if="tab.name === '通知' && authStore.user?.unread_count"
          class="absolute -top-1 -right-2 bg-red-500 text-white text-[10px] rounded-full min-w-[16px] h-4 flex items-center justify-center px-1"
        >
          {{ authStore.user.unread_count > 99 ? '99+' : authStore.user.unread_count }}
        </span>
      </RouterLink>
    </div>
  </nav>
</template>
