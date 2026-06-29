<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const showDropdown = ref(false)

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

function closeDropdown() {
  showDropdown.value = false
}

async function handleLogout() {
  closeDropdown()
  await authStore.logout()
  router.push('/')
}
</script>

<template>
  <nav class="hidden md:flex bg-maple-600 text-white px-6 py-3 items-center justify-between shadow-md">
    <div class="flex items-center gap-8">
      <RouterLink to="/" class="flex items-center justify-center w-9 h-9 bg-white/20 rounded-lg text-lg font-bold tracking-wide">枫</RouterLink>
      <div v-if="authStore.isAuthenticated" class="flex gap-6 text-sm font-medium">
        <RouterLink to="/" class="hover:text-maple-200 transition-colors">首页</RouterLink>
        <RouterLink to="/groups" class="hover:text-maple-200 transition-colors">群组</RouterLink>
        <RouterLink to="/friends" class="hover:text-maple-200 transition-colors">好友</RouterLink>
        <RouterLink to="/chat" class="hover:text-maple-200 transition-colors">聊天</RouterLink>
        <RouterLink to="/notifications" class="hover:text-maple-200 transition-colors relative">
          通知
          <span v-if="authStore.user?.unread_count" class="absolute -top-1 -right-4 bg-red-500 text-white text-xs rounded-full min-w-[18px] h-[18px] flex items-center justify-center px-1">
            {{ authStore.user.unread_count > 99 ? '99+' : authStore.user.unread_count }}
          </span>
        </RouterLink>
        <RouterLink v-if="authStore.isAdmin" to="/admin" class="hover:text-maple-200 transition-colors">管理后台</RouterLink>
      </div>
      <div v-else class="flex gap-6 text-sm font-medium">
        <RouterLink to="/" class="hover:text-maple-200 transition-colors">广场</RouterLink>
        <RouterLink to="/groups" class="hover:text-maple-200 transition-colors">群组</RouterLink>
      </div>
    </div>
    <div v-if="authStore.isAuthenticated" class="relative">
      <button @click="toggleDropdown" class="flex items-center gap-2 hover:text-maple-200 transition-colors cursor-pointer">
        <div class="w-8 h-8 rounded-full bg-maple-400 overflow-hidden flex items-center justify-center text-sm font-bold flex-shrink-0">
          <img v-if="authStore.user?.avatar_url" :src="authStore.user.avatar_url" class="w-full h-full object-cover" />
          <span v-else>{{ authStore.user?.username?.[0]?.toUpperCase() || 'U' }}</span>
        </div>
        <span class="text-sm max-w-[120px] truncate">{{ authStore.user?.nickname || authStore.user?.username }}</span>
      </button>
      <div v-if="showDropdown" @click="closeDropdown" class="fixed inset-0 z-10" />
      <div v-if="showDropdown" class="absolute right-0 top-full mt-2 w-48 bg-white rounded-xl shadow-lg border border-border overflow-hidden z-20">
        <RouterLink
          :to="`/profile/${authStore.user?.user_id}`"
          @click="closeDropdown"
          class="block px-4 py-2.5 text-sm text-text-primary hover:bg-maple-50 transition-colors"
        >
          我的主页
        </RouterLink>
        <RouterLink
          to="/settings"
          @click="closeDropdown"
          class="block px-4 py-2.5 text-sm text-text-primary hover:bg-maple-50 transition-colors"
        >
          个人设置
        </RouterLink>
        <hr class="border-border" />
        <button
          @click="handleLogout"
          class="w-full text-left px-4 py-2.5 text-sm text-red-500 hover:bg-red-50 transition-colors"
        >
          退出登录
        </button>
      </div>
    </div>
    <div v-else class="flex items-center gap-3">
      <RouterLink to="/login" class="text-sm hover:text-maple-200 transition-colors px-3 py-1.5">登录</RouterLink>
      <RouterLink to="/register" class="text-sm bg-white text-maple-600 px-4 py-1.5 rounded-lg font-medium hover:bg-maple-50 transition-colors">注册</RouterLink>
    </div>
  </nav>
</template>
