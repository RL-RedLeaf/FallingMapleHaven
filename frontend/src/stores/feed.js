import { defineStore } from 'pinia'
import { postApi } from '@/api/posts'

export const useFeedStore = defineStore('feed', {
  state: () => ({
    posts: [],
    currentPage: 1,
    hasMore: true,
    loading: false,
  }),
  actions: {
    async fetchPosts(params = {}) {
      this.loading = true
      try {
        const res = await postApi.list({ page: this.currentPage, ...params })
        if (this.currentPage === 1) {
          this.posts = res.data.results
        } else {
          this.posts.push(...res.data.results)
        }
        this.hasMore = res.data.page * res.data.page_size < res.data.total
        this.currentPage += 1
      } finally {
        this.loading = false
      }
    },
    async createPost(formData) {
      const res = await postApi.create(formData)
      this.posts.unshift(res.data)
      return res
    },
    async toggleLike(postId) {
      const res = await postApi.like(postId)
      const post = this.posts.find(p => p.id === postId)
      if (post) {
        post.is_liked = res.data.is_liked
        post.like_count = res.data.like_count
      }
      return res
    },
    async deletePost(postId) {
      await postApi.delete(postId)
      this.posts = this.posts.filter(p => p.id !== postId)
    },
  },
})
