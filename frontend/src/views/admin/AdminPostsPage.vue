<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import TabBar from '@/components/TabBar.vue'

const posts = ref([])
const comments = ref([])
const loading = ref(true)
const activeTab = ref('posts')
const error = ref('')

async function fetchContent() {
  loading.value = true
  error.value = ''
  try {
    const [postRes, commentRes] = await Promise.all([
      adminApi.posts(),
      adminApi.comments(),
    ])
    posts.value = postRes.data || []
    comments.value = commentRes.data || []
  } catch {
    error.value = '内容数据加载失败'
  } finally {
    loading.value = false
  }
}

async function deletePost(post) {
  if (!confirm('确认删除这条动态？')) return
  try {
    await adminApi.deletePost(post.id)
    posts.value = posts.value.filter(item => item.id !== post.id)
  } catch {
    error.value = '动态删除失败'
  }
}

async function deleteComment(comment) {
  if (!confirm('确认删除这条评论？')) return
  try {
    await adminApi.deleteComment(comment.id)
    comments.value = comments.value.filter(item => item.id !== comment.id)
  } catch {
    error.value = '评论删除失败'
  }
}

onMounted(fetchContent)
</script>

<template>
  <div>
    <h2 class="text-xl font-bold text-text-primary mb-6">内容管理</h2>
    <p v-if="error" class="mb-4 text-sm text-red-500">{{ error }}</p>
    <TabBar
      :tabs="[{ key: 'posts', label: '动态' }, { key: 'comments', label: '评论' }]"
      :activeKey="activeTab"
      @update:activeKey="activeTab = $event"
      class="mb-4"
    />
    <div class="bg-white rounded-xl border border-border overflow-hidden">
      <table v-if="activeTab === 'posts'" class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 text-text-secondary">
            <th class="text-left px-4 py-3 font-medium">ID</th>
            <th class="text-left px-4 py-3 font-medium">内容</th>
            <th class="text-left px-4 py-3 font-medium">作者</th>
            <th class="text-left px-4 py-3 font-medium">时间</th>
            <th class="text-right px-4 py-3 font-medium">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="5" class="text-center py-8 text-text-secondary">加载中...</td></tr>
          <tr v-else-if="!posts.length"><td colspan="5" class="text-center py-8 text-text-secondary">暂无数据</td></tr>
          <tr v-for="post in posts" :key="post.id" class="border-t border-border hover:bg-gray-50">
            <td class="px-4 py-3">{{ post.id }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ post.content || '(无内容)' }}</td>
            <td class="px-4 py-3">{{ post.author_nickname || '-' }}</td>
            <td class="px-4 py-3 text-text-secondary">{{ post.created_at ? new Date(post.created_at).toLocaleString() : '-' }}</td>
            <td class="px-4 py-3 text-right">
              <button @click="deletePost(post)" class="text-xs text-red-500 hover:text-red-600 cursor-pointer">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <table v-else class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 text-text-secondary">
            <th class="text-left px-4 py-3 font-medium">ID</th>
            <th class="text-left px-4 py-3 font-medium">评论</th>
            <th class="text-left px-4 py-3 font-medium">动态</th>
            <th class="text-left px-4 py-3 font-medium">作者</th>
            <th class="text-left px-4 py-3 font-medium">时间</th>
            <th class="text-right px-4 py-3 font-medium">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="6" class="text-center py-8 text-text-secondary">加载中...</td></tr>
          <tr v-else-if="!comments.length"><td colspan="6" class="text-center py-8 text-text-secondary">暂无评论</td></tr>
          <tr v-for="comment in comments" :key="comment.id" class="border-t border-border hover:bg-gray-50">
            <td class="px-4 py-3">{{ comment.id }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ comment.content }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ comment.post_content || '-' }}</td>
            <td class="px-4 py-3">{{ comment.author_nickname || '-' }}</td>
            <td class="px-4 py-3 text-text-secondary">{{ comment.created_at ? new Date(comment.created_at).toLocaleString() : '-' }}</td>
            <td class="px-4 py-3 text-right">
              <button @click="deleteComment(comment)" class="text-xs text-red-500 hover:text-red-600 cursor-pointer">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
