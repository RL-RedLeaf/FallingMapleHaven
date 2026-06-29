<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { groupApi } from '@/api/plugin'
import { postApi } from '@/api/posts'
import { useToast } from '@/composables/useToast'
import PostCard from '@/components/PostCard.vue'
import AvatarImage from '@/components/AvatarImage.vue'
import TabBar from '@/components/TabBar.vue'

const route = useRoute()
const authStore = useAuthStore()
const groupId = computed(() => Number(route.params.groupId))

const group = ref(null)
const posts = ref([])
const members = ref([])
const activeTab = ref('posts')
const loading = ref(true)
const joining = ref(false)
const newPostContent = ref('')
const submittingPost = ref(false)

const isMember = computed(() => {
  if (!group.value?.members) return false
  return group.value.members.some(m => m.user_id === authStore.user?.user_id)
})

const isOwner = computed(() => {
  return group.value?.owner?.user_id === authStore.user?.user_id
})

const toast = useToast()

onMounted(() => {
  fetchGroup()
})

watch(() => route.params.groupId, () => {
  fetchGroup()
})

async function fetchGroup() {
  loading.value = true
  try {
    const res = await groupApi.detail(groupId.value)
    group.value = res.data
    members.value = res.data?.members || []
    if (isMember.value) {
      await fetchPosts()
    }
  } catch { /* ignore */ } finally {
    loading.value = false
  }
}

async function fetchPosts() {
  try {
    const res = await groupApi.posts(groupId.value)
    posts.value = res.data?.results || res.data || []
  } catch { /* ignore */ }
}

async function handleJoin() {
  joining.value = true
  try {
    await groupApi.join(groupId.value)
    await fetchGroup()
    toast.success('已加入小组')
  } catch { /* ignore */ } finally {
    joining.value = false
  }
}

async function handleLeave() {
  joining.value = true
  try {
    await groupApi.leave(groupId.value)
    await fetchGroup()
    toast.success('已退出小组')
  } catch { /* ignore */ } finally {
    joining.value = false
  }
}

function getRole(member) {
  return member.user_id === group.value?.owner?.user_id ? '组长' : '成员'
}

async function submitGroupPost() {
  if (!newPostContent.value.trim() || submittingPost.value) return
  submittingPost.value = true
  try {
    const formData = new FormData()
    formData.append('content', newPostContent.value.trim())
    formData.append('group_id', groupId.value)
    await postApi.create(formData)
    newPostContent.value = ''
    await fetchPosts()
    toast.success('已发布到小组')
  } catch { /* ignore */ } finally {
    submittingPost.value = false
  }
}
</script>

<template>
  <div v-if="loading" class="max-w-4xl mx-auto px-4 py-8 text-center text-text-secondary">加载中...</div>

  <div v-else-if="group" class="max-w-4xl mx-auto px-4 pb-8">
    <div class="relative w-full rounded-b-2xl overflow-hidden h-48 bg-gradient-to-r from-maple-600 to-maple-400">
      <img v-if="group.cover_url" :src="group.cover_url" class="w-full h-full object-cover" />
    </div>

    <div class="px-4 -mt-8 relative z-10">
      <div class="bg-white rounded-xl border border-border p-5 shadow-sm">
        <h1 class="text-xl font-bold text-text-primary">{{ group.name }}</h1>
        <p v-if="group.description" class="text-sm text-text-secondary mt-1">{{ group.description }}</p>
        <div class="flex items-center gap-4 mt-3 text-xs text-text-secondary">
          <span>创建者: {{ group.owner?.nickname }}</span>
          <span>👥 {{ group.member_count || members.length }} 名成员</span>
          <span v-if="!group.is_public" class="px-1.5 py-0.5 bg-gray-100 rounded">私密</span>
        </div>
        <button
          v-if="!isOwner"
          @click="isMember ? handleLeave() : handleJoin()"
          :disabled="joining"
          class="mt-4 px-5 py-2 text-sm rounded-lg transition-colors cursor-pointer disabled:opacity-50"
          :class="isMember ? 'border border-maple-600 text-maple-600 hover:bg-maple-50' : 'bg-maple-600 text-white hover:bg-maple-700'"
        >
          {{ joining ? '处理中...' : isMember ? '退出小组' : '加入小组' }}
        </button>
      </div>
    </div>

    <div class="px-4 mt-6">
      <TabBar
        :tabs="[{ key: 'posts', label: '动态' }, { key: 'members', label: '成员' }]"
        :activeKey="activeTab"
        @update:activeKey="activeTab = $event"
      />

      <div v-if="activeTab === 'posts'" class="mt-4 space-y-4">
        <div v-if="!isMember" class="text-center text-text-secondary py-8">
          加入小组后即可查看组内动态
        </div>
        <template v-else>
          <div class="bg-white rounded-2xl shadow-sm border border-border p-4">
            <textarea
              v-model="newPostContent"
              rows="3"
              placeholder="分享到小组..."
              class="w-full px-4 py-3 border border-border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600 resize-none"
            />
            <div class="flex justify-end mt-2">
              <button
                @click="submitGroupPost"
                :disabled="submittingPost || !newPostContent.trim()"
                class="px-5 py-1.5 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors disabled:opacity-50 cursor-pointer"
              >
                {{ submittingPost ? '发布中...' : '发布' }}
              </button>
            </div>
          </div>
          <div v-if="!posts.length" class="text-center text-text-secondary py-8">
            暂无动态
          </div>
          <PostCard v-for="post in posts" :key="post.id" :post="post" :showActions="true" />
        </template>
      </div>

      <div v-if="activeTab === 'members'" class="mt-4 space-y-3">
        <div v-for="m in members" :key="m.user_id" class="flex items-center gap-3 py-2">
          <AvatarImage :user="m" size="md" />
          <div class="flex-1 min-w-0">
            <span class="text-sm font-medium text-text-primary">{{ m.nickname }}</span>
          </div>
          <span class="text-xs px-2 py-0.5 rounded-full" :class="getRole(m) === '组长' ? 'bg-maple-100 text-maple-600' : 'bg-gray-100 text-text-secondary'">
            {{ getRole(m) }}
          </span>
        </div>
        <div v-if="!members.length" class="text-center text-text-secondary py-8">暂无成员</div>
      </div>
    </div>
  </div>

  <div v-else class="max-w-4xl mx-auto px-4 py-8 text-center text-text-secondary">小组不存在</div>
</template>
