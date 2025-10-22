import { defineStore } from "pinia";
import router from '@/router'

export const useLoginModalStore = defineStore('loginModal', {
  state: () => ({
    showLoginModal: false,
  }),
  actions: {
    openLoginModal() {
      this.showLoginModal = true;
    },
    closeLoginModal() {
      this.showLoginModal = false;
    },
  },
});