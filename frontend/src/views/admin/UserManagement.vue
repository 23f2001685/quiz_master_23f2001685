<template>
  <div class="container mt-4">
    <h2 class="mb-4">User Management</h2>

    <div class="row mt-4" v-if="users && users.length">
      <p v-if="isSearching"><strong class="text-muted">Search Results for : </strong>"{{ getSearchQuery }}"</p>
      <div class="themed-card shadow-sm">
          <table class="table table-striped table-hover">
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
              <tr v-for="user in filteredUsers" :key="user.id">
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
          <div v-if="isSearching && !filteredUsers.length" class="text-center p-4">
            <p class="text-muted">No users found for "{{ getSearchQuery }}"</p>
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
    ...mapGetters(['users', 'isLoading', 'getSearchQuery']),
    isSearching() {
      return this.getSearchQuery && this.getSearchQuery.trim() !== '';
    },
    filteredUsers() {
      if (this.isSearching) {
        const query = this.getSearchQuery.toLowerCase();
        return this.users.filter(user =>
          user.full_name.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query) ||
          user.qualification?.toLowerCase().includes(query) ||
          user.dob?.toLowerCase().includes(query)
        );
      }
      return this.users;
    }
  },
  methods: {
    ...mapActions(['fetchUsers', 'deactivateUser', 'performSearch']),
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
  beforeUnmount() {
    this.performSearch(''); // Clear search query on unmount
  }
};
</script>

<style scoped>
.themed-card {
  background: rgba(181, 177, 177, 0.35);
  box-shadow: 0 8px 32px 0 rgba(18, 19, 32, 0.557);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.509);
  color: white;
}


.table {
  color: white;
  --bs-table-bg: transparent;
  --bs-table-border-color: rgba(255, 255, 255, 0.2);
  --bs-table-hover-bg: rgba(255, 255, 255, 0.1);
  --bs-table-hover-color: white;
}

.table thead {
  color: #c7d2fe;
}

.table>thead>tr>th {
  border-bottom-width: 2px;
}

.badge {
  font-size: 0.9rem;
}
</style>
