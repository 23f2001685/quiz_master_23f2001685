<template>
  <div class="container mt-4">
    <div
      :class="['d-flex', 'justify-content-between', 'align-items-center', 'mb-4', { 'blurred': isQuizModalVisible }]">
      <h2 class="mb-4">User Dashboard</h2>
    </div>
    <Toast ref="toastRef" />
    <strong v-if="isSearching" class="text-center text-muted">Searching...</strong>
    <div :class="['card-themed', 'mx-auto', 'shadow-sm', { 'blurred': isQuizModalVisible }]">
      <div class="table-responsive" v-if="activeQuizzes.length !== 0">
        <h4 class="text-center text-dark my-4">Active Quizzes</h4>
        <table class="table table-bordered align-middle text-center">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title - Chapter</th>
              <th>End Time</th>
              <th>Time Remaining</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in activeQuizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td>{{ quiz.title }} - {{ quiz.chapter }}</td>
              <td>{{ formatEndTime(quiz.date_of_quiz, quiz.time_duration) }}</td>
              <td>{{ getTimeRemaining(quiz.date_of_quiz, quiz.time_duration) }}</td>
              <td>
                <button class="btn btn-info btn-sm me-2" @click="openQuizModal(quiz)">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="!isSearching" class="text-center p-4">No quizzes are currently active.</div>
    </div>
    <div :class="['card-themed', 'mx-auto', 'shadow-sm', { 'blurred': isQuizModalVisible }]">
      <div class="table-responsive" v-if="upcomingQuizzes.length !== 0">
        <h4 class="text-center text-dark my-4">Upcoming Quizzes</h4>
        <table class="table table-bordered align-middle text-center">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title - Chapter</th>
              <th>Starts At</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in upcomingQuizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td>{{ quiz.title }} - {{ quiz.chapter }}</td>
              <td>{{ formatDate(quiz.date_of_quiz) }}</td>
              <td>
                <span class="badge text-bg-info">upcoming</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="pastQuizzes && pastQuizzes.length" :class="['card-themed', 'mx-auto', 'shadow-sm', { 'blurred': isQuizModalVisible }]">
      <h4 class="text-center text-dark my-4">Past Quizzes</h4>
      <div class="table-responsive">
        <table class="table table-bordered align-middle text-center">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title - Chapter</th>
              <th>Date | Time</th>
              <th>Duration (hh:mm)</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in pastQuizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td>{{ quiz.title }} - {{ quiz.chapter }}</td>
              <td>{{ formatDate(quiz.date_of_quiz) }}</td>
              <td>{{ formatDuration(quiz.time_duration) }}</td>
              <td>
                <span class="badge text-bg-danger">Time Out</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- No Results Message -->
    <div v-if="isSearching && noResults" class="card-themed text-center p-5 mt-4">
      <h4 class="text-dark">No Quizzes Found</h4>
      <p class="text-dark-50">No quizzes match your search for "{{ getSearchQuery }}".</p>
      <button class="btn btn-primary mt-3" @click="clearSearch">Clear Search</button>
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
            <p v-if="!selectedQuiz.is_active" class="fw-bold text-danger text-center fs-5">The quiz has been deactivated</p>
          </div>
          <div class="modal-footer d-flex justify-content-around align-items-center">

            <button v-if="selectedQuiz.questions.length !== 0 && selectedQuiz.is_active" class="btn btn-success px-3" @click="startQuiz(selectedQuiz)">Start</button>
            <button class="btn btn-secondary px-3" @click="closeQuizModal">Close</button>
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
      currentTime: new Date(),
      timerId: null,
    };
  },
  computed: {
    ...mapGetters([
      'getUser',
      'getQuizzes',
      'getQuiz',
      'getSearchQuery',
    ]),
    isSearching() {
      return this.getSearchQuery && this.getSearchQuery.trim() !== '';
    },
    noResults() {
      return this.activeQuizzes.length === 0 && this.upcomingQuizzes.length === 0 && this.pastQuizzes.length === 0;
    },
    filteredQuizzes() {
      if (!this.isSearching) {
        return this.getQuizzes || [];
      }
      const query = this.getSearchQuery.toLowerCase().trim();
      return (this.getQuizzes || []).filter(quiz => {
        const titleMatch = quiz.title && quiz.title.toLowerCase().includes(query);
        const subjectMatch = quiz.subject && quiz.subject.toLowerCase().includes(query);
        const chapterMatch = quiz.chapter && quiz.chapter.toLowerCase().includes(query);
        return titleMatch || subjectMatch || chapterMatch;
      });
    },
    upcomingQuizzes() {
      return this.filteredQuizzes.filter(quiz => {
        const startTime = new Date(quiz.date_of_quiz);
        if (isNaN(startTime.getTime())) return false;
        return this.currentTime < startTime;
      });
    },
    activeQuizzes() {
      return this.filteredQuizzes.filter(quiz => {
        const startTime = new Date(quiz.date_of_quiz);
        const durationInMinutes = parseInt(quiz.time_duration, 10);

        if (isNaN(startTime.getTime()) || isNaN(durationInMinutes)) {
          return false;
        }

        const endTime = new Date(startTime.getTime() + durationInMinutes * 60 * 1000);
        return this.currentTime >= startTime && this.currentTime <= endTime;
      });
    },
    pastQuizzes() {
      return this.filteredQuizzes.filter(quiz => {
        const startTime = new Date(quiz.date_of_quiz);
        const durationInMinutes = parseInt(quiz.time_duration, 10);

        if (isNaN(startTime.getTime()) || isNaN(durationInMinutes)) {
          return false;
        }

        const endTime = new Date(startTime.getTime() + durationInMinutes * 60 * 1000);
        return this.currentTime > endTime;
      });
    },
  },
  methods: {
    ...mapActions(['fetchQuizzes', 'performSearch']),
    showToast() {
      this.$refs.toastRef.showToast('Hello', 'This is a toast message from User Dashboard!');
    },
    clearSearch() {
      this.performSearch('');
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
    formatEndTime(startTimeStr, duration) {
      const startTime = new Date(startTimeStr);
      const durationInMinutes = parseInt(duration, 10);
      if (isNaN(startTime.getTime()) || isNaN(durationInMinutes)) return 'N/A';

      const endTime = new Date(startTime.getTime() + durationInMinutes * 60 * 1000);
      return endTime.toLocaleTimeString(undefined, {
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    getTimeRemaining(startTimeStr, duration) {
      const startTime = new Date(startTimeStr);
      const durationInMinutes = parseInt(duration, 10);
      if (isNaN(startTime.getTime()) || isNaN(durationInMinutes)) return 'N/A';

      const endTime = new Date(startTime.getTime() + durationInMinutes * 60 * 1000);
      const remainingMs = endTime - this.currentTime;

      if (remainingMs <= 0) return 'Finished';

      const hours = Math.floor(remainingMs / (1000 * 60 * 60));
      const minutes = Math.floor((remainingMs % (1000 * 60 * 60)) / (1000 * 60));

      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')} left`;
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
      this.$router.push(`/quiz/${quiz.id}`);

    }
  },
  async mounted() {
    this.fetchQuizzes();
    // Update the current time every second to keep the list and time remaining reactive
    this.timerId = setInterval(() => {
      this.currentTime = new Date();
    }, 1000);
  },
  beforeUnmount() {
    if (this.timerId) {
      clearInterval(this.timerId);
    }
    this.clearSearch();
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

.btn-info:hover {
    background-color: rgba(23, 162, 184, 1);
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
.translucent-card {
  background: rgba(255, 255, 255, 0.6) !important;
  backdrop-filter: blur(5px);
  border-radius: 1rem;
  box-shadow: 0 16px 32px 0 rgba(31, 38, 135, 0.2);
}
</style>
