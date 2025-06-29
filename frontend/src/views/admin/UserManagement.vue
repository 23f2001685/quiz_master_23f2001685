<template>
  <div class="container mt-4">
    <h2 class="mb-4">User Management</h2>

    <div class="row mt-4" v-if="users && users.length">
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Users List</h5>
          </div>
          <div class="card-body">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Full Name</th>
                  <th>Email</th>
                  <th>Qualification</th>
                  <th>Date of Birth</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.full_name }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.qualification || 'N/A' }}</td>
                  <td>{{ user.dob || 'N/A' }}</td>
                  <td>
                    <span :class="user.active ? 'badge bg-success' : 'badge bg-danger'">
                      {{ user.active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-sm " :class="user.active ? 'btn-danger' : 'btn-success'" @click="disableUser(user)">
                      {{ user.active ? 'Deactivate' : 'Activate' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="isLoading" class="text-center">
      Loading users...
    </div>
    <div v-else class="text-center text-muted">
      No users found.
    </div>

    <Spinner :active="isLoading"></Spinner>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import Spinner from '../../components/Spinner.vue';

export default {
  name: 'UserManagement',
  components: { Spinner },
  computed: {
    ...mapGetters(['users', 'isLoading']),
  },
  methods: {
    ...mapActions(['fetchUsers', 'deactivateUser']),
    async disableUser(user) {
      if (confirm(`Are you sure you want to ${user.active ? "deactivate" : "activate" } user: "${user.full_name}" (${user.email})?`)) {
        try {
          await this.deactivateUser(user.id);
          alert(`User ${user.active ? "deactivated" : "activated" } successfully!`);
        } catch (error) {
          alert('Failed to activate/deactivate user: ' + (error.response?.data?.message || error.message));
        }
      }
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
.table th,
.table td {
  text-align: center;
  vertical-align: middle;
}

.card-body {
  padding: 1.5rem;
}

.badge {
  font-size: 0.9rem;
}
</style>
