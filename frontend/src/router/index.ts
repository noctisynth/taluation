import { createRouter, createWebHistory } from 'vue-router';

import Layout from '@/components/Layout.vue';
const routes = [
    {
        path: '/',
        component: Layout,
        children: [
            {
                path: '/home',
                component: () => import('@/views/Home.vue')
            },
            {
                path: '/change-password',
                component: () => import('@/views/common/ChangePassword.vue')
            },
            {
                path: '/profile',
                component: () => import('@/views/common/Profile.vue')
            }
        ]
    },
    {
        path: '/login',
        component: () => import('@/views/Login.vue'),
    },
    {
        path: '/register',
        component: () => import('@/views/Register.vue'),
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