<template>
  <div class="container mt-4">
    <h2 class="mb-4 text-center">Admin Summary</h2>
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-if="!loading && error" class="alert alert-danger">{{ error }}</div>
    <div v-if="!loading && !error" class="row">
      <div class="col-md-6 mb-4">
        <div class="card-themed shadow-sm p-3">
          <h4 class="text-center text-dark my-2">Subject-wise Top Scores</h4>
          <div style="height: 400px;">
            <Bar :data="topScoresChartData" :options="barChartOptions" />
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-4">
        <div class="card-themed shadow-sm p-3">
          <h4 class="text-center text-dark my-2">Subject-wise User Attempts</h4>
          <div style="height: 400px;">
            <Doughnut :data="attemptsChartData" :options="doughnutChartOptions" />
          </div>
        </div>
      </div>
    </div>
    <div v-if="!loading && !error && (!statsData || (!statsData.subject_top_scores && !statsData.subject_attempts))" class="text-center p-4 card-themed shadow-sm">
      <p>No data available yet. Data will appear once users start taking quizzes!</p>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { Bar, Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';
import axios from 'axios';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

export default {
  name: 'AdminSummary',
  components: {
    Bar,
    Doughnut,
  },
  data() {
    return {
      loading: true,
      error: null,
      statsData: null,
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
              display: false,
          },
          title: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              stepSize: 10,
              callback: function(value) {
                return value + '%';
              }
            }
          }
        }
      },
      doughnutChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
          title: {
            display: false,
          },
        },
      },
    };
  },
  computed: {
    ...mapGetters(['getUser']),
    topScoresChartData() {
      if (!this.statsData || !this.statsData.subject_top_scores) {
        return { labels: [], datasets: [] };
      }

      const subjectScores = this.statsData.subject_top_scores;
      const labels = Object.keys(subjectScores);
      const data = Object.values(subjectScores);

      return {
        labels,
        datasets: [
          {
            label: 'Top Score (%)',
            backgroundColor: ['#87CEEB', '#DC143C', '#32CD32', '#FFD700', '#FFA07A'],
            data,
          },
        ],
      };
    },
    attemptsChartData() {
      if (!this.statsData || !this.statsData.subject_attempts) {
        return { labels: [], datasets: [] };
      }

      const subjectAttempts = this.statsData.subject_attempts;
      const labels = Object.keys(subjectAttempts);
      const data = Object.values(subjectAttempts);

      return {
        labels,
        datasets: [
          {
            backgroundColor: ['#32CD32', '#4169E1', '#DC143C', '#FFD700', '#FF69B4'],
            data,
          },
        ],
      };
    },
  },
  methods: {
    ...mapActions([]),
    async loadAdminSummaryData() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get('http://localhost:5000/api/quiz-attempts/stats', {
          headers: {
            'Authentication-Token': localStorage.getItem('auth_token')
          }
        });

        if (response.data) {
          this.statsData = response.data;

        }

      } catch (err) {
        this.error = 'Failed to load admin summary data. Please try again later.';
        console.error('Admin summary error:', err);
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    this.loadAdminSummaryData();
  },
};
</script>

<style scoped>
 /* {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
  border-radius: 1rem;
  color: #333;
} */

.card-themed {
  background: rgba(181, 177, 177, 0.35);
  box-shadow: 0 8px 32px 0 rgba(18, 19, 32, 0.557);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.509);
}
</style>
