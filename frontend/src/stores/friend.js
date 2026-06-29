import { defineStore } from 'pinia'
import { friendApi } from '@/api/friends'

export const useFriendStore = defineStore('friend', {
  state: () => ({
    friends: [],
    requests: [],
    loading: false,
  }),
  actions: {
    async fetchFriends() {
      const res = await friendApi.list()
      this.friends = res.data || []
    },
    async fetchRequests() {
      const res = await friendApi.requests()
      this.requests = res.data || []
    },
    async sendRequest(to_user_id) {
      return friendApi.request(to_user_id)
    },
    async handleRequest(params, action) {
      const payload = typeof params === 'object' ? { ...params, action } : { request_id: params, action }
      return friendApi.handle(payload)
    },
    async unfriend(friend_id) {
      return friendApi.unfriend(friend_id)
    },
  },
})
