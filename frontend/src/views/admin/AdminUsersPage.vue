<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const users = ref([])
const loading = ref(true)
const error = ref('')

async function fetchUsers() {
  loading.value = true
  error.value = ''
  try {
    const res = await adminApi.users()
    users.value = res.data || []
  } catch {
    error.value = '用户列表加载失败'
  } finally {
    loading.value = false
  }
}

async function toggleUserActive(user) {
  const nextActive = !user.is_active
  try {
    const res = await adminApi.updateUser(user.id, { is_active: nextActive })
    Object.assign(user, res.data)
  } catch {
    error.value = '用户状态更新失败'
  }
}

onMounted(fetchUsers)
</script>

<template>
  <div>
    <h2 class="text-xl font-bold text-text-primary mb-6">用户管理</h2>
    <p v-if="error" class="mb-4 text-sm text-red-500">{{ error }}</p>
    <div class="bg-white rounded-xl border border-border overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 text-text-secondary">
            <th class="text-left px-4 py-3 font-medium">ID</th>
            <th class="text-left px-4 py-3 font-medium">用户名</th>
            <th class="text-left px-4 py-3 font-medium">昵称</th>
            <th class="text-left px-4 py-3 font-medium">状态</th>
            <th class="text-right px-4 py-3 font-medium">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="5" class="text-center py-8 text-text-secondary">加载中...</td></tr>
          <tr v-else-if="!users.length"><td colspan="5" class="text-center py-8 text-text-secondary">暂无数据</td></tr>
          <tr v-for="user in users" :key="user.id" class="border-t border-border hover:bg-gray-50">
            <td class="px-4 py-3">{{ user.id }}</td>
            <td class="px-4 py-3">{{ user.username }}</td>
            <td class="px-4 py-3">{{ user.nickname || '-' }}</td>
            <td class="px-4 py-3">
              <span class="px-2 py-0.5 rounded-full text-xs" :class="user.is_active ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-500'">
                {{ user.is_active ? '正常' : '禁用' }}
              </span>
            </td>
            <td class="px-4 py-3 text-right">
              <button
                @click="toggleUserActive(user)"
                class="text-xs text-maple-600 hover:text-maple-700 cursor-pointer"
              >
                {{ user.is_active ? '禁用' : '启用' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
