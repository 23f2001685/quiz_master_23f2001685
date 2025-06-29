<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-4">User Dashboard</h2>
      <div class="d-flex justify-content-end mb-3">
        <button class="btn btn-outline-danger d-flex align-items-center gap-2" @click="logOut">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-box-arrow-right" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-7a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-7A1.5 1.5 0 0 0 1 3.5v9A1.5 1.5 0 0 0 2.5 14h7a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/>
            <path fill-rule="evenodd" d="M15.354 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L13.293 7.5H5.5a.5.5 0 0 0 0 1h7.793l-1.647 1.646a.5.5 0 0 0 .708.708l3-3z"/>
          </svg>
          Log Out
        </button>
      </div>
    </div>
    <Toast ref="toastRef" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import Toast from '../../components/Toast.vue';

export default {

  name: 'UserDashboard',
  components: {
    Toast,
  },
  methods: {
    showToast() {
      this.$refs.toastRef.showToast('Hello', 'This is a toast message from User Dashboard!');
    },
    logOut() {
      this.$store.dispatch('logOut');
      this.$router.push('/login');
    }
  },
  computed: {
    ...mapGetters([
      'getUser'
    ])
  },
  async mounted() {
    console.log(this.getUser);
  }

};
</script>

<style scoped>
header nav a:hover {
  text-decoration: underline;
}

footer button {
  width: 50px;
  height: 50px;
}
</style>
