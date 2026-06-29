import client from './client'

export const notificationApi = {
  list: (params) => client.get('/notifications/', { params }),
  read: (id) => client.post(`/notifications/${id}/read/`),
  readAll: () => client.post('/notifications/read-all/'),
  unreadCount: () => client.get('/notifications/unread-count/'),
}
