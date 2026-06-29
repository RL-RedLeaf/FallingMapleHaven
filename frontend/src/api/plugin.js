import client from './client'

export const quizApi = {
  create: (data) => client.post('/plugins/quiz/questions/', data),
  received: () => client.get('/plugins/quiz/questions/received/'),
  answer: (id, answer) => client.post(`/plugins/quiz/questions/${id}/answer/`, { answer }),
  result: (friendId) => client.get(`/plugins/quiz/result/${friendId}/`),
}

export const questionBoxApi = {
  ask: (data) => client.post('/plugins/question-box/', data),
  inbox: () => client.get('/plugins/question-box/inbox/'),
  answer: (id, answer) => client.post(`/plugins/question-box/${id}/answer/`, { answer }),
  delete: (id) => client.delete(`/plugins/question-box/${id}/delete/`),
}

export const groupApi = {
  list: () => client.get('/groups/'),
  detail: (id) => client.get(`/groups/${id}/`),
  create: (data) => client.post('/groups/create/', data),
  join: (id) => client.post(`/groups/${id}/join/`),
  leave: (id) => client.post(`/groups/${id}/leave/`),
  posts: (id) => client.get(`/groups/${id}/posts/`),
}
