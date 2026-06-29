<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const logs = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await adminApi.logs()
    logs.value = res.data || []
  } catch {
    error.value = '操作日志加载失败'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h2 class="text-xl font-bold text-text-primary mb-6">操作日志</h2>
    <p v-if="error" class="mb-4 text-sm text-red-500">{{ error }}</p>
    <div class="bg-white rounded-xl border border-border overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 text-text-secondary">
            <th class="text-left px-4 py-3 font-medium">时间</th>
            <th class="text-left px-4 py-3 font-medium">操作人</th>
            <th class="text-left px-4 py-3 font-medium">操作内容</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="3" class="text-center py-8 text-text-secondary">加载中...</td></tr>
          <tr v-else-if="!logs.length"><td colspan="3" class="text-center py-8 text-text-secondary">暂无日志</td></tr>
          <tr v-for="log in logs" :key="log.id" class="border-t border-border hover:bg-gray-50">
            <td class="px-4 py-3 text-text-secondary whitespace-nowrap">{{ log.created_at ? new Date(log.created_at).toLocaleString() : '-' }}</td>
            <td class="px-4 py-3">{{ log.admin_nickname || '-' }}</td>
            <td class="px-4 py-3">{{ log.action }} {{ log.detail ? JSON.stringify(log.detail) : '' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
