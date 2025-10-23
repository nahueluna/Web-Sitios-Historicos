import { defineStore } from "pinia";

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