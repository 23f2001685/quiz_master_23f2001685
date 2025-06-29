import { createRouter, createWebHistory } from 'vue-router';
import LoginCard from '../views/auth/LoginCard.vue';
import Register from '../views/auth/Register.vue';
import AdminDashboard from '../views/admin/AdminDashboard.vue';
import UserDashboard from '../views/user/UserDashboard.vue';
import QuizManagement from '../views/admin/QuizManagement.vue';
import UserManagement from '../views/admin/UserManagement.vue';

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
        component: AdminDashboard
    },
    {
        path: '/user',
        name: 'UserDashboard',
        component: UserDashboard
    },
    {
        path: '/quiz',
        name: 'QuizManagement',
        component: QuizManagement
    },
    {
        path: '/users',
        name: 'UserManagement',
        component: UserManagement,
        meta: { requiresAdmin: true },
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});



export default router;
