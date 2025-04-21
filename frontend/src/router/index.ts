import { createRouter, createWebHistory } from 'vue-router';

import Layout from '@/components/Layout.vue';
const routes = [
	{
		path: '/',
		component: Layout,
		children: [
			{
				path: '/',
				redirect: '/home',
			},
			{
				path: '/home',
				component: () => import('@/views/Home.vue'),
			},
			{
				path: '/change-password',
				component: () => import('@/views/common/ChangePassword.vue'),
			},
			{
				path: '/profile',
				component: () => import('@/views/common/Profile.vue'),
			},
			{
				path: '/courses',
				component: () => import('@/views/common/Courses.vue'),
			},
			{
				path: '/my-evaluations',
				component: () => import('@/views/student/MyEvaluations.vue'),
			},
			{
				path: '/my-courses',
				component: () => import('@/views/teacher/MyCourses.vue'),
			},
			{
				path: '/user-management',
				component: () => import('@/views/admin/UserManagement.vue'),
			},
			{
				path: '/evaluation-management',
				component: () => import('@/views/admin/EvaluationManagement.vue'),
			},
			{
				path: '/course-management',
				component: () => import('@/views/admin/CourseManagement.vue'),
			},
		],
	},
	{
		path: '/login',
		component: () => import('@/views/Login.vue'),
	},
	{
		path: '/register',
		component: () => import('@/views/Register.vue'),
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

router.beforeEach((to, _from, next) => {
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
