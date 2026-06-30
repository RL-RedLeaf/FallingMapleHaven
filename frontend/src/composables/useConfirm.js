import { reactive } from 'vue'

const dialogState = reactive({
  visible: false,
  title: '',
  message: '',
  confirmText: '确认',
  cancelText: '取消',
  variant: 'default',
})

let resolveCallback = null

export function useConfirm() {
  function confirm(options = {}) {
    Object.assign(dialogState, {
      visible: true,
      title: options.title || '确认',
      message: options.message || '',
      confirmText: options.confirmText || '确认',
      cancelText: options.cancelText || '取消',
      variant: options.variant || 'default',
    })
    return new Promise((resolve) => {
      resolveCallback = resolve
    })
  }

  function resolveConfirm(value) {
    dialogState.visible = false
    resolveCallback?.(value)
    resolveCallback = null
  }

  return { dialogState, confirm, resolveConfirm }
}
