export default [
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', name: 'AdminStats', component: () => import('@/views/admin/AdminStatsPage.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('@/views/admin/AdminUsersPage.vue') },
      { path: 'posts', name: 'AdminPosts', component: () => import('@/views/admin/AdminPostsPage.vue') },
      { path: 'plugins', name: 'AdminPlugins', component: () => import('@/views/admin/AdminPluginsPage.vue') },
      { path: 'settings', name: 'AdminSettings', component: () => import('@/views/admin/AdminSettingsPage.vue') },
      { path: 'logs', name: 'AdminLogs', component: () => import('@/views/admin/AdminLogsPage.vue') },
      { path: 'anonymous-questions', name: 'AdminAnonymousQuestions', component: () => import('@/views/admin/AdminAnonymousQuestionsPage.vue') },
    ],
  },
]
