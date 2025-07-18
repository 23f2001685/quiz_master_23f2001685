import { createStore } from 'vuex'
import axios from 'axios'

const store = createStore({
  state: {
    user: null,
    subjects: [],
    chapters: [],
    quizzes: [],
    users: [],
    isModalVisible: false,
    newSubject: { name: '', description: '' },
    newQuiz: {
      title: '',
      remarks: '',
      chapter_id: null,
      date_of_quiz: "",
      time_duration: 60,
      is_active: true
    },
    subjectId: null,
    modalAction: 'New Subject',
    quizModalAction: 'New Quiz',
    error: null,
    isLoading: false,
    isQuestionModalVisible: false,
    questionModalAction: 'Add Question',
    currentQuiz: null,
    newQuestion: {
      quiz_id: null,
      question_statement: '',
      option1: '',
      option2: '',
      option3: '',
      option4: '',
      correct_option: 1,
    },
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_USERS(state, users) {
      state.users = users;
    },
    SET_SUBJECTS(state, subjects) {
      state.subjects = subjects
    },
    SET_CHAPTERS(state, chapters) {
      state.chapters = chapters
    },
    SET_QUIZZES(state, quizzes) {
      state.quizzes = quizzes
    },
    SET_MODAL_VISIBLE(state, isVisible) {
      state.isModalVisible = isVisible
    },
    SET_NEW_SUBJECT(state, newSubject) {
      state.newSubject = newSubject
    },
    SET_SUBJECT_ID(state, subjectId) {
      state.subjectId = subjectId
    },
    SET_MODAL_ACTION(state, action) {
      state.modalAction = action
    },
    SET_QUIZ_MODAL_ACTION(state, action) {
      state.modalAction = action
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    SET_NEW_QUIZ(state, newQuiz) {
      state.newQuiz = newQuiz
    },
    SET_LOADING(state, isLoading) {
      state.isLoading = isLoading
    },
    SET_QUESTION_MODAL_VISIBLE(state, isVisible) {
      state.isQuestionModalVisible = isVisible;
    },
    SET_QUESTION_MODAL_ACTION(state, action) {
      state.questionModalAction = action;
    },
    SET_CURRENT_QUIZ(state, quiz) {
      state.currentQuiz = quiz;
    },
    SET_NEW_QUESTION(state, newQuestion) {
      state.newQuestion = newQuestion;
    },
    RESET_NEW_QUESTION(state) {
      state.newQuestion = {
        quiz_id: null,
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: 1,
      };
    },
  },
  actions: {

    // Users
    async fetchUser({ commit }) {
      const auth_token = localStorage.getItem('auth_token')
      if (auth_token == null) return
      try {
        const response = await axios.get('http://localhost:5000/me', {
          headers: {
            'Authentication-Token': localStorage.getItem('auth_token'),
          },
        });
        commit('SET_USER', response.data);
      } catch (error) {
        console.error('Please login to proceed');
      }
    },
    logOut({ commit }) {
      localStorage.removeItem('auth_token');
      commit('SET_USER', null);
      commit('SET_USERS', []);
      commit('SET_SUBJECTS', []);
      commit('SET_CHAPTERS', []);
      commit('SET_QUIZZES', []);
      commit('SET_MODAL_VISIBLE', false);
      commit('SET_NEW_SUBJECT', { name: '', description: '' });
      commit('SET_NEW_QUIZ', {
        remarks: '',
        chapter_id: null,
        date_of_quiz: "",
        time_duration: 60,
        is_active: true
      });
      commit('SET_SUBJECT_ID', null);
      commit('SET_MODAL_ACTION', 'New Subject');
      commit('SET_QUIZ_MODAL_ACTION', 'New Quiz');
      commit('SET_ERROR', null);
      commit('SET_LOADING', false);
      commit('SET_QUESTION_MODAL_VISIBLE', false);
      commit('RESET_NEW_QUESTION');
      commit('SET_CURRENT_QUIZ', null);
      commit('SET_QUESTION_MODAL_ACTION', 'Add Question');
      commit('SET_NEW_QUESTION', {
        quiz_id: null,
        question_statement: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: 1,
      });
    },
    async fetchUsers({ commit }) {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        console.error('Authentication token is missing');
        commit('SET_USERS', []);
        return;
      }
      try {
        commit('SET_LOADING', true);
        const response = await axios.get('http://localhost:5000/api/users', {
          headers: {
            'Authentication-Token': token,
          },
        });
        commit('SET_USERS', response.data);
      } catch (error) {
        console.error('Error fetching users:', error.response?.data?.message || error.message);
        commit('SET_USERS', []);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    async deactivateUser({ commit, dispatch }, userId) {
      try {
        commit('SET_LOADING', true);
        await axios.put(`http://localhost:5000/api/users/${userId}/deactivate`, {}, {
          headers: {
            'Authentication-Token': localStorage.getItem('auth_token'),
          },
        });
        dispatch('fetchUsers');
      } catch (error) {
        console.error('Error deactivating user:', error.response?.data?.message || error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },

    // Quiz + Subjects
    async fetchSubjects({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await axios.get('http://localhost:5000/api/subjects', {
          headers: {
            'Authentication-Token': localStorage.getItem('auth_token'),
          },
        })
        commit('SET_SUBJECTS', response.data)
        const chapters = response.data.flatMap((subject) => subject.chapters)
        commit('SET_CHAPTERS', chapters)
        commit('SET_LOADING', false)
      } catch (error) {
        console.error('Error fetching subjects:', error)
        commit('SET_LOADING', false)
      }
    },
    async fetchQuizzes({ commit }) {
      try {
        const response = await axios.get('http://localhost:5000/api/quizzes',
          {
            headers: {
              'Authentication-Token': localStorage.getItem('auth_token'),
            },
          });
          console.log('Fetched quizzes:', response.data);

        commit('SET_QUIZZES', response.data);
      } catch (error) {
        console.error('Error fetching quizzes:', error);
      }
    },
    openModal({ commit }) {
      commit('SET_MODAL_VISIBLE', true);
    },
    closeModal({ commit }) {
      commit('SET_MODAL_VISIBLE', false);
      commit('SET_MODAL_ACTION', 'New Subject');
      commit('SET_QUIZ_MODAL_ACTION', 'New Quiz');
      commit('SET_NEW_SUBJECT', { name: '', description: '' });
      commit('SET_SUBJECT_ID', null);
      commit('SET_NEW_QUIZ', {
        remarks: '',
        chapter: '',
        date_of_quiz: "",
        time_duration: 60,
        is_active: false
      })
    },
    async saveSubject({ commit, state, dispatch }) {
      commit('SET_LOADING', true)
      if (!state.newSubject.name.trim()) {
        commit('SET_ERROR', 'Please provide subject name.');
        return;
      }

      try {
        if (state.subjectId !== null) {
          await axios.put(
            `http://localhost:5000/api/subjects/${state.subjectId}`,
            {
              name: state.newSubject.name,
              description: state.newSubject.description,
            },
            {
              headers: {
                'Authentication-Token': localStorage.getItem('auth_token'),
              },
            }
          );
        } else {
          await axios.post(
            'http://localhost:5000/api/subjects',
            {
              name: state.newSubject.name,
              description: state.newSubject.description,
            },
            {
              headers: {
                'Authentication-Token': localStorage.getItem('auth_token'),
              },
            }
          );
        }
        commit('SET_NEW_SUBJECT', { name: '', description: '' });
        commit('SET_MODAL_VISIBLE', false);
        commit('SET_SUBJECT_ID', null);
        commit('SET_ERROR', null);
        dispatch('fetchSubjects');
        commit('SET_LOADING', false)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Error saving subject');
        commit('SET_LOADING', false)
      }
      commit('SET_LOADING', false)
    },
    editSubject({ commit }, subject) {
      commit('SET_NEW_SUBJECT', {
        name: subject.name,
        description: subject.description,
      });
      commit('SET_SUBJECT_ID', subject.id);
      commit('SET_MODAL_ACTION', 'Edit Subject');
      commit('SET_MODAL_VISIBLE', true);
    },
    async deleteSubject({ dispatch }, subjectId) {
      try {
        const response = await axios.delete(
          `http://localhost:5000/api/subjects/${subjectId}`,
          {
            headers: {
              'Authentication-Token': localStorage.getItem('auth_token'),
            },
          }
        );
        dispatch('fetchSubjects');
      } catch (error) {
        console.error('Error deleting subject:', error.response);
      }
    },
    async saveQuiz({ commit, state, dispatch }) {
      commit('SET_LOADING', true)
      if (!state.newQuiz.title.trim()) {
        commit('SET_ERROR', 'Please provide quiz name.');
        return;
      }
      try {
        if (state.newQuiz.id) {
          await axios.put(
            `http://localhost:5000/api/quizzes/${state.newQuiz.id}`,
            {
              title: state.newQuiz.title,
              remarks: state.newQuiz.remarks,
              chapter_id: state.newQuiz.chapter_id,
              date_of_quiz: state.newQuiz.date_of_quiz,
              time_duration: state.newQuiz.time_duration,
              is_active: state.newQuiz.is_active
            },
            {
              headers: {
                'Authentication-Token': localStorage.getItem('auth_token'),
              },
            }
          );
        } else {
          console.log("Saving new quiz:", state.newQuiz);
          const date = new Date(state.newQuiz.date_of_quiz);
          const formattedDate = date.toISOString()//.slice(0, 10); // Format to YYYY-MM-DD (Pythonic)
          await axios.post(
            'http://localhost:5000/api/quizzes',
            {
              title: state.newQuiz.title,
              remarks: state.newQuiz.remarks,
              chapter_id: state.newQuiz.chapter_id,
              date_of_quiz: formattedDate,
              time_duration: state.newQuiz.time_duration,
              is_active: state.newQuiz.is_active
            },
            {
              headers: {
                'Authentication-Token': localStorage.getItem('auth_token'),
              },
            }
          )
        }

        commit('SET_NEW_QUIZ', {
          remarks: '',
          chapter: '',
          date_of_quiz: "",
          time_duration: 60,
          is_active: true
        });
        commit('SET_MODAL_VISIBLE', false);
        commit('SET_ERROR', null);
        dispatch('fetchQuizzes');
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.message || 'Error saving quiz');
        console.log('Error saving quiz:', error.response?.data?.message || error.message);

      } finally {
        commit('SET_LOADING', false)
      }
    },
    updateQuiz({ commit, state }, {quiz}) {
      const date = new Date(quiz.date_of_quiz);
      const formattedDate = date.toISOString();
      commit('SET_NEW_QUIZ', {
        chapter_id: quiz.chapter_id,
        date_of_quiz: formattedDate,
        time_duration: quiz.time_duration,
        remarks: quiz.remarks,
        is_active: quiz.is_active,
        id: quiz.id,
      });
      commit('SET_QUIZ_MODAL_ACTION', 'Edit Quiz');
      commit('SET_MODAL_VISIBLE', true);
    },
    async deleteQuiz({ commit, dispatch }, { quizId }) {
      try {

        commit('SET_LOADING', true);
        const res = await axios.delete(
          `http://localhost:5000/api/quizzes/${quizId}`,
          {
            headers: {
              'Authentication-Token': localStorage.getItem('auth_token'),
            },
          }
        )
        dispatch('fetchQuizzes');
      } catch (error) {
        console.error('Error deleting quiz:', error.response?.data?.message || error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    openQuestionModal({ commit }, { quiz, action = 'Add Question', question = null }) {
      commit('SET_CURRENT_QUIZ', quiz);
      commit('SET_QUESTION_MODAL_ACTION', action);
      if (action === 'Edit Question' && question) {
        commit('SET_NEW_QUESTION', {
          quiz_id: quiz.id,
          question_statement: question.question_statement,
          option1: question.option1,
          option2: question.option2,
          option3: question.option3,
          option4: question.option4,
          correct_option: question.correct_option,
          id: question.id,
        });
      } else {
        commit('SET_NEW_QUESTION', {
          quiz_id: quiz.id,
          question_statement: '',
          option1: '',
          option2: '',
          option3: '',
          option4: '',
          correct_option: 1,
        });
      }
      commit('SET_QUESTION_MODAL_VISIBLE', true);
    },
    closeQuestionModal({ commit }) {
      commit('SET_QUESTION_MODAL_VISIBLE', false);
      commit('RESET_NEW_QUESTION');
      commit('SET_CURRENT_QUIZ', null);
    },
    async addQuestion({ state, commit, dispatch }) {
      try {
        commit('SET_LOADING', true);
        await axios.post(
          `http://localhost:5000/api/quizzes/${state.currentQuiz.id}/questions`,
          state.newQuestion,
          {
            headers: {
              'Authentication-Token': localStorage.getItem('auth_token'),
            },
          }
        );
        commit('SET_QUESTION_MODAL_VISIBLE', false);
        commit('RESET_NEW_QUESTION');
        dispatch('fetchQuizzes');
      } catch (error) {
        console.error('Error adding question:', error.response?.data?.message || error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    async updateQuestion({ state, commit, dispatch }) {
      try {
        commit('SET_LOADING', true);
        const questionId = state.newQuestion.id;
        await axios.put(
          `http://localhost:5000/api/quizzes/${state.currentQuiz.id}/questions/${questionId}`,
          state.newQuestion,
          {
            headers: {
              'Authentication-Token': localStorage.getItem('auth_token'),
            },
          }
        );
        commit('SET_QUESTION_MODAL_VISIBLE', false);
        commit('RESET_NEW_QUESTION');
        dispatch('fetchQuizzes');
      } catch (error) {
        console.error('Error updating question:', error.response?.data?.message || error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    async deleteQuestion({ commit, dispatch }, { quizId, questionId }) {
      try {
        commit('SET_LOADING', true);
        await axios.delete(
          `http://localhost:5000/api/quizzes/${quizId}/questions/${questionId}`,
          {
            headers: {
              'Authentication-Token': localStorage.getItem('auth_token'),
            },
          }
        );
        dispatch('fetchQuizzes');
      } catch (error) {
        console.error('Error deleting question:', error.response?.data?.message || error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
  },
  getters: {
    getUser(state) {
      return state.user;
    },
    users(state) {
      return state.users;
    },
    getSubjects(state) {
      return state.subjects;
    },
    getChapters(state) {return state.chapters.map((chapter) => {
        const subject = state.subjects.find((s) => s.id === chapter.subject_id);
        return {
          ...chapter,
          subject: subject ? { id: subject.id, name: subject.name } : { id: chapter.subject_id, name: 'Unknown' },
        };
      });
    },
    isLoading(state) {
      return state.isLoading;
    },
    getQuizzes(state) {
      return state.quizzes;
    },

    isModalVisible(state) {
      return state.isModalVisible;
    },
    newSubject(state) {
      return state.newSubject;
    },
    newQuiz(state) {
      return state.newQuiz;
    },
    modalAction(state) {
      return state.modalAction;
    },
    quizModalAction(state) {
      return state.quizModalAction;
    },
    getError(state) {
      return state.error;
    },
    isQuestionModalVisible(state) {
      return state.isQuestionModalVisible;
    },
    questionModalAction(state) {
      return state.questionModalAction;
    },
    newQuestion(state) {
      return state.newQuestion;
    },
  },
});

export default store;
