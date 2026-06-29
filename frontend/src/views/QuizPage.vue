<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { friendApi } from '@/api/friends'
import { quizApi } from '@/api/plugin'
import TabBar from '@/components/TabBar.vue'
import Icon from '@/components/Icon.vue'
import SelectField from '@/components/SelectField.vue'

const route = useRoute()
const authStore = useAuthStore()
const activeTab = ref('create')

const friends = ref([])
const selectedFriendId = ref(null)
const questionText = ref('')
const correctAnswer = ref('')
const createMessage = ref('')
const submitting = ref(false)

const receivedQuestions = ref([])
const loadingReceived = ref(false)
const answerText = ref({})

const matchFriendId = ref(null)
const matchResult = ref(null)
const loadingMatch = ref(false)

onMounted(() => {
  fetchFriends()
  fetchReceived()
})

async function fetchFriends() {
  try {
    const res = await friendApi.list()
    friends.value = res.data || []
  } catch { /* ignore */ }
}

async function fetchReceived() {
  loadingReceived.value = true
  try {
    const res = await quizApi.received()
    receivedQuestions.value = res.data || []
  } catch { /* ignore */ } finally {
    loadingReceived.value = false
  }
}

async function submitQuestion() {
  if (!selectedFriendId.value || !questionText.value.trim() || !correctAnswer.value.trim()) return
  submitting.value = true
  createMessage.value = ''
  try {
    await quizApi.create({
      target_user_id: selectedFriendId.value,
      question: questionText.value.trim(),
      correct_answer: correctAnswer.value.trim(),
    })
    createMessage.value = '出题成功!'
    questionText.value = ''
    correctAnswer.value = ''
    selectedFriendId.value = null
  } catch (e) {
    createMessage.value = e.response?.data?.detail || '出题失败'
  } finally {
    submitting.value = false
  }
}

async function submitAnswer(question) {
  const answer = answerText.value[question.id]
  if (!answer?.trim()) return
  try {
    const res = await quizApi.answer(question.id, answer.trim())
    question.has_answered = true
    question.is_correct = res.data?.is_correct
    question.result = res.data
  } catch { /* ignore */ }
}

async function fetchResult() {
  if (!matchFriendId.value) return
  loadingMatch.value = true
  try {
    const res = await quizApi.result(matchFriendId.value)
    matchResult.value = res.data
  } catch { /* ignore */ } finally {
    loadingMatch.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-maple-700 mb-6">默契问答</h1>

    <TabBar
      :tabs="[{ key: 'create', label: '出题' }, { key: 'answer', label: '答题' }, { key: 'match', label: '匹配度' }]"
      :activeKey="activeTab"
      @update:activeKey="activeTab = $event"
      class="mb-6"
    />

    <div v-if="activeTab === 'create'" class="space-y-4 max-w-lg">
      <div>
        <label class="block text-sm font-medium text-text-primary mb-1">选择好友</label>
        <SelectField
          v-model="selectedFriendId"
          :options="friends.map(f => ({ value: f.id || f.user_id, label: f.nickname || f.username }))"
          placeholder="请选择好友"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-text-primary mb-1">题目</label>
        <input
          v-model="questionText"
          type="text"
          placeholder="输入题目..."
          class="input-base"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-text-primary mb-1">正确答案</label>
        <input
          v-model="correctAnswer"
          type="text"
          placeholder="输入正确答案..."
          class="input-base"
        />
      </div>
      <button
        @click="submitQuestion"
        :disabled="submitting || !selectedFriendId || !questionText.trim() || !correctAnswer.trim()"
        class="btn-primary px-5 py-2.5"
      >
        {{ submitting ? '提交中...' : '提交题目' }}
      </button>
      <p v-if="createMessage" class="text-sm" :class="createMessage.includes('成功') ? 'text-green-600' : 'text-red-500'">
        {{ createMessage }}
      </p>
    </div>

    <div v-if="activeTab === 'answer'" class="space-y-4">
      <div v-if="loadingReceived" class="text-center text-text-secondary py-8">加载中...</div>
      <div v-else-if="!receivedQuestions.length" class="text-center text-text-secondary py-8">暂未收到题目</div>
      <div
        v-for="q in receivedQuestions"
        :key="q.id"
        class="card-base p-4 space-y-3"
      >
        <div class="text-sm text-text-secondary">来自: {{ q.from_user?.nickname || q.from_user?.username || '匿名' }}</div>
        <p class="text-sm font-medium text-text-primary">{{ q.question }}</p>
        <div v-if="!q.has_answered" class="flex gap-2">
          <input
            v-model="answerText[q.id]"
            type="text"
            placeholder="输入答案..."
            class="flex-1 input-base"
            @keyup.enter="submitAnswer(q)"
          />
          <button
            @click="submitAnswer(q)"
            class="btn-primary"
          >
            提交
          </button>
        </div>
        <div v-else class="text-sm font-medium" :class="q.is_correct ? 'text-green-600' : 'text-red-500'">
          {{ q.is_correct ? '回答正确!' : '回答错误' }}
          <span v-if="q.result?.correct_answer" class="text-text-secondary ml-2">正确答案: {{ q.result.correct_answer }}</span>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'match'" class="space-y-4 max-w-lg">
      <div>
        <label class="block text-sm font-medium text-text-primary mb-1">选择好友查看匹配度</label>
        <SelectField
          v-model="matchFriendId"
          :options="friends.map(f => ({ value: f.id || f.user_id, label: f.nickname || f.username }))"
          placeholder="请选择好友"
          @update:model-value="fetchResult"
        />
      </div>
      <div v-if="loadingMatch" class="text-center text-text-secondary py-4">加载中...</div>
      <div v-else-if="matchResult" class="bg-white rounded-xl border border-border p-6 text-center space-y-3">
        <div class="text-4xl font-bold text-maple-600">{{ matchResult.match_score || 0 }}%</div>
        <div class="text-sm text-text-secondary">匹配度</div>
        <div class="flex justify-center gap-6 text-sm text-text-secondary">
          <span>总题数: {{ matchResult.total_questions || 0 }}</span>
          <span>正确数: {{ matchResult.correct_count || 0 }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
