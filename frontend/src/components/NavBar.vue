<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Icon from '@/components/Icon.vue'

const authStore = useAuthStore()
const router = useRouter()
const showDropdown = ref(false)
const dropdownRef = ref(null)
const triggerRef = ref(null)

function onDocumentClick(e) {
  if (!showDropdown.value) return
  const target = e.target
  if (triggerRef.value?.contains(target)) return
  if (dropdownRef.value && !dropdownRef.value.contains(target)) {
    showDropdown.value = false
  }
}

function onKeydown(e) {
  if (e.key === 'Escape' && showDropdown.value) {
    showDropdown.value = false
    triggerRef.value?.focus()
  }
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
  document.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
})

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
  <nav class="hidden md:flex bg-maple-600 text-white px-6 py-3 items-center justify-between shadow-float">
    <div class="flex items-center gap-8">
      <RouterLink to="/" class="flex items-center justify-center w-9 h-9 bg-white/20 rounded-lg text-lg font-bold tracking-wide hover:bg-white/30 transition-colors">枫</RouterLink>
      <div v-if="authStore.isAuthenticated" class="flex gap-6 text-sm font-medium">
        <RouterLink to="/" class="flex items-center gap-1.5 hover:text-maple-200 transition-colors">
          <Icon name="home" :size="16" /> 首页
        </RouterLink>
        <RouterLink to="/groups" class="flex items-center gap-1.5 hover:text-maple-200 transition-colors">
          <Icon name="users" :size="16" /> 群组
        </RouterLink>
        <RouterLink to="/friends" class="flex items-center gap-1.5 hover:text-maple-200 transition-colors">
          <Icon name="userPlus" :size="16" /> 好友
        </RouterLink>
        <RouterLink to="/chat" class="flex items-center gap-1.5 hover:text-maple-200 transition-colors">
          <Icon name="messageCircle" :size="16" /> 聊天
        </RouterLink>
        <RouterLink to="/notifications" class="flex items-center gap-1.5 hover:text-maple-200 transition-colors relative">
          <Icon name="bell" :size="16" /> 通知
          <span v-if="authStore.user?.unread_count" class="absolute -top-1.5 -right-4 bg-red-500 text-white text-xs rounded-full min-w-[18px] h-[18px] flex items-center justify-center px-1">
            {{ authStore.user.unread_count > 99 ? '99+' : authStore.user.unread_count }}
          </span>
        </RouterLink>
        <RouterLink v-if="authStore.isAdmin" to="/admin" class="flex items-center gap-1.5 hover:text-maple-200 transition-colors">
          <Icon name="shield" :size="16" /> 管理
        </RouterLink>
      </div>
      <div v-else class="flex gap-6 text-sm font-medium">
        <RouterLink to="/" class="flex items-center gap-1.5 hover:text-maple-200 transition-colors">
          <Icon name="globe" :size="16" /> 广场
        </RouterLink>
        <RouterLink to="/groups" class="flex items-center gap-1.5 hover:text-maple-200 transition-colors">
          <Icon name="users" :size="16" /> 群组
        </RouterLink>
      </div>
    </div>
    <div v-if="authStore.isAuthenticated" class="relative">
      <button
        ref="triggerRef"
        @click="toggleDropdown"
        class="flex items-center gap-2 hover:text-maple-200 transition-all duration-150 active:scale-[0.97] cursor-pointer min-h-[44px]"
        aria-haspopup="true"
        :aria-expanded="showDropdown"
      >
        <div class="w-8 h-8 rounded-full bg-maple-400 overflow-hidden flex items-center justify-center text-sm font-bold flex-shrink-0">
          <img v-if="authStore.user?.avatar_url" :src="authStore.user.avatar_url" class="w-full h-full object-cover" />
          <span v-else>{{ authStore.user?.username?.[0]?.toUpperCase() || 'U' }}</span>
        </div>
        <span class="text-sm max-w-[120px] truncate">{{ authStore.user?.nickname || authStore.user?.username }}</span>
        <Icon name="chevronDown" :size="14" class="transition-transform duration-150" :class="showDropdown ? 'rotate-180' : ''" />
      </button>
      <Transition name="fade-scale">
        <div
          v-if="showDropdown"
          ref="dropdownRef"
          role="menu"
          class="absolute right-0 top-full mt-3 w-48 bg-white rounded-xl shadow-modal border border-border overflow-hidden z-20"
        >
          <div class="absolute -top-1.5 right-6 w-3 h-3 bg-white border-l border-t border-border rotate-45" />
          <RouterLink
            :to="`/profile/${authStore.user?.user_id}`"
            role="menuitem"
            @click="closeDropdown"
            class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-text-primary hover:bg-maple-50 hover:text-maple-700 transition-colors"
          >
            <Icon name="user" :size="16" class="text-text-secondary" /> 我的主页
          </RouterLink>
          <RouterLink
            to="/settings"
            role="menuitem"
            @click="closeDropdown"
            class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-text-primary hover:bg-maple-50 hover:text-maple-700 transition-colors"
          >
            <Icon name="settings" :size="16" class="text-text-secondary" /> 个人设置
          </RouterLink>
          <hr class="border-border" />
          <button
            @click="handleLogout"
            role="menuitem"
            class="flex items-center gap-2.5 w-full text-left px-4 py-2.5 text-sm text-red-500 hover:bg-red-50 transition-colors cursor-pointer"
          >
            <Icon name="logOut" :size="16" /> 退出登录
          </button>
        </div>
      </Transition>
    </div>
    <div v-else class="flex items-center gap-3">
      <RouterLink to="/login" class="flex items-center gap-1.5 text-sm hover:text-maple-200 transition-colors px-3 py-1.5 min-h-[44px]">登录</RouterLink>
      <RouterLink to="/register" class="flex items-center gap-1.5 text-sm bg-white text-maple-600 px-4 py-1.5 rounded-lg font-medium hover:bg-maple-50 transition-colors min-h-[44px]">注册</RouterLink>
    </div>
  </nav>
</template>

<style scoped>
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.15s ease-out;
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-4px);
}
</style>
