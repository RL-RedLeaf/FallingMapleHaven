import client from './client'

export const friendApi = {
  request: (to_user_id) => client.post('/friends/request/', { to_user_id }),
  handle: (payload) => client.post('/friends/handle/', payload),
  unfriend: (friend_id) => client.post('/friends/unfriend/', { friend_id }),
  list: () => client.get('/friends/'),
  requests: () => client.get('/friends/requests/'),
  search: (q) => client.get('/friends/search/', { params: { q } }),
}
