<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { profileApi } from '@/api/profiles'
import { relativeTime } from '@/utils/time'
import AvatarImage from '@/components/AvatarImage.vue'

const route = useRoute()
const entries = ref([])
const loading = ref(true)
const newContent = ref('')
const targetUserId = computed(() => route.params.userId)

onMounted(async () => {
  if (!targetUserId.value) return
  try {
    const res = await profileApi.guestbook(targetUserId.value, { page: 1, page_size: 20 })
    entries.value = res.data?.results || []
  } catch { /* ignore */ } finally {
    loading.value = false
  }
})

async function submitEntry() {
  if (!newContent.value.trim() || !targetUserId.value) return
  try {
    const res = await profileApi.createGuestbook(targetUserId.value, newContent.value.trim())
    entries.value.unshift(res.data)
    newContent.value = ''
  } catch { /* ignore */ }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-maple-700 mb-6">留言板</h1>

    <div class="bg-white rounded-2xl shadow-sm border border-border p-4 mb-6">
      <textarea
        v-model="newContent"
        rows="3"
        placeholder="留下你的留言..."
        class="w-full px-4 py-3 border border-border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600 resize-none"
      />
      <div class="flex justify-end mt-2">
        <button
          @click="submitEntry"
          :disabled="!newContent.trim()"
          class="px-5 py-1.5 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors disabled:opacity-50 cursor-pointer"
        >
          发布
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center text-text-secondary py-12">加载中...</div>

    <div v-else-if="!entries.length" class="text-center text-text-secondary py-12">
      暂无留言
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="entry in entries"
        :key="entry.id"
        class="bg-white rounded-2xl shadow-sm border border-border p-4 flex items-start gap-3"
      >
        <AvatarImage :user="entry.user" size="sm" />
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2">
            <span class="text-sm font-medium text-text-primary">{{ entry.user?.nickname }}</span>
            <span class="text-xs text-text-secondary">{{ relativeTime(entry.created_at) }}</span>
          </div>
          <p class="text-sm text-text-primary mt-1">{{ entry.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
