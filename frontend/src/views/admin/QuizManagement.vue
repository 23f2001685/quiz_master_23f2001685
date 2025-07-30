<template>
  <div class="container mt-4">

    <div class="row mt-4">
      <div class="col-md-6 mb-4" v-for="quiz in filteredQuizzes" :key="quiz.id">
        <div class="card-themed shadow-sm p-1">
          <div class="card-header p-1">
            <i class="bi bi-pencil-fill text-warning fs-4" @click="editQuiz(quiz)"></i>
            <h3>{{ quiz.title }} ({{ quiz.subject }})</h3>
            <i class="bi bi-trash3-fill text-danger fs-4" @click="delQuiz(quiz.id)"></i>
          </div>
          <div class="">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Question</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(question, index) in quiz.questions" :key="question.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ question.question_statement }}</td>
                  <td>
                    <button class="btn btn-sm btn-warning me-2" @click="editQuestion(quiz, question)">Edit</button>
                    <button class="btn btn-sm btn-danger" @click="delQuestion(quiz, question)">Delete</button>
                  </td>
                </tr>
                <tr v-if="!quiz.questions || quiz.questions.length === 0">
                  <td colspan="3" class="text-center">No questions available</td>
                </tr>
              </tbody>
            </table>

            <div class="text-center d-flex justify-content-around align-items-center">
              <button class="btn btn-sm me-2" :class="quiz.is_active ? 'btn-danger' : 'btn-success'" @click="toggleQuiz(quiz)">{{ quiz.is_active ? 'Deactivate' : 'Activate' }}</button>
              <button class="btn btn-sm btn-pink" @click="addNewQuestion(quiz); console.log(quiz)">+ Question</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isSearching && !filteredQuizzes.length" class="text-center p-5">
      <h4 class="text-muted">No quizzes or questions found for "{{ getSearchQuery }}"</h4>
    </div>

    <ModalComponent v-if="isModalVisible" :title="quizModalAction" :isVisible="isModalVisible" @save="saveQuiz"
      @cancel="closeModal">
      <form class="mx-5" @submit.prevent="">
        <div class="mb-3 form-floating">
          <input type="text" v-model="newQuiz.title" name="title" id="title" class="form-control"
            placeholder="title" required />
          <label for="remarks" class="form-label">Title:</label>
        </div>
        <div class="mb-3 form-floating">
          <textarea rows="10" type="text" v-model="newQuiz.remarks" name="description" id="description"
            class="form-control" placeholder="description" required />
          <label for="description" class="form-label">Description:</label>
        </div>
        <div class="mb-3">
          <label for="chapter" class="form-label">Select Chapter:</label>
            <select v-if="getChapters && getChapters.length" id="chapter" v-model="newQuiz.chapter_id" name="chapter"
            class="form-select" required>
            <option disabled value="">Select a chapter</option>
            <option v-for="chapter in getChapters" :key="chapter.id" :value="chapter.id">
              {{ chapter.name }} ({{ chapter.subject.name }})
            </option>
            </select>
          <div v-else class="text-muted">No chapters available</div>
        </div>
        <div class="mb-3">
          <label for="date_of_quiz" class="form-label">Date & Time of Quiz:</label>
          <input type="datetime-local" v-model="newQuiz.date_of_quiz" name="date_of_quiz" id="date_of_quiz"
            class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="time_duration" class="form-label">Time duration (in minutes):</label>
          <input type="number" v-model="newQuiz.time_duration" name="time_duration" id="time_duration"
            class="form-control" required />
        </div>
      </form>
    </ModalComponent>

    <ModalComponent v-if="isQuestionModalVisible" :title="questionModalAction"
      :isVisible="isQuestionModalVisible" @save="saveQuestion" @cancel="closeQuestionModal">
      <form class="mx-5" @submit.prevent="">
        <div class="mb-3">
          <label for="question_statement" class="form-label">Question Statement:</label>
          <textarea :value="newQuestion.question_statement"
            @input="updateNewQuestion('question_statement', $event.target.value)" id="question_statement"
            class="form-control" rows="3" placeholder="Enter the question" required></textarea>
        </div>
        <div class="mb-3">
          <label for="option1" class="form-label">Option 1:</label>
          <input type="text" :value="newQuestion.option1" @input="updateNewQuestion('option1', $event.target.value)"
            id="option1" class="form-control" placeholder="Option 1" required />
        </div>
        <div class="mb-3">
          <label for="option2" class="form-label">Option 2:</label>
          <input type="text" :value="newQuestion.option2" @input="updateNewQuestion('option2', $event.target.value)"
            id="option2" class="form-control" placeholder="Option 2" required />
        </div>
        <div class="mb-3">
          <label for="option3" class="form-label">Option 3:</label>
          <input type="text" :value="newQuestion.option3" @input="updateNewQuestion('option3', $event.target.value)"
            id="option3" class="form-control" placeholder="Option 3" required />
        </div>
        <div class="mb-3">
          <label for="option4" class="form-label">Option 4:</label>
          <input type="text" :value="newQuestion.option4" @input="updateNewQuestion('option4', $event.target.value)"
            id="option4" class="form-control" placeholder="Option 4" required />
        </div>
        <div class="mb-3">
          <label for="correct_option" class="form-label">Correct Option:</label>
          <select :value="newQuestion.correct_option"
            @change="updateNewQuestion('correct_option', Number($event.target.value))" id="correct_option"
            class="form-select" required>
            <option value="1">Option 1</option>
            <option value="2">Option 2</option>
            <option value="3">Option 3</option>
            <option value="4">Option 4</option>
          </select>
        </div>
      </form>
    </ModalComponent>

    <Spinner :active="isLoading"></Spinner>
    <Fab v-if="!isModalVisible && !isQuestionModalVisible" @click="openModal" toAdd="Quiz" />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import ModalComponent from '../../components/ModalComponent.vue';
