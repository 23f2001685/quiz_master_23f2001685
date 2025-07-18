<template>
  <div class="container">
    <div class="row d-flex justify-content-between align-items-center">


      <!-- Quiz Header -->
      <div class="card quiz-container shadow-lg col-lg me-2">
        <div class="quiz-header d-flex justify-content-between align-items-center p-3">
          <div class="quiz-info d-flex align-items-center">
            <span class="quiz-number">Q.No.</span>
            <span class="question-counter">{{ currentQuestionIndex + 1 }}/{{ totalQuestions }}</span>
          </div>
          <div class="timer">
            <span class="time-display">{{ formatTime(timeRemaining) }}</span>
          </div>
        </div>

        <!-- Question Content -->
        <div class="question-section p-4" v-if="currentQuestion">
          <div class="question-statement-box p-4 mb-4">
            <h4 class="question-text">{{ currentQuestion.question_statement }}</h4>
          </div>

          <!-- Options -->
          <div class="options-container">
            <div
              v-for="(option, index) in options"
              :key="index"
              class="option-item d-flex align-items-center mb-3"
              @click="selectOption(index + 1)"
            >
              <span class="option-number me-3">{{ index + 1 }})</span>
              <span class="option-text flex-grow-1">{{ option }}</span>
              <div class="option-radio">
                <input
                  type="radio"
                  :name="'question-' + currentQuestion.id"
                  :value="index + 1"
                  v-model="selectedAnswer"
                  class="form-check-input"
                />
              </div>
            </div>
          </div>

          <!-- Navigation Buttons -->
          <div class="navigation-buttons d-flex justify-content-center gap-3 mt-4">
            <button
              class="btn btn-primary nav-btn"
              @click="saveAndNext"
              :disabled="currentQuestionIndex >= totalQuestions - 1"
            >
              Save and Next
            </button>
            <button
              class="btn btn-success nav-btn"
              @click="submitQuiz"
            >
              Submit
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-else class="text-center p-5">
          <Spinner :active="true" />
          <p class="mt-3">Loading quiz...</p>
        </div>
      </div>

      <!-- Quiz Navigation Panel -->
      <div class="card question-nav-panel shadow-lg col-lg-2 mt-2 mt-xl-0">
        <h6 class="mb-0 card-header">Question Navigation</h6>
        <div class="card-body">
          <div class="question-grid">
            <button
              v-for="(question, index) in quizQuestions"
              :key="question.id"
              @click="goToQuestion(index)"
              :class="[
                'btn btn-sm question-nav-btn',
                {
                  'btn-success': answers[question.id],
                  'btn-warning': currentQuestionIndex === index,
                  'btn-outline-secondary': !answers[question.id] && currentQuestionIndex !== index
                }
              ]"
            >
              {{ index + 1 }}
            </button>

          </div>
        </div>
      </div>
    </div>
    <!-- Submit Confirmation Modal -->
    <ModalComponent
      v-if="showSubmitModal"
      title="Submit Quiz"
      :isVisible="showSubmitModal"
      @save="confirmSubmit"
      @cancel="closeSubmitModal"
    >
      <div class="text-center">
        <p>Are you sure you want to submit the quiz?</p>
        <p class="text-muted">You have answered {{ answeredCount }} out of {{ totalQuestions }} questions.</p>
        <p class="text-warning" v-if="answeredCount < totalQuestions">
          {{ totalQuestions - answeredCount }} questions are still unanswered.
        </p>
      </div>
    </ModalComponent>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import ModalComponent from '../../components/ModalComponent.vue';
import Spinner from '../../components/Spinner.vue';
import axios from 'axios';

