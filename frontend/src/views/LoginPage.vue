<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const authStore = useAuthStore()
const toast = useToast()
const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!username.value || !password.value) {
    error.value = '请填写用户名和密码'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await authStore.login(username.value, password.value)
    const redirect = route.query.next || '/'
    router.push(redirect)
  } catch (e) {
    error.value = e.response?.data?.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-8">
      <h1 class="text-2xl font-bold text-maple-600 text-center mb-2">FallingMapleHaven</h1>
      <p class="text-text-secondary text-center text-sm mb-8">登录你的账号</p>
      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-text-primary mb-1.5">用户名</label>
          <input
            v-model="username"
            type="text"
            placeholder="请输入用户名"
            class="w-full px-4 py-2.5 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-text-primary mb-1.5">密码</label>
          <div class="relative">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="请输入密码"
              class="w-full px-4 py-2.5 pr-10 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary hover:text-maple-600 transition-colors cursor-pointer text-sm select-none"
              :aria-label="showPassword ? '隐藏密码' : '显示密码'"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2.5 bg-maple-600 text-white rounded-lg text-sm font-medium hover:bg-maple-700 disabled:opacity-60 disabled:cursor-not-allowed transition-colors"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      <p class="text-center text-sm text-text-secondary mt-6">
        没有账号？
        <RouterLink :to="`/register${route.query.next ? '?next=' + encodeURIComponent(route.query.next) : ''}`" class="text-maple-600 hover:underline">去注册</RouterLink>
      </p>
    </div>
  </div>
</template>
