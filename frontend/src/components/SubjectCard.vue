<template>
  <div class="card shadow-lg mb-4">
    <div class="card-header text-center bg-secondary text-white">
      <i class="bi bi-pencil-fill text-warning fs-4" @click="editSubject"></i>
      <h5 class="mb-0">{{ subject.name }} - {{ subject.description }}</h5>
      <i class="bi bi-trash3-fill text-danger fs-4" @click="deleteSubject"></i>
    </div>
    <div class="card-body">
      <Spinner :active="isLoading" />
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Chapter Name</th>
            <th>Description</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="chapter in chapters" :key="chapter.id">
            <td>{{ chapter.name }}</td>
            <td>{{ chapter.description }}</td>
            <td>
              <button class="btn btn-sm btn-warning me-2" @click="editChapter(chapter)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteChapter(chapter)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <button class="btn btn-outline-primary w-100 mt-3" @click="openModal">+ Chapter</button>
    </div>
  </div>
  <ModalComponent v-if="isModalVisible" :title="modalTitle" :isVisible="isModalVisible" @save="saveChapter"
    @cancel="closeModal" class="modal">
    <form @submit.prevent="">
      <div class="mb-3">
        <label for="name" class="form-label">Name:</label>
        <input type="text" v-model="newChapter.name" id="name" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="description" class="form-label">Description:</label>
        <textarea v-model="newChapter.description" id="description" rows="3" class="form-control"></textarea>
      </div>
    </form>
  </ModalComponent>
</template>

<script>
import axios from "axios";
import ModalComponent from "./ModalComponent.vue";
import Spinner from "./Spinner.vue"
export default {
  name: 'SubjectCard',
  props: ['subject'],
  components: { ModalComponent, Spinner },
  emits: ['edit-subject', 'delete-subject'],
  data() {
    return {
      chapters: [],
      isLoading: true,
      isModalVisible: false,
      newChapter: { name: "", description: "", subject_id: this.subject.id },
      id: null,
      modalTitle: "New Chapter"
    }
  },
  methods: {
    openModal() {
      this.isModalVisible = true

    },
    closeModal() {
      this.isModalVisible = false
      this.modalTitle = "New Chapter"
      this.newChapter = { name: "", description: "", subject_id: this.subject.id }
    },
    async saveChapter() {
      this.isLoading = true
      if (this.id !== null) {
        await axios.put(`http://localhost:5000/api/subjects/${this.subject.id}/chapters/${this.id}`, {
          "name": this.newChapter.name,
          "description": this.newChapter.description,
        }, {
          headers: {
            "Authentication-Token": localStorage.getItem('auth_token')
          }
        })
          .then(res => {
            this.newChapter = { name: "", description: "" }
            this.isModalVisible = false
            this.fetchChapters()
          })
          .catch(err => {
            console.error("Cannot edit chapter", err);
          })
      } else {
        try {
          const res = await axios.post(`http://localhost:5000/api/subjects/${this.subject.id}/chapters`, {
            "name": this.newChapter.name,
            "description": this.newChapter.description,
          }, {
            headers: {
              "Authentication-Token": localStorage.getItem('auth_token')
            }
          })
          this.newChapter = { name: "", description: "" }
          this.isModalVisible = false
          this.fetchChapters()
        } catch (err) {
          console.error("Cannot add chapter", err);
        }
      }
      this.isLoading = false
      this.modalTitle = "New Chapter"
    },
    async fetchChapters() {
      await axios.get(`http://localhost:5000/api/subjects/${this.subject.id}/chapters`, {
        headers: {
          'Authentication-Token': localStorage.getItem('auth_token')
        }
      })
        .then(res => {
          this.chapters = res.data
          this.isLoading = false
        })
        .catch(err => {
          console.error(err);
          this.isLoading = false
        })
    },
    editChapter(chapter) {
      this.newChapter = chapter
      this.id = chapter.id
      this.openModal()
      this.modalTitle = "Edit Chapter"

    },
    async deleteChapter(chapter) {
      await axios.delete(`http://localhost:5000/api/subjects/${this.subject.id}/chapters/${chapter.id}`, {
        headers: {
          "Authentication-Token": localStorage.getItem('auth_token')
        }
      })
        .then(res => {
          this.fetchChapters()
        })
        .catch(err => {
          console.error(err);

        })
    },
    editSubject() {
      this.$emit('edit-subject')
    },
    deleteSubject() {
      this.$emit('delete-subject')
    }
  },
  mounted() {
    this.fetchChapters()
  }
};
</script>

<style scoped>
.card-header {
  border-radius: 0.375rem;
  display: flex;
  justify-content: space-between;
}

.modal {
  z-index: 99;
}
</style>
