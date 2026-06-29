<script setup>
import { onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import NavBar from '@/components/NavBar.vue'
import MobileTabBar from '@/components/MobileTabBar.vue'
import ToastContainer from '@/components/ToastContainer.vue'

const authStore = useAuthStore()
const chatStore = useChatStore()

onMounted(async () => {
  await authStore.ensureSession()
  if (authStore.isAuthenticated) {
    chatStore.connectWs()
  }
})

watch(
  () => authStore.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated) {
      chatStore.connectWs()
    } else {
      chatStore.disconnectWs()
    }
  }
)
</script>

<template>
  <div class="min-h-screen bg-maple-50">
    <NavBar />
    <main class="pb-16 md:pb-0">
      <router-view />
    </main>
    <MobileTabBar />
    <ToastContainer />
  </div>
</template>
