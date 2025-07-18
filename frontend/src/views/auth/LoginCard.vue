<template>
  <Spinner :active="isActive" />
  <div class="card mx-auto mt-5">
    <div class="card-body">
      <h3 class="card-title text-center">Welcome to Quiz Master</h3>
      <h2 class="text-center text-warning">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input type="email" v-model="email" id="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password:</label>
          <input type="password" v-model="password" id="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
      <div class="text-center mt-3">
            <p>Don't have an account? <router-link to="/Register" class="text-primary">Register here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Spinner from '../../components/Spinner.vue';

export default {
  name: 'LoginCard',
  components: { Spinner },
  data() {
    return {
      email: '',
      password: '',
      role: '',
      isActive: false
    };
  },
  methods: {
    toRegister() {
      this.$router.push('Register')
    },
    async fetchCurrentUserRole(authToken) {
      this.isActive = true
      try {
        const res = await axios.get('http://localhost:5000/me', {
          headers: {
            'Authentication-Token': authToken
          }
        })
        this.role = res.data.roles[0]
      } catch (error) {
        console.error("Please login to proceed")
      }
      this.isActive = false
    },
    async handleLogin() {
      this.isActive = true
      try {
        const response = await axios.post('http://localhost:5000/login?include_auth_token', {
          email: this.email,
          password: this.password,
        });


        const authToken = response.data.response.user.authentication_token
        localStorage.setItem('auth_token', authToken)
        await this.fetchCurrentUserRole(authToken)
        this.$store.dispatch('fetchUser')
        this.isActive = false
        if (this.role == 'admin') {
          localStorage.setItem('role', 'admin')
          this.$router.push('/admin')
        } else {
          localStorage.setItem('role', 'user')
          this.$router.push('/user')
        }
      } catch (error) {
        this.isActive = false
        alert(`Invalid credentials. Please try again. ${error.response?.data?.message || error.message}`);
      }
    },
  },
  async mounted() {
    this.isActive = true
    if (localStorage.getItem('auth_token')) {
      await this.fetchCurrentUserRole(localStorage.getItem('auth_token'))
      this.isActive = false
      if (this.role == 'admin') {
        this.$router.push('/admin')
      } else {
        this.$router.push('/user')
      }
    }
    this.isActive = false

  }
}
</script>

<style scoped>
.card {
  max-width: 25em;
}

.text-danger:hover {
  text-decoration: underline;
}
</style>
