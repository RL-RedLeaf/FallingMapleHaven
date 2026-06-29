<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const plugins = ref([])
const loading = ref(true)
const error = ref('')

async function fetchPlugins() {
  loading.value = true
  error.value = ''
  try {
    const res = await adminApi.plugins()
    plugins.value = res.data || []
  } catch {
    error.value = '插件列表加载失败'
  } finally {
    loading.value = false
  }
}

async function togglePlugin(plugin) {
  const nextActive = !plugin.is_active
  try {
    const res = await adminApi.updatePlugin(plugin.id, { is_active: nextActive })
    Object.assign(plugin, res.data)
  } catch {
    error.value = '插件状态更新失败'
  }
}

onMounted(fetchPlugins)
</script>

<template>
  <div>
    <h2 class="text-xl font-bold text-text-primary mb-6">插件管理</h2>
    <p v-if="error" class="mb-4 text-sm text-red-500">{{ error }}</p>
    <div v-if="loading" class="text-center text-text-secondary py-8">加载中...</div>
    <div v-else-if="!plugins.length" class="text-center text-text-secondary py-8">暂无插件</div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="plugin in plugins"
        :key="plugin.id"
        class="bg-white rounded-xl border border-border p-4 space-y-3"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-text-primary">{{ plugin.name }}</h3>
          <button
            @click="togglePlugin(plugin)"
            class="relative w-10 h-5 rounded-full transition-colors cursor-pointer"
            :class="plugin.is_active ? 'bg-maple-600' : 'bg-gray-300'"
          >
            <div
              class="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform"
              :class="plugin.is_active ? 'translate-x-[22px]' : 'translate-x-0.5'"
            />
          </button>
        </div>
        <p class="text-xs text-text-secondary">类型: {{ plugin.type }}</p>
        <p class="text-xs text-text-secondary">{{ plugin.description || '暂无描述' }}</p>
      </div>
    </div>
  </div>
</template>
