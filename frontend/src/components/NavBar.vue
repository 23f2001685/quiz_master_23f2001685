<template>

  <div class="container navbar-expand-lg">
    <header class="d-flex justify-content-between align-items-center mb-4 p-3 border rounded">
      <nav class="d-inline-flex-m">
        <router-link to="/" class="grow text-decoration-none text-success me-3"
          :class="$route.name == 'AdminDashboard' ? 'neonText ' : ''">Home</router-link>
        <router-link to="/quiz" class="grow text-decoration-none text-success me-3" v-if="isAdmin"
          :class="$route.name == 'QuizManagement' ? 'neonText ' : ''">Quiz</router-link>
        <router-link to="/quiz" class="grow text-decoration-none text-success me-3" v-else
          :class="$route.name == 'QuizManagement' ? 'neonText ' : ''">Scores</router-link>
        <router-link to="/" class="grow text-decoration-none text-success me-3">Summary</router-link>
      </nav>
      <span class="fs-3"><span class="fw-bold">Welcome, </span>{{ username }}</span>
      <router-link v-if="$route.name !== 'UserManagement' && isAdmin" class="routerLink btn btn-outline-primary"
        to="/users"><i class="bi bi-person-fill-gear pe-2"></i>User Management</router-link>
        <input type="text" class="grow-search form-control" placeholder="Search" style="width: 200px;" />
        <button class="btn btn-outline-danger d-flex align-items-center gap-2" @click="logOut">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-box-arrow-right" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-7a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-7A1.5 1.5 0 0 0 1 3.5v9A1.5 1.5 0 0 0 2.5 14h7a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/>
            <path fill-rule="evenodd" d="M15.354 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L13.293 7.5H5.5a.5.5 0 0 0 0 1h7.793l-1.647 1.646a.5.5 0 0 0 .708.708l3-3z"/>
          </svg>
          Log Out
        </button>
    </header>
  </div>
</template>

<script>

import { RouterLink } from 'vue-router';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'NavBar',
  props: ['username'],
  components: { RouterLink },
  computed: {
    ...mapGetters(['getUser']),
    isAdmin() {
      return this.getUser && this.getUser.roles && this.getUser.roles.includes('admin');
    },
  },
  methods: {
    ...mapActions(['logOut']),
    async logOut() {
      await this.$store.dispatch('logOut');
      localStorage.clear()
      this.$router.push('/login')
    }
  },
  async mounted() {
    await this.$store.dispatch('fetchUser');

  },
};
</script>

<style scoped>
a:hover {
  text-decoration: underline !important;
}

.grow-search {
  transition: all .8s ease-in-out;
}

.grow-search:hover {
  transform: scale(1.3);
}

.routerLink {
  text-decoration: none !important;
}

@media only screen and (max-width: 990px) {
  header {
    overflow-x: scroll;
  }
}

header {
  background: rgba(181, 177, 177, 0.35);
  box-shadow: 0 8px 32px 0 rgba(18, 19, 32, 0.557);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.509) !important;
}

a {
  cursor: pointer;
}
</style>
