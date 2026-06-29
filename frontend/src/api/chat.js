import client from './client'

export const chatApi = {
  rooms: () => client.get('/chat/rooms/'),
  messages: (roomId, page = 1) => client.get(`/chat/rooms/${roomId}/messages/`, { params: { page, page_size: 50 } }),
  createRoom: (data) => client.post('/chat/rooms/create/', data),
  sendMessage: (roomId, content) => client.post(`/chat/rooms/${roomId}/messages/send/`, { content, msg_type: 'text' }),
}
