<script>
import { RouterView } from "vue-router";
import NavBar from './components/NavBar.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'App',
  components: { RouterView, NavBar },
  data() {
    return {
      isAdmin: false,
      isUser: false,
      isUserActive: false,
    }
  },
  computed: {
    ...mapGetters(['getUser']),
  },
  async mounted() {
    await this.$store.dispatch('fetchUser');
    if (!this.getUser) {
      this.$router.push('/login');
      return;
    }
    if (this.getUser.error) {
      alert(this.getUser.error);
      this.$router.push('/login');
      return;
    }
    const roles = await this.getUser.roles;
    this.isAdmin = roles.includes('admin')
    this.isUser = roles.includes('user')
    if (!this.isAdmin) {
      if (!this.getUser.active) {
        alert('Please contact administrator as your account is blocked.')
        this.$router.push('/login')
      }
    }
  },
  watch: {
    getUser(newVal) {
      if (!newVal) {
        this.$router.push('/login');
      }
    }
  }
}

</script>

<template>
  <div>
    <div style="position: sticky; top: 0; z-index: 1000;">
      <NavBar v-if="getUser" :username="getUser ? getUser.full_name : 'Guest'" />
    </div>
    <div style="margin-top: 64px;">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
body {
  font-family: Arial, sans-serif;
}
</style>
