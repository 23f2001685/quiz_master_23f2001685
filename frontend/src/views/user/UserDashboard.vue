<template>
  <div class="container mt-4">
    <div
      :class="['d-flex', 'justify-content-between', 'align-items-center', 'mb-4', { 'blurred': isQuizModalVisible }]">
      <h2 class="mb-4">User Dashboard</h2>
    </div>
    <Toast ref="toastRef" />

    <div :class="['card', 'mx-auto', 'shadow-sm', { 'blurred': isQuizModalVisible }]">
      <h4 class="text-center my-4">Upcoming Quizzes</h4>
      <div class="table-responsive" v-if="getQuizzes && getQuizzes.length">
        <table class="table table-bordered align-middle text-center">
          <thead class="table-primary">
            <tr>
              <th>ID</th>
              <th>Title - Chapter</th>
              <th>Date | Time</th>
              <th>Duration (hh:mm)</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in getQuizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td>{{ quiz.remarks }} - {{ quiz.chapter }}</td>
              <td>{{ formatDate(quiz.date_of_quiz) }}</td>
              <td>{{ formatDuration(quiz.time_duration) }}</td>
              <td>
                <button class="btn btn-info btn-sm me-2" @click="openQuizModal(quiz)">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-center">No Quizzes have been scheduled.</div>
    </div>

    <!-- Quiz Details Modal -->
    <div class="modal fade show custom-modal-bg" tabindex="-1" v-if="isQuizModalVisible">
      <div class="modal-dialog">
        <div class="modal-content translucent-card">
          <div class="modal-header">
            <h5 class="modal-title">Quiz Details</h5>
            <button type="button" class="btn-close" aria-label="Close" @click="closeQuizModal"></button>
          </div>
          <div class="modal-body">
            <p><strong>Description:</strong> {{ selectedQuiz.remarks }}</p>
            <p><strong>Chapter:</strong> {{ selectedQuiz.chapter }}</p>
            <p><strong>Date & Time:</strong> {{ formatDate(selectedQuiz.date_of_quiz) }}</p>
            <p><strong>Duration:</strong> {{ formatDuration(selectedQuiz.time_duration) }}</p>
            <p><strong>Number of Questions:</strong>
              {{ selectedQuiz.num_questions || (selectedQuiz.questions ? selectedQuiz.questions.length : 'N/A') }}
            </p>
            <!-- Add more quiz details here if available -->
          </div>
          <div class="modal-footer d-flex justify-content-between align-items-center">
            <div></div>
            <button class="btn btn-success" @click="startQuiz(selectedQuiz)">Start</button>
          </div>
        </div>
      </div>
    </div>
    <!-- End Quiz Details Modal -->
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
  data() {
    return {
      isQuizModalVisible: false,
      selectedQuiz: {},
    };
  },
  computed: {
    ...mapGetters([
      'getUser',
      'getQuizzes',
      'getQuiz',
    ])
  },
  methods: {
    ...mapActions(['fetchQuizzes']),
    showToast() {
      this.$refs.toastRef.showToast('Hello', 'This is a toast message from User Dashboard!');
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      const datePart = date.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
      const timePart = date.toLocaleTimeString(undefined, {
        hour: '2-digit',
        minute: '2-digit'
      });
      return `${datePart} | ${timePart}`;
    },
    formatDuration(duration) {
      if (!duration) return '';
      const totalMinutes = parseInt(duration, 10);
      const hours = Math.floor(totalMinutes / 60);
      const minutes = totalMinutes % 60;
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    },
    openQuizModal(quiz) {
      this.selectedQuiz = quiz;
      this.isQuizModalVisible = true;
    },
    closeQuizModal() {
      this.isQuizModalVisible = false;
      this.selectedQuiz = {};
    },
    startQuiz(quiz) {
      this.closeQuizModal();
      this.$refs.toastRef.showToast('Quiz Started', `You have started quiz: ${quiz.remarks}`);
      // Add your quiz start logic here
    }
  },
  async mounted() {
    console.log(this.fetchQuizzes());
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

.modal {
  display: block;
}

.modal.fade:not(.show) {
  opacity: 0;
}

.blurred {
  filter: blur(6px) brightness(0.8);
  pointer-events: none;
  user-select: none;
}

.custom-modal-bg {
  background: rgba(42, 75, 183, 0.501) !important;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1050;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-modal-bg .modal-dialog {
  max-width: 800px;
  width: 90vw;
}

.translucent-card {
  background: rgba(255, 255, 255, 0.6) !important;
  backdrop-filter: blur(5px);
  border-radius: 1rem;
  box-shadow: 0 16px 32px 0 rgba(31, 38, 135, 0.2);
}
</style>
