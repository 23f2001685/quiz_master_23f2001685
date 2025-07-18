<template>
  <div class="container mt-4">
    <h2 class="text-center mb-4  fw-bold">My Quiz Scores</h2>

    <div v-if="isLoading" class="text-center">
      <Spinner :active="true" />
      <p class="mt-3 text-black">Loading scores...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="attempts.length === 0" class="border-light card-themed text-center p-5">
      <h4 class="text-black">No Quiz Attempts Found</h4>
      <p class="text-black-50">You haven't attempted any quizzes yet. Go to the dashboard to start one!</p>
      <router-link to="/user" class="btn btn-primary mt-3">Go to Dashboard</router-link>
    </div>

    <div v-else class="card-themed">
      <div class="table-responsive">
        <table class="table  table-hover align-middle text-center">
          <thead>
            <tr>
              <th>Quiz Title</th>
              <th>Date Attempted</th>
              <th>Score</th>
              <th>Percentage</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="attempt in attempts" :key="attempt.id" class="table-row-item">
              <td>{{ attempt.quiz_title || 'N/A' }}</td>
              <td>{{ formatDate(attempt.timestamp) }}</td>
              <td>{{ attempt.total_score }} / {{ attempt.max_score }}</td>
              <td>
                {{ attempt.percentage.toFixed(2) }}%
                <div class="progress" style="height: 3px; background-color: rgba(0,0,0,0.2);">
                  <div
                    :class="getProgressBarClass(attempt.percentage)"
                    role="progressbar"
                    :style="{ width: attempt.percentage + '%' }"
                    :aria-valuenow="attempt.percentage"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  >
                  </div>
                </div>
              </td>
              <td>
                <span :class="getResultBadgeClass(attempt.percentage)">
                  {{ getResultText(attempt.percentage) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Controls -->
      <div v-if="pagination.pages > 1" class="d-flex justify-content-center align-items-center p-1">
        <button
          class="btn btn-outline-dark me-2"
          @click="fetchAttempts(pagination.page - 1)"
          :disabled="!pagination.has_prev"
        >
          &laquo; Previous
        </button>
        <span class="text-dark">
          Page {{ pagination.page }} of {{ pagination.pages }}
        </span>
        <button
          class="btn btn-outline-dark ms-2"
          @click="fetchAttempts(pagination.page + 1)"
          :disabled="!pagination.has_next"
        >
          Next &raquo;
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Spinner from '../../components/Spinner.vue';

export default {
  name: 'Scores',
  components: {
    Spinner,
  },
  data() {
    return {
      attempts: [],
      isLoading: true,
      error: null,
      pagination: {
        page: 1,
        per_page: 10,
        total: 0,
        pages: 0,
        has_next: false,
        has_prev: false,
      },
    };
  },
  methods: {
    async fetchAttempts(page = 1) {
      this.isLoading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) {
          this.$router.push('/login');
          return;
        }

        const response = await axios.get('http://localhost:5000/api/quiz-attempts', {
          headers: {
            'Authentication-Token': token,
          },
          params: {
            page: page,
            per_page: this.pagination.per_page,
          },
        });

        this.attempts = response.data.attempts;
        this.pagination = response.data.pagination;
      } catch (err) {
        this.error = err.response?.data?.message || 'An error occurred while fetching your scores.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      const date = new Date(dateStr);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    },
    getProgressBarClass(percentage) {
      if (percentage >= 75) return 'progress-bar bg-success';
      if (percentage >= 50) return 'progress-bar bg-warning';
      return 'progress-bar bg-danger';
    },
    getResultBadgeClass(percentage) {
      if (percentage >= 50) return 'badge bg-success-light';
      return 'badge bg-danger-light';
    },
    getResultText(percentage) {
      return percentage >= 50 ? 'Pass' : 'Fail';
    },
  },
  mounted() {
    this.fetchAttempts();
  },
};
</script>

<style scoped>
.card-themed {
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

.table-row-item:hover {
  background-color: rgba(84, 84, 84, 0.093);
}

.progress-bar {
  font-weight: 600;
  color: #212529;
}

.badge {
  padding: 0.5em 0.9em;
  font-size: 0.9rem;
  font-weight: 600;
}

.bg-success-light {
  background-color: rgba(40, 167, 69, 0.7);
  color: white;
}

.bg-danger-light {
  background-color: rgba(220, 53, 69, 0.7);
  color: white;
}
</style>
