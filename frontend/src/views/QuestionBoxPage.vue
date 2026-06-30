<script setup>
import { ref, onMounted, computed } from 'vue'
import { questionBoxApi } from '@/api/plugin'
import { useAuthStore } from '@/stores/auth'
import TabBar from '@/components/TabBar.vue'

const authStore = useAuthStore()
const activeTab = ref('inbox')
const inboxQuestions = ref([])
const loading = ref(false)
const answerText = ref({})
const submittingAnswer = ref(false)

onMounted(() => {
  fetchInbox()
})

async function fetchInbox() {
  loading.value = true
  try {
    const res = await questionBoxApi.inbox()
    inboxQuestions.value = res.data || []
  } catch { /* ignore */ } finally {
    loading.value = false
  }
}

async function submitAnswer(q) {
  const answer = answerText.value[q.id]
  if (!answer?.trim()) return
  submittingAnswer.value = true
  try {
    await questionBoxApi.answer(q.id, answer.trim())
    q.is_answered = true
    q.answer = answer.trim()
    answerText.value[q.id] = ''
  } catch { /* ignore */ } finally {
    submittingAnswer.value = false
  }
}

async function deleteQuestion(q) {
  try {
    await questionBoxApi.delete(q.id)
    inboxQuestions.value = inboxQuestions.value.filter(item => item.id !== q.id)
  } catch { /* ignore */ }
}

const answeredQuestions = computed(() =>
  inboxQuestions.value.filter(q => q.is_answered)
)

const unansweredQuestions = computed(() =>
  inboxQuestions.value.filter(q => !q.is_answered)
)
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-maple-700 mb-6">匿名提问箱</h1>

    <TabBar
      :tabs="[{ key: 'inbox', label: `待回答 (${unansweredQuestions.length})` }, { key: 'answers', label: `已回答 (${answeredQuestions.length})` }]"
      :activeKey="activeTab"
      @update:activeKey="activeTab = $event"
      class="mb-6"
    />

    <div v-if="activeTab === 'inbox'" class="space-y-4">
      <div v-if="loading" class="text-center text-text-secondary py-8">加载中...</div>
      <template v-else-if="unansweredQuestions.length">
        <div v-for="q in unansweredQuestions" :key="q.id" class="bg-white rounded-xl border border-border p-4 space-y-3">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-sm text-text-primary">{{ q.content }}</p>
              <div v-if="authStore.isAdmin && q.real_sender" class="text-xs text-red-500 mt-1">
                真实提问者: {{ q.real_sender.nickname }} (ID: {{ q.real_sender.user_id }})
              </div>
              <span class="text-xs text-text-secondary mt-1 inline-block">未回答</span>
            </div>
            <button
              @click="deleteQuestion(q)"
              class="text-xs text-red-400 hover:text-red-500 transition-colors cursor-pointer flex-shrink-0 ml-2"
            >
              删除
            </button>
          </div>
          <div class="flex gap-2">
            <input
              v-model="answerText[q.id]"
              type="text"
              placeholder="输入回答..."
              class="flex-1 px-3 py-2 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600"
              @keyup.enter="submitAnswer(q)"
            />
            <button
              @click="submitAnswer(q)"
              :disabled="submittingAnswer || !answerText[q.id]?.trim()"
              class="px-4 py-2 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors disabled:opacity-50 cursor-pointer"
            >
              回答
            </button>
          </div>
        </div>
      </template>
      <div v-else class="text-center text-text-secondary py-8">没有待回答的提问</div>
    </div>

    <div v-if="activeTab === 'answers'" class="space-y-4">
      <div v-if="!answeredQuestions.length" class="text-center text-text-secondary py-8">暂无已公开的回答</div>
      <div
        v-for="q in answeredQuestions"
        :key="q.id"
        class="bg-white rounded-xl border border-border p-4 space-y-2"
      >
        <p class="text-sm text-text-primary">Q: {{ q.content }}</p>
        <div v-if="authStore.isAdmin && q.real_sender" class="text-xs text-red-500">
          真实提问者: {{ q.real_sender.nickname }} (ID: {{ q.real_sender.user_id }})
        </div>
        <div class="pl-3 border-l-2 border-maple-400">
          <p class="text-sm text-maple-700">A: {{ q.answer }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
