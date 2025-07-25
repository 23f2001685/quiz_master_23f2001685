<template>
    <div class="card p-3 mt-4 mx-auto">
        <div class="container">
            <h2 class="mb-4 text-center">Register</h2>
            <form @submit.prevent="register" class="mx-auto" style="max-width: 500px;">
                <div class="mb-3">
                    <label for="email" class="form-label">Email:</label>
                    <input type="email" v-model="getNewUser.email" id="email" class="form-control" required />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password:</label>
                    <input type="password" v-model="getNewUser.password" id="password" class="form-control" required />
                </div>
                <div class="mb-3">
                    <label for="full_name" class="form-label">Full Name:</label>
                    <input type="text" v-model="getNewUser.full_name" id="full_name" class="form-control" required />
                </div>
                <div class="mb-3">
                    <label for="qualification" class="form-label">Qualification:</label>
                    <input type="text" v-model="getNewUser.qualification" id="qualification" class="form-control" />
                </div>
                <div class="mb-3">
                    <label for="dob" class="form-label">Date of Birth:</label>
                    <input type="date" v-model="getNewUser.dob" id="dob" class="form-control" />
                </div>
                <button type="submit" class="btn btn-primary">Register</button>
            </form>
        </div>
        <div class="text-center mt-3">
            <p>Already have an account? <router-link to="/login" class="text-primary">Login here</router-link></p>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
    name: 'Register',
    computed: {
        ...mapGetters(['getError', 'getNewUser']),
    },
    methods: {
        ...mapActions(['register']),
    },
};
</script>

<style scoped>
.form-control {
    border-radius: 5px;
}

.card {
  max-width: 25em;
}

.btn-primary {
    width: 100%;
}
</style>
