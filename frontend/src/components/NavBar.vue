<template>
  <div class="container mt-4">
    <header class="d-flex justify-content-between align-items-center mb-4 p-3 border rounded">
      <nav class="d-inline-flex">
        <router-link to="/" class="grow text-decoration-none text-success me-3"
          :class="$route.name == 'AdminDashboard' ? 'neonText ' : ''">Home</router-link>
        <router-link to="/quiz" class="grow text-decoration-none text-success me-3"
          :class="$route.name == 'QuizManagement' ? 'neonText ' : ''">Quiz</router-link>
        <router-link to="/" class="grow text-decoration-none text-success me-3">Summary</router-link>
        <a class="grow text-decoration-none text-danger me-3" @click.prevent="logOut">Logout</a>
      </nav>
      <div class="d-flex align-items-center">
        <router-link v-if="$route.name !== 'UserManagement' && getUser.roles && getUser.roles.includes('admin')" class="routerLink btn btn-outline-primary me-5"
          to="/users">User Management</router-link>
        <input type="text" class="grow-search form-control me-5" placeholder="Search" style="width: 200px;" />
        <span>Welcome, {{ username }}</span>
      </div>
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
  text-decoration: none;
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
