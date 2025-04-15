import { createRouter, createWebHistory } from 'vue-router';

import Home from '@/views/Home.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import ClassManagement from '@/views/panels/ClassManagement.vue';
import EvaluationManagement from '@/views/panels/EvaluationManagement.vue';
import UserManagement from '@/views/panels/UserManagement.vue';

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/register',
        component: Register
    },
    {
        path: '/classes',
        component: ClassManagement
    },
    {
        path: '/evaluations',
        component: EvaluationManagement
    },
    {
        path: '/users',
        component: UserManagement
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    
    if (!token || !username) {
        if (to.path !== '/login' && to.path !== '/register') {
            next('/login');
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;