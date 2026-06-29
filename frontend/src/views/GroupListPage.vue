<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { groupApi } from '@/api/plugin'

const router = useRouter()
const authStore = useAuthStore()
const groups = ref([])
const loading = ref(true)
const showCreateModal = ref(false)
const createForm = ref({ name: '', description: '', is_public: true })
const creating = ref(false)
const createError = ref('')

onMounted(() => {
  fetchGroups()
})

async function fetchGroups() {
  loading.value = true
  try {
    const res = await groupApi.list()
    groups.value = res.data || []
  } catch { /* ignore */ } finally {
    loading.value = false
  }
}

async function createGroup() {
  if (!createForm.value.name.trim()) return
  creating.value = true
  createError.value = ''
  try {
    await groupApi.create(createForm.value)
    showCreateModal.value = false
    createForm.value = { name: '', description: '', is_public: true }
    await fetchGroups()
  } catch (e) {
    createError.value = e.response?.data?.message || '创建失败'
  } finally {
    creating.value = false
  }
}

function goToDetail(id) {
  if (authStore.isAuthenticated) {
    router.push(`/groups/${id}`)
  } else {
    router.push(`/login?next=/groups/${id}`)
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-maple-700">兴趣小组</h1>
      <button
        v-if="authStore.isAuthenticated"
        @click="showCreateModal = true"
        class="px-4 py-2 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors cursor-pointer"
      >
        + 创建小组
      </button>
    </div>

    <div v-if="loading" class="text-center text-text-secondary py-8">加载中...</div>

    <div v-else-if="!groups.length" class="text-center text-text-secondary py-16">
      <p class="text-lg mb-2">还没有小组</p>
      <p class="text-sm">创建一个吧</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="group in groups"
        :key="group.id"
        @click="goToDetail(group.id)"
        class="bg-white rounded-xl border border-border overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
      >
        <div class="h-32 bg-gradient-to-r from-maple-600 to-maple-400 relative">
          <img
            v-if="group.cover_url"
            :src="group.cover_url"
            class="w-full h-full object-cover"
          />
        </div>
        <div class="p-4">
          <h3 class="font-medium text-text-primary">{{ group.name }}</h3>
          <p v-if="group.description" class="text-sm text-text-secondary mt-1 line-clamp-2">{{ group.description }}</p>
          <div class="flex items-center gap-4 mt-3 text-xs text-text-secondary">
            <span>👥 {{ group.member_count || 0 }} 名成员</span>
            <span v-if="!group.is_public" class="px-1.5 py-0.5 bg-gray-100 rounded">私密</span>
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40" @click.self="showCreateModal = false">
        <div class="bg-white rounded-2xl p-6 w-full max-w-md mx-4 shadow-xl">
          <h2 class="text-lg font-bold text-text-primary mb-4">创建小组</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-text-primary mb-1">名称</label>
              <input
                v-model="createForm.name"
                type="text"
                placeholder="输入小组名称"
                class="w-full px-3 py-2 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-text-primary mb-1">简介</label>
              <textarea
                v-model="createForm.description"
                rows="3"
                placeholder="小组简介（可选）"
                class="w-full px-3 py-2 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600 resize-none"
              />
            </div>
            <div class="flex items-center gap-2">
              <input
                v-model="createForm.is_public"
                type="checkbox"
                :true-value="true"
                :false-value="false"
                class="rounded border-border text-maple-600 focus:ring-maple-600"
              />
              <label class="text-sm text-text-primary">公开小组（任何人都可加入）</label>
            </div>
          </div>
          <p v-if="createError" class="text-red-500 text-sm">{{ createError }}</p>
          <div class="flex gap-3 mt-6 justify-end">
            <button
              @click="showCreateModal = false"
              class="px-4 py-2 text-sm text-text-secondary hover:text-text-primary transition-colors cursor-pointer"
            >
              取消
            </button>
            <button
              @click="createGroup"
              :disabled="creating || !createForm.name.trim()"
              class="px-5 py-2 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors disabled:opacity-50 cursor-pointer"
            >
              {{ creating ? '创建中...' : '创建' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
