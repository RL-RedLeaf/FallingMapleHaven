import client from './client'

export const authApi = {
  register: (data) => client.post('/auth/register/', data),
  login: (data) => client.post('/auth/login/', data),
  logout: () => client.post('/auth/logout/'),
  me: () => client.get('/auth/me/'),
  updateMe: (data) => client.patch('/auth/me/', data),
  changePassword: (data) => client.post('/auth/change-password/', data),
  uploadAvatar: (file) => client.post('/auth/avatar/', { avatar: file }, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  uploadCover: (file) => client.post('/auth/cover/', { cover_image: file }, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
}
