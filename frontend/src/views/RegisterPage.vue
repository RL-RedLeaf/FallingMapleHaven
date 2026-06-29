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
const nickname = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirm = ref(false)
const email = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  if (!username.value || !nickname.value || !password.value || !confirmPassword.value) {
    error.value = '请填写必填字段'
    return
  }
  if (password.value.length < 8) {
    error.value = '密码长度不能少于8位'
    return
  }
  if (!/[A-Za-z]/.test(password.value)) {
    error.value = '密码必须包含字母'
    return
  }
  if (!/\d/.test(password.value)) {
    error.value = '密码必须包含数字'
    return
  }
  if (!/[!@#$%^&*()_+\-=[\]{}|;':",./<>?`~]/.test(password.value)) {
    error.value = '密码必须包含至少一个特殊字符'
    return
  }
  if (password.value !== confirmPassword.value) {
    error.value = '两次密码输入不一致'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await authStore.register({
      username: username.value,
      nickname: nickname.value,
      password: password.value,
      email: email.value || undefined,
    })
    toast.success('注册成功，欢迎加入！')
    const redirect = route.query.next || (authStore.user?.user_id ? `/profile/${authStore.user.user_id}` : '/')
    router.push(redirect)
  } catch (e) {
    error.value = e.response?.data?.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-8">
      <h1 class="text-2xl font-bold text-maple-600 text-center mb-2">FallingMapleHaven</h1>
      <p class="text-text-secondary text-center text-sm mb-8">创建你的账号</p>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-text-primary mb-1.5">用户名 <span class="text-red-500">*</span></label>
          <input v-model="username" type="text" placeholder="请输入用户名" class="w-full px-4 py-2.5 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600" />
        </div>
        <div>
          <label class="block text-sm font-medium text-text-primary mb-1.5">昵称 <span class="text-red-500">*</span></label>
          <input v-model="nickname" type="text" placeholder="请输入昵称" class="w-full px-4 py-2.5 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600" />
        </div>
        <div>
          <label class="block text-sm font-medium text-text-primary mb-1.5">密码 <span class="text-red-500">*</span></label>
          <div class="relative">
            <input v-model="password" :type="showPassword ? 'text' : 'password'" placeholder="至少8位，需包含字母、数字和特殊字符" class="w-full px-4 py-2.5 pr-10 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600" />
            <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary hover:text-maple-600 transition-colors cursor-pointer text-sm select-none" :aria-label="showPassword ? '隐藏密码' : '显示密码'">{{ showPassword ? '🙈' : '👁️' }}</button>
          </div>
          <p class="text-xs text-text-secondary mt-1">密码需至少8位，包含字母、数字和至少一个特殊字符</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-text-primary mb-1.5">确认密码 <span class="text-red-500">*</span></label>
          <div class="relative">
            <input v-model="confirmPassword" :type="showConfirm ? 'text' : 'password'" placeholder="再次输入密码" class="w-full px-4 py-2.5 pr-10 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600" />
            <button type="button" @click="showConfirm = !showConfirm" class="absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary hover:text-maple-600 transition-colors cursor-pointer text-sm select-none" :aria-label="showConfirm ? '隐藏密码' : '显示密码'">{{ showConfirm ? '🙈' : '👁️' }}</button>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-text-primary mb-1.5">邮箱 <span class="text-text-secondary">(可选)</span></label>
          <input v-model="email" type="email" placeholder="example@mail.com" class="w-full px-4 py-2.5 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600" />
        </div>
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        <button type="submit" :disabled="loading" class="w-full py-2.5 bg-maple-600 text-white rounded-lg text-sm font-medium hover:bg-maple-700 disabled:opacity-60 disabled:cursor-not-allowed transition-colors">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="text-center text-sm text-text-secondary mt-6">
        已有账号？
        <RouterLink :to="`/login${route.query.next ? '?next=' + encodeURIComponent(route.query.next) : ''}`" class="text-maple-600 hover:underline">去登录</RouterLink>
      </p>
    </div>
  </div>
</template>
