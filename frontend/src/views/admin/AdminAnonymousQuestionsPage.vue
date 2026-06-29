<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const questions = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await adminApi.anonymousQuestions()
    questions.value = res.data || []
  } catch { /* ignore */ } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h2 class="text-xl font-bold mb-4">匿名提问追溯</h2>
    <div v-if="loading" class="text-center text-text-secondary py-8">加载中...</div>
    <div v-else-if="!questions.length" class="text-center text-text-secondary py-8">暂无数据</div>
    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-border">
            <th class="text-left py-2 px-3">ID</th>
            <th class="text-left py-2 px-3">提问者</th>
            <th class="text-left py-2 px-3">接收者</th>
            <th class="text-left py-2 px-3">内容</th>
            <th class="text-left py-2 px-3">回答</th>
            <th class="text-left py-2 px-3">状态</th>
            <th class="text-left py-2 px-3">时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="q in questions" :key="q.id" class="border-b border-border hover:bg-gray-50">
            <td class="py-2 px-3">{{ q.id }}</td>
            <td class="py-2 px-3">
              <span class="text-maple-600 font-medium">{{ q.real_sender?.nickname || '未知' }}</span>
              <span class="text-text-secondary text-xs ml-1">(#{{ q.real_sender?.user_id }})</span>
            </td>
            <td class="py-2 px-3">{{ q.recipient_nickname || q.recipient }}</td>
            <td class="py-2 px-3 max-w-xs truncate">{{ q.content }}</td>
            <td class="py-2 px-3 max-w-xs truncate">{{ q.answer || '-' }}</td>
            <td class="py-2 px-3">
              <span :class="q.is_answered ? 'text-green-600' : 'text-yellow-600'">
                {{ q.is_answered ? '已回答' : '未回答' }}
              </span>
            </td>
            <td class="py-2 px-3 text-text-secondary">{{ new Date(q.created_at).toLocaleDateString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
