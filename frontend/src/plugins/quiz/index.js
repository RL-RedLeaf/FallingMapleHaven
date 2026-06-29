import { pluginRegistry } from '../registry'

pluginRegistry.register({
  type: 'quiz',
  name: '默契问答',
  icon: 'help-circle',
  route: { path: '/profile/:userId/plugins/quiz', name: 'QuizPage' },
})