export default {
  name: 'Quiz',
  components: {
    ModalComponent,
    Spinner
  },
  data() {
    return {
      currentQuestionIndex: 0,
      selectedAnswer: null,
      answers: {},
      timeRemaining: 0,
      timer: null,
      showSubmitModal: false,
      quizId: null,
      quizQuestions: [],
      currentQuiz: null,
      correctAnswers: 0 // To track correct answers if needed
    };
  },
  computed: {
    ...mapGetters(['getQuizzes', 'getUser']),
    currentQuestion() {
      return this.quizQuestions[this.currentQuestionIndex] || null;
    },
    totalQuestions() {
      return this.quizQuestions.length;
    },
    options() {
      if (!this.currentQuestion) return [];
      return [
        this.currentQuestion.option1,
        this.currentQuestion.option2,
        this.currentQuestion.option3,
        this.currentQuestion.option4
      ];
    },
    answeredCount() {
      return Object.keys(this.answers).length;
    }
  },
  methods: {
    ...mapActions(['fetchQuizzes']),

    initializeQuiz() {
      // Get quiz ID from route params or localStorage
      this.quizId = this.$route.params.quizId || localStorage.getItem('currentQuizId');

      if (!this.quizId) {
        this.$router.push('/');
        return;
      }

      // Find the quiz from the store
      const quiz = this.getQuizzes.find(q => q.id == this.quizId);
      if (quiz && quiz.questions) {
        this.currentQuiz = quiz;
        this.quizQuestions = quiz.questions;
        this.timeRemaining = quiz.time_duration * 60; // Convert minutes to seconds
        this.startTimer();
      } else {
        // Fetch quiz data if not available
        this.fetchQuizData();
      }
    },

    async fetchQuizData() {
      try {
        // This would typically fetch quiz data from the API
        await this.fetchQuizzes();
        const quiz = this.getQuizzes.find(q => q.id == this.quizId);
        if (quiz) {
          this.currentQuiz = quiz;
          this.quizQuestions = quiz.questions || [];
          this.timeRemaining = quiz.time_duration * 60;
          this.startTimer();
        }
      } catch (error) {
        console.error('Error fetching quiz data:', error);
        this.$router.push('/');
      }
    },

    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeRemaining > 0) {
          this.timeRemaining--;
        } else {
          this.timeUp();
        }
      }, 1000);
    },

    formatTime(seconds) {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = seconds % 60;
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },

    selectOption(optionNumber) {
      this.selectedAnswer = optionNumber;
    },

    saveAndNext() {
      if (this.selectedAnswer) {
        this.answers[this.currentQuestion.id] = this.selectedAnswer;
      }

      if (this.currentQuestionIndex < this.totalQuestions - 1) {
        this.currentQuestionIndex++;
        this.loadCurrentQuestion();
      }
    },

    goToQuestion(index) {
      // Save current answer before navigating
      if (this.selectedAnswer) {
        this.answers[this.currentQuestion.id] = this.selectedAnswer;
      }

      this.currentQuestionIndex = index;
      this.loadCurrentQuestion();
    },

    loadCurrentQuestion() {
      // Load saved answer for current question
      const savedAnswer = this.answers[this.currentQuestion.id];
      this.selectedAnswer = savedAnswer || null;
    },

    submitQuiz() {
      // Save current answer before submitting
      if (this.selectedAnswer) {
        this.answers[this.currentQuestion.id] = this.selectedAnswer;
      }

      this.showSubmitModal = true;
    },

    closeSubmitModal() {
      this.showSubmitModal = false;
    },

    async confirmSubmit() {
      try {
        // Stop the timer
        if (this.timer) {
          clearInterval(this.timer);
        }

        const submission = {
          quiz_id: this.quizId,
          answers: this.answers, // Send answers like { question_id: selected_option }
        };

        const token = localStorage.getItem('auth_token');

        // POST the submission to the backend API
        const response = await axios.post('http://localhost:5000/api/quiz-attempts', submission, {
          headers: {
            'Authentication-Token': token,
          },
        });

        // Show a success message with the score calculated by the server
        const result = response.data.attempt;
        alert(`Quiz submitted successfully! Your score: ${result.total_score}/${result.max_score} (${result.percentage.toFixed(2)}%)`);

        this.$router.push('/scores');

      } catch (error) {
        console.error('Error submitting quiz:', error);
        const errorMessage = error.response?.data?.message || 'Error submitting quiz. Please try again.';
        alert(errorMessage);
      }

      this.closeSubmitModal();
    },

    timeUp() {
      alert('Time is up! The quiz will be submitted automatically.');
      this.confirmSubmit();
    }
  },

  mounted() {
    this.initializeQuiz();
  },

  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
};
</script>

<style scoped>
.quiz-container {
  background: rgba(181, 177, 177, 0.35);
  box-shadow: 0 8px 32px 0 rgba(18, 19, 32, 0.557);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.509);
}

.quiz-header {
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px 10px 0 0;
}

.quiz-number {
  font-size: 1.2rem;
  font-weight: 600;
  margin-right: 0.5rem;
  color: #333;
}

.question-counter {
  background: #28a745;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 1rem;
}

.timer {
  background: rgba(135, 206, 235, 0.8);
  padding: 0.5rem 1.5rem;
  border-radius: 25px;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.time-display {
  font-family: 'Courier New', monospace;
  font-size: 1.2rem;
  font-weight: bold;
  color: #000;
}

.question-statement-box {
  background: rgba(135, 206, 235, 0.3);
  border: 2px solid rgba(135, 206, 235, 0.5);
  border-radius: 15px;
  backdrop-filter: blur(5px);
}

.question-text {
  color: #333;
  font-weight: 600;
  margin: 0;
  line-height: 1.6;
}

.option-item {
  background: rgba(255, 255, 255, 0.2);
  padding: 1rem;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-item:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateX(5px);
}

.option-number {
  font-weight: 600;
  font-size: 1.1rem;
  color: #333;
  min-width: 30px;
}

.option-text {
  color: #333;
  font-size: 1rem;
}

.option-radio input[type="radio"] {
  width: 20px;
  height: 20px;
  accent-color: #007bff;
}

.nav-btn {
  padding: 0.75rem 2rem;
  font-weight: 600;
  border-radius: 25px;
  transition: all 0.3s ease;
  min-width: 140px;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.question-nav-panel {
  background: rgba(181, 177, 177, 0.35);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.509);
  height: 600px;
  overflow-y: auto;
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
  gap: 0.5rem;
}

.question-nav-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-weight: 600;
  transition: all 0.2s ease;
}

.question-nav-btn:hover {
  transform: scale(1.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .quiz-header {
    flex-direction: column;
    gap: 1rem;
  }

  .navigation-buttons {
    flex-direction: column;
  }

  .nav-btn {
    width: 100%;
  }

  .question-grid {
    grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  }

  .question-nav-btn {
    width: 40px;
    height: 40px;
  }
}

/* Custom animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.question-section {
  animation: fadeIn 0.5s ease;
}
</style>
