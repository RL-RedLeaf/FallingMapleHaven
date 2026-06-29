<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const settings = ref({
  allow_register: true,
  site_notice: '',
  site_name: 'FallingMapleHaven',
})
const saving = ref(false)
const saved = ref(false)
const error = ref('')

function applySettings(items) {
  for (const item of items || []) {
    settings.value[item.key] = item.value
  }
}

onMounted(async () => {
  try {
    const res = await adminApi.settings()
    applySettings(res.data)
  } catch {
    error.value = '站点设置加载失败'
  }
})

async function saveSettings() {
  saving.value = true
  saved.value = false
  error.value = ''
  try {
    await adminApi.updateSettings(settings.value)
    saved.value = true
  } catch { /* ignore */ } finally {
    error.value = saved.value ? '' : '站点设置保存失败'
    saving.value = false
  }
}
</script>

<template>
  <div>
    <h2 class="text-xl font-bold text-text-primary mb-6">站点设置</h2>
    <p v-if="error" class="mb-4 text-sm text-red-500">{{ error }}</p>
    <div class="bg-white rounded-xl border border-border p-6 max-w-lg space-y-5">
      <div>
        <label class="flex items-center gap-3 cursor-pointer">
          <input
            v-model="settings.allow_register"
            type="checkbox"
            class="rounded border-border text-maple-600 focus:ring-maple-600"
          />
          <span class="text-sm text-text-primary">允许新用户注册</span>
        </label>
      </div>
      <div>
        <label class="block text-sm font-medium text-text-primary mb-1">网站名称</label>
        <input
          v-model="settings.site_name"
          type="text"
          class="w-full px-3 py-2 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-text-primary mb-1">站点公告</label>
        <textarea
          v-model="settings.site_notice"
          rows="4"
          placeholder="输入公告内容..."
          class="w-full px-3 py-2 border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-maple-600/20 focus:border-maple-600 resize-none"
        />
      </div>
      <button
        @click="saveSettings"
        :disabled="saving"
        class="px-5 py-2 bg-maple-600 text-white text-sm rounded-lg hover:bg-maple-700 transition-colors disabled:opacity-50 cursor-pointer"
      >
        {{ saving ? '保存中...' : '保存设置' }}
      </button>
      <p v-if="saved" class="text-sm text-green-600">设置已保存</p>
    </div>
  </div>
</template>
