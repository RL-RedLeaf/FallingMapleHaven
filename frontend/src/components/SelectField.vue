<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import Icon from './Icon.vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, required: true },
  placeholder: { type: String, default: '请选择' },
  disabled: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue'])

const open = ref(false)
const dropdownRef = ref(null)
const buttonRef = ref(null)
const panelStyle = ref({})

const selectedLabel = computed(() => {
  if (!props.modelValue && props.modelValue !== 0) return ''
  const opt = props.options.find(o => (o.value ?? o) === props.modelValue)
  return opt ? (opt.label ?? opt) : ''
})

function toggle() {
  if (props.disabled) return
  open.value = !open.value
}

function select(val) {
  emit('update:modelValue', val)
  open.value = false
  buttonRef.value?.focus()
}

function onDocumentClick(e) {
  if (!open.value) return
  const isButton = buttonRef.value?.contains(e.target)
  const isPanel = dropdownRef.value?.contains(e.target)
  if (!isButton && !isPanel) {
    open.value = false
  }
}

function onKeydown(e) {
  if (e.key === 'Escape' && open.value) {
    open.value = false
    buttonRef.value?.focus()
  }
  if (e.key === 'Enter' || e.key === ' ') {
    if (document.activeElement === buttonRef.value) {
      e.preventDefault()
      toggle()
    }
  }
}

function onScroll() {
  if (open.value) positionPanel()
}

function positionPanel() {
  if (!buttonRef.value) return
  const rect = buttonRef.value.getBoundingClientRect()
  const gap = 4
  panelStyle.value = {
    top: `${rect.bottom + gap}px`,
    left: `${rect.left}px`,
    width: `${rect.width}px`,
  }
}

watch(open, async (val) => {
  if (val) {
    await nextTick()
    positionPanel()
  }
})

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
  document.addEventListener('keydown', onKeydown)
  document.addEventListener('scroll', onScroll, true)
  window.addEventListener('resize', onScroll)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
  document.removeEventListener('scroll', onScroll, true)
  window.removeEventListener('resize', onScroll)
})
</script>

<template>
  <div class="relative">
    <button
      ref="buttonRef"
      type="button"
      :disabled="disabled"
      class="input-base flex items-center justify-between gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed text-left"
      :class="open ? 'ring-2 ring-maple-600/20 border-maple-600' : ''"
      @click="toggle"
      aria-haspopup="listbox"
      :aria-expanded="open"
    >
      <span :class="selectedLabel ? 'text-text-primary' : 'text-text-secondary/50'">
        {{ selectedLabel || placeholder }}
      </span>
      <Icon
        name="chevronDown"
        :size="16"
        class="text-text-secondary shrink-0 transition-transform duration-150"
        :class="open ? 'rotate-180' : ''"
      />
    </button>
    <Teleport to="body">
      <Transition name="drop">
        <div
          v-if="open"
          ref="dropdownRef"
          role="listbox"
          :style="panelStyle"
          class="fixed z-[70] bg-white rounded-xl shadow-modal border border-border overflow-hidden max-h-60 overflow-y-auto"
        >
          <button
            v-for="opt in options"
            :key="opt.value ?? opt"
            role="option"
            type="button"
            :aria-selected="(opt.value ?? opt) === modelValue"
            class="w-full text-left px-4 py-2.5 text-sm transition-colors cursor-pointer"
            :class="(opt.value ?? opt) === modelValue
              ? 'bg-maple-50 text-maple-700 font-medium'
              : 'text-text-primary hover:bg-maple-50/60'"
            @click="select(opt.value ?? opt)"
          >
            {{ opt.label ?? opt }}
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.drop-enter-active,
.drop-leave-active {
  transition: all 0.15s ease-out;
}
.drop-enter-from,
.drop-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
