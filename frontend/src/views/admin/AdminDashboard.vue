<template>
  <div class="container mt-4">
    <div v-if="getError" class="alert alert-danger">
      {{ getError }}
    </div>
    <main class="row">
      <div class="col-md-6" v-for="subject in filteredSubjects" :key="subject.id">
        <SubjectCard
          :subject="subject"
          @edit-subject="editSubject(subject)"
          @delete-subject="delSubject(subject.id)"
        />
      </div>
      <div v-if="isSearching && !filteredSubjects.length" class="text-center p-5">
        <h4 class="text-muted">No subjects found for "{{ getSearchQuery }}"</h4>
      </div>
    </main>
    <ModalComponent
      v-if="isModalVisible"
      :title="modalAction"
      :isVisible="isModalVisible"
      @save="saveSubject"
      @cancel="closeModal"
    >
      <form @submit.prevent="">
        <div class="mb-3">
          <label for="name" class="form-label">Name:</label>
          <input
            type="text"
            v-model="newSubject.name"
            id="name"
            class="form-control"
            required
          />
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Description:</label>
          <textarea
            v-model="newSubject.description"
            id="description"
            rows="3"
            class="form-control"
          ></textarea>
        </div>
      </form>
    </ModalComponent>
    <Fab v-if="!isModalVisible" @click="openModal" toAdd="Subject" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import SubjectCard from '../../components/SubjectCard.vue';
import ModalComponent from '../../components/ModalComponent.vue';
import Fab from '../../components/Fab.vue';
import NavBar from '../../components/NavBar.vue';

export default {
  name: 'AdminDashboard',
  components: { ModalComponent, SubjectCard, Fab, NavBar },
  computed: {
    ...mapGetters([
      'getUser',
      'getError',
      'getSubjects',
      'isModalVisible',
      'modalAction',
      'newSubject',
      'getSearchQuery',
    ]),
    isSearching() {
      return this.getSearchQuery && this.getSearchQuery.trim() !== '';
    },
    filteredSubjects() {
      if (!this.isSearching) {
        return this.getSubjects;
      }
      const query = this.getSearchQuery.toLowerCase().trim();
      return this.getSubjects.filter(subject => {
        const nameMatch = subject.name.toLowerCase().includes(query);
        const descriptionMatch = subject.description.toLowerCase().includes(query);
        return nameMatch || descriptionMatch;
      });
    },
  },
  methods: {
    ...mapActions([
      'fetchSubjects',
      'openModal',
      'closeModal',
      'saveSubject',
      'editSubject',
      'deleteSubject',
      'performSearch'
    ]),
    logOut() {
      localStorage.clear();
      this.$router.push('/login');
    },
    delSubject(id) {
      if (!confirm('Are you sure you want to delete this subject?')) {
        return;
      }
      this.deleteSubject(id)
        .then(() => {
          this.$store.dispatch('fetchSubjects');
        })
        .catch((error) => {
          console.error('Error deleting subject:', error);
        });
    },
  },
  mounted() {
    this.fetchSubjects();
    this.$store.dispatch('fetchUser');
  },
  beforeUnmount() {
    this.performSearch(''); // Clear search query on unmount
  }
};
</script>

<style scoped>
header nav a:hover {
  text-decoration: underline;
}
header {
  background: rgba(181, 177, 177, 0.35);
  box-shadow: 0 8px 32px 0 rgba(18, 19, 32, 0.557);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.509) !important;
}
footer button {
  width: 50px;
  height: 50px;
}
</style>
