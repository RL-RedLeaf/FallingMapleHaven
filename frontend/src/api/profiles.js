import client from './client'

function lookupConfig(userId, params = {}) {
  return {
    params: {
      ...params,
      ...(/^\d+$/.test(String(userId)) ? { lookup: 'id' } : {}),
    },
  }
}

export const profileApi = {
  get: (userId) => client.get(`/profiles/${userId}/`, lookupConfig(userId)),
  visitors: (userId, params) => client.get(`/profiles/${userId}/visitors/`, lookupConfig(userId, params)),
  posts: (userId, params) => client.get(`/profiles/${userId}/posts/`, lookupConfig(userId, params)),
  guestbook: (userId, params) => client.get(`/profiles/${userId}/guestbook/`, lookupConfig(userId, params)),
  createGuestbook: (userId, content) => client.post(`/profiles/${userId}/guestbook/create/`, { content }, lookupConfig(userId)),
  replyGuestbook: (entryId, reply) => client.post(`/profiles/guestbook/${entryId}/reply/`, { reply }),
  deleteGuestbook: (entryId) => client.delete(`/profiles/guestbook/${entryId}/delete/`),
  getAdminInfo: (userId) => client.get(`/profiles/${userId}/admin/`),
  banUser: (userId, isActive) => client.patch(`/profiles/${userId}/admin/`, { is_active: isActive }),
}
