<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

const route = useRoute()
const mobileNavOpen = ref(false)

const navItems = [
  { path: '/admin', name: '数据统计', icon: '📊', exact: true },
  { path: '/admin/users', name: '用户管理', icon: '👥' },
  { path: '/admin/posts', name: '内容管理', icon: '📝' },
  { path: '/admin/anonymous-questions', name: '匿名追溯', icon: '🕵️' },
  { path: '/admin/plugins', name: '插件管理', icon: '🔧' },
  { path: '/admin/settings', name: '站点设置', icon: '⚙️' },
  { path: '/admin/logs', name: '操作日志', icon: '📋' },
]

function isActive(path, exact = false) {
  if (exact) return route.path === path
  return route.path.startsWith(path)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-gray-900 text-white px-4 md:px-6 py-3 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button @click="mobileNavOpen = !mobileNavOpen" class="md:hidden text-white cursor-pointer">☰</button>
        <h1 class="text-lg font-bold">管理后台</h1>
      </div>
      <RouterLink to="/" class="text-sm text-gray-300 hover:text-white transition-colors">← 返回前台</RouterLink>
    </header>

    <div class="flex">
      <aside class="hidden md:flex flex-col w-56 bg-white border-r border-border min-h-[calc(100vh-52px)] p-4 gap-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors"
          :class="isActive(item.path, item.exact) ? 'bg-maple-50 text-maple-700 font-medium' : 'text-text-secondary hover:bg-gray-50 hover:text-text-primary'"
        >
          <span>{{ item.icon }}</span>
          <span>{{ item.name }}</span>
        </RouterLink>
      </aside>

      <div v-if="mobileNavOpen" class="md:hidden fixed inset-0 z-40 flex">
        <div @click="mobileNavOpen = false" class="flex-1 bg-black/30" />
        <div class="w-56 bg-white h-full p-4 shadow-lg">
          <div class="flex flex-col gap-1">
            <RouterLink
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              @click="mobileNavOpen = false"
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors"
              :class="isActive(item.path, item.exact) ? 'bg-maple-50 text-maple-700 font-medium' : 'text-text-secondary hover:bg-gray-50 hover:text-text-primary'"
            >
              <span>{{ item.icon }}</span>
              <span>{{ item.name }}</span>
            </RouterLink>
          </div>
        </div>
      </div>

      <main class="flex-1 p-4 md:p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>
