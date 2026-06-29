import client from './client'

export const postApi = {
  list: (params) => client.get('/posts/', { params }),
  create: (formData) => client.post('/posts/create/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  detail: (id) => client.get(`/posts/${id}/`),
  delete: (id) => client.delete(`/posts/${id}/delete/`),
  like: (id) => client.post(`/posts/${id}/like/`),
  comments: (id) => client.get(`/posts/${id}/comments/`),
  createComment: (id, content) => client.post(`/posts/${id}/comments/create/`, { content }),
  deleteComment: (id) => client.delete(`/posts/comments/${id}/delete/`),
}
