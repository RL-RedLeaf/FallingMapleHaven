<script setup>
const props = defineProps({
  modelValue: { type: Boolean, required: true },
  disabled: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue'])

function toggle() {
  if (props.disabled) return
  emit('update:modelValue', !props.modelValue)
}
</script>

<template>
  <button
    type="button"
    role="switch"
    :aria-checked="modelValue"
    :disabled="disabled"
    @click="toggle"
    class="relative inline-flex items-center flex-shrink-0 w-11 h-6 rounded-full transition-colors duration-200 ease-out cursor-pointer focus-visible:outline-2 focus-visible:outline-maple-600 focus-visible:outline-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
    :class="modelValue ? 'bg-maple-600' : 'bg-gray-300'"
  >
    <span
      class="absolute top-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-all duration-200 ease-out"
      :class="modelValue ? 'left-[22px]' : 'left-0.5'"
    />
  </button>
</template>