import Fab from '../../components/Fab.vue';
import Spinner from '../../components/Spinner.vue';


export default {
  name: 'QuizManagement',
  components: { Fab, ModalComponent, Spinner },
  computed: {
    ...mapGetters([
      'getUser',
      'getQuizzes',
      'getChapters',
      'isModalVisible',
      'quizModalAction',
      'newQuiz',
      'isLoading',
      'isQuestionModalVisible',
      'questionModalAction',
      'newQuestion',
      'getSearchQuery',
    ]),
    quizzes() {
      return this.getQuizzes;
    },
    isSearching() {
      return this.getSearchQuery && this.getSearchQuery.trim() !== '';
    },
    filteredQuizzes() {
      if (!this.isSearching) {
        return this.quizzes;
      }
      const query = this.getSearchQuery.toLowerCase().trim();
      return this.quizzes.filter(quiz => {
        const titleMatch = quiz.title.toLowerCase().includes(query);
        const subjectMatch = quiz.subject.toLowerCase().includes(query);
        const questionMatch = quiz.questions.some(question =>
          question.question_statement.toLowerCase().includes(query)
        );
        return titleMatch || subjectMatch || questionMatch;
      });
    },
  },
  methods: {
    ...mapActions([
      'fetchUser',
      'fetchQuizzes',
      'fetchSubjects',
      'openModal',
      'closeModal',
      'saveQuiz',
      'updateQuiz',
      'deleteQuiz',
      'openQuestionModal',
      'closeQuestionModal',
      'addQuestion',
      'updateQuestion',
      'deleteQuestion',
      'performSearch',
      'toggleQuiz',
    ]),
    editQuiz(quiz) {
      this.updateQuiz({ quiz: quiz })
    },
    async delQuiz(quizID) {
      if (confirm(`Are you sure you want to delete quiz?`)) {
        try {
          await this.deleteQuiz({ quizId: quizID });
          alert('Quiz deleted successfully!');
        } catch (error) {
          alert('Failed to delete quiz: ' + (error.response?.data?.message || error.message));
        }
      }
    },
    updateNewQuestion(field, value) {
      this.$store.commit('SET_NEW_QUESTION', { ...this.newQuestion, [field]: value });
    },

    editQuestion(quiz, question) {
      this.openQuestionModal({ quiz, action: 'Edit Question', question });
    },

    async delQuestion(quiz, question) {
      if (confirm(`Are you sure you want to delete question: "${question.question_statement}"?`)) {
        try {
          await this.deleteQuestion({ quizId: quiz.id, questionId: question.id });
          alert('Question deleted successfully!');
        } catch (error) {
          alert('Failed to delete question: ' + (error.response?.data?.message || error.message));
        }
      }
    },

    addNewQuestion(quiz) {
      this.openQuestionModal({ quiz, action: 'Add Question' });
    },

    async saveQuestion() {
      try {
        if (this.questionModalAction === 'Add Question') {
          await this.addQuestion();
          alert('Question added successfully!');
        } else {
          await this.updateQuestion();
          alert('Question updated successfully!');
        }
      } catch (error) {
        alert('Failed to save question: ' + (error.response?.data?.message || error.message));
      }
    },
  },
  mounted() {
    this.fetchUser();
    this.fetchSubjects();
    this.fetchQuizzes();
  },
  beforeUnmount() {
    this.performSearch(''); // Clear search query on unmount
  }
};
</script>

<style scoped>
.card-header {
  border-radius: 0.375rem;
  display: flex;
  justify-content: space-between;
  font-weight: bold;
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


.card-themed {
  background: rgba(181, 177, 177, 0.35);
  box-shadow: 0 8px 32px 0 rgba(18, 19, 32, 0.557);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.509);
}


.btn-pink {
  background-color: #ff99cc;
  border-color: #ff99cc;
  color: white;
}

.btn-pink:hover {
  background-color: #ff80bf;
  border-color: #ff80bf;
}

/* .table th,
.table td {
  text-align: center;
  vertical-align: middle;
} */

.card-body {
  padding: 1.5rem;
}
</style>
