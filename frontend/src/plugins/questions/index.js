import { pluginRegistry } from '../registry'

pluginRegistry.register({
  type: 'question_box',
  name: '匿名提问箱',
  icon: 'message-question',
  route: { path: '/profile/:userId/plugins/question-box', name: 'QuestionBoxPage' },
})
