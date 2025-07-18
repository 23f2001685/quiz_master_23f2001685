import { createRouter, createWebHistory } from 'vue-router';
import LoginCard from '../views/auth/LoginCard.vue';
import Register from '../views/auth/Register.vue';
import AdminDashboard from '../views/admin/AdminDashboard.vue';
import UserDashboard from '../views/user/UserDashboard.vue';
import QuizManagement from '../views/admin/QuizManagement.vue';
import UserManagement from '../views/admin/UserManagement.vue';
import Quiz from '../views/user/Quiz.vue';
import Scores from '../views/user/Scores.vue';
import UserSummary from '../views/user/UserSummary.vue';

const routes = [
    {
        path: '/',
        redirect: '/login',
    },
    {
        path: '/login',
        name: 'LoginPage',
        component: LoginCard
    },
    {
        path: '/register',
        component: Register
    },
    {
        path: '/admin',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
        path: '/user',
        name: 'UserDashboard',
        component: UserDashboard,
        meta: { requiresAuth: true }
    },
    {
        path: '/quiz',
        name: 'QuizManagement',
        component: QuizManagement,
        meta: { requiresAdmin: true },
    },
    {
        path: '/users',
        name: 'UserManagement',
        component: UserManagement,
        meta: { requiresAdmin: true },
    },
    {
        path: '/quiz/:quizId',
        name: 'TakeQuiz',
        component: Quiz,
        props: true,
        meta: { requiresAuth: true }
    },
    {
        path: '/scores',
        name: 'ViewScores',
        component: Scores,
        props: true,
        meta: { requiresAuth: true }
    },
    {
        path: '/summary',
        name: 'ViewSummary',
        component: UserSummary,
        props: true,
        meta: { requiresAuth: true }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    // Replace these with your actual authentication logic
    const isAuthenticated = !!localStorage.getItem('auth_token'); // Example: check if user is logged in
    const isAdmin = localStorage.getItem('role') === 'admin'; // Example: check if user is admin

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated) {
            next({ path: '/login' });
            return;
        }
    }
    if (to.matched.some(record => record.meta.requiresAdmin)) {
        if (!isAdmin) {
            next(from.path); // Redirect to the previous page if not admin
            return;
        }
    }
    next();
});



export default router;
