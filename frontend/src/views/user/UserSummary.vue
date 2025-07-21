<template>
  <div class="container mt-4">
    <h2 class="mb-4 text-center">Quiz Summary</h2>
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-if="!loading && error" class="alert alert-danger">{{ error }}</div>
    <div v-if="!loading && !error && userAttempts.length > 0" class="row">
      <div class="col-md-6 mb-4">
        <div class="card-themed shadow-sm p-3">
          <h4 class="text-center text-dark my-2">Subject-wise Quizzes Attempted</h4>
          <Bar :data="subjectChartData" :options="chartOptions" />
        </div>
      </div>
      <div class="col-md-6 mb-4">
        <div class="card-themed shadow-sm p-3">
          <h4 class="text-center text-dark my-2">Month-wise Quizzes Attempted</h4>
          <Pie :data="monthChartData" :options="chartOptions" />
        </div>
      </div>
    </div>
    <div v-if="!loading && !error && userAttempts.length === 0" class="text-center p-4 card-themed shadow-sm">
      <p>You haven't attempted any quizzes yet. Go ahead and take a quiz to see your summary here!</p>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { Bar, Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

export default {
  name: 'UserSummary',
  components: {
    Bar,
    Pie,
  },
  data() {
    return {
      loading: true,
      error: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: false,
          },
        },
      },
    };
  },
  computed: {
    ...mapGetters(['getUser', 'getUserAttempts']),
    userAttempts() {
      return this.getUserAttempts || [];
    },
    subjectChartData() {
      const subjectCounts = this.userAttempts.reduce((acc, attempt) => {
        const subject = attempt.quiz_subject || 'Uncategorized';
        acc[subject] = (acc[subject] || 0) + 1;
        return acc;
      }, {});

      const labels = Object.keys(subjectCounts);
      const data = Object.values(subjectCounts);

      return {
        labels,
        datasets: [
          {
            label: 'Quizzes Attempted',
            backgroundColor: ['#42A5F5', '#66BB6A', '#FFA726', '#26A69A', '#AB47BC', '#EC407A'],
            data,
          },
        ],
      };
    },
    monthChartData() {
      const monthCounts = this.userAttempts.reduce((acc, attempt) => {
        const month = new Date(attempt.timestamp).toLocaleString('default', { month: 'long' });
        acc[month] = (acc[month] || 0) + 1;
        return acc;
      }, {});

      const labels = Object.keys(monthCounts);
      const data = Object.values(monthCounts);

      return {
        labels,
        datasets: [
          {
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
            data,
          },
        ],
      };
    },
  },
  methods: {
    ...mapActions(['fetchUserAttempts']),
    async loadSummaryData() {
      this.loading = true;
      this.error = null;
      try {
        if (this.getUser && this.getUser.id) {
          await this.fetchUserAttempts(this.getUser.id);
        } else {
          this.error = "Could not identify user. Please log in again.";
        }
      } catch (err) {
        this.error = 'Failed to load summary data. Please try again later.';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.loadSummaryData();
  },
};
</script>

<style scoped>
.card-themed {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
  border-radius: 1rem;
  color: #333;
}
</style>
