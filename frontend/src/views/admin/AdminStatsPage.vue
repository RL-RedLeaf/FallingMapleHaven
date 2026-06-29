<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const stats = ref([
  { label: '总用户数', value: '--', icon: '👥', color: 'bg-blue-50 text-blue-600' },
  { label: '日活跃用户', value: '--', icon: '📊', color: 'bg-green-50 text-green-600' },
  { label: '动态总数', value: '--', icon: '📝', color: 'bg-purple-50 text-purple-600' },
  { label: '评论总数', value: '--', icon: '💬', color: 'bg-orange-50 text-orange-600' },
  { label: '消息总数', value: '--', icon: '✉️', color: 'bg-maple-50 text-maple-600' },
])
const error = ref('')

onMounted(async () => {
  try {
    const res = await adminApi.stats()
    const data = res.data || {}
    stats.value = [
      { label: '总用户数', value: data.total_users ?? 0, icon: '👥', color: 'bg-blue-50 text-blue-600' },
      { label: '日活跃用户', value: data.active_users_today ?? 0, icon: '📊', color: 'bg-green-50 text-green-600' },
      { label: '动态总数', value: data.total_posts ?? 0, icon: '📝', color: 'bg-purple-50 text-purple-600' },
      { label: '评论总数', value: data.total_comments ?? 0, icon: '💬', color: 'bg-orange-50 text-orange-600' },
      { label: '消息总数', value: data.total_messages ?? 0, icon: '✉️', color: 'bg-maple-50 text-maple-600' },
    ]
  } catch {
    error.value = '统计数据加载失败'
  }
})
</script>

<template>
  <div>
    <h2 class="text-xl font-bold text-text-primary mb-6">数据统计</h2>
    <p v-if="error" class="mb-4 text-sm text-red-500">{{ error }}</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="bg-white rounded-xl border border-border p-5 flex items-center gap-4"
      >
        <div class="w-12 h-12 rounded-lg flex items-center justify-center text-xl" :class="stat.color">
          {{ stat.icon }}
        </div>
        <div>
          <p class="text-2xl font-bold text-text-primary">{{ stat.value }}</p>
          <p class="text-sm text-text-secondary">{{ stat.label }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
