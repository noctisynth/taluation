import router from '@/router';
import request from './request';

export function logout(needRequest: boolean = true) {
	const token = localStorage.getItem('token');
	const username = localStorage.getItem('username');

	if (token && username && needRequest) {
		request
			.get('/account/logout', {
				params: {
					username,
					token,
				},
			})
			.then(() => {
				router.push('/login');
			})
			.catch(() => {
				router.push('/login');
			});
	} else {
		router.push('/login');
	}

	localStorage.removeItem('token');
	localStorage.removeItem('username');
}

export async function changePassword(newpassword: string, oldpassword: string) {
	try {
		const res = await request.post('/account/change-password', {
			newpassword,
			oldpassword,
		});
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function getProfile(username?: string) {
	try {
		const res = await request.get('/account', {
			params: {
				name: username || localStorage.getItem('username'),
			},
		});
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function updateProfile(data: {
	username: string;
	newname?: string;
	email?: string;
	phone?: string;
	type?: string;
}) {
	try {
		const res = await request.patch('/account', data);
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function getUsers() {
	try {
		const res = await request.get('/account/users');
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function addClass(data: {
	name: string;
	teacher: string;
	description: string;
	category: string;
}) {
	try {
		const res = await request.put('/class', data);
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function deleteClass(data: {
	id?: string;
	name?: string;
}) {
	try {
		const res = await request.delete('/class', {
			params: data,
		});
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function updateClass(data: {
	name: string;
	newname?: string;
	teacher?: string;
	description?: string;
	category?: string;
}) {
	try {
		const res = await request.patch('/class', data);
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function getClasses(data: {
	id?: string;
	name?: string;
	teacher?: string;
}) {
	try {
		const res = await request.get('/class', {
			params: data,
		});
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function addEvaluation(data: {
	cls: string;
	score: number;
	comment: string;
}) {
	try {
		const res = await request.put('/evaluation', {
			cls: data.cls,
			score: data.score,
			comment: data.comment,
		});
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function getEvaluationStats(data: {
	class_id?: string;
	class_name?: string;
}) {
	try {
		const res = await request.get('/evaluation/stats', {
			params: data,
		});
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function getEvaluations(data: {
	id?: string;
	user_id?: string;
	class_id?: string;
	user_name?: string;
	class_name?: string;
}) {
	try {
		const res = await request.get('/evaluation', {
			params: {
				id: data.id,
				user_id: data.user_id,
				class_id: data.class_id,
				user_name: data.user_name,
				class_name: data.class_name,
			},
		});
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function deleteEvaluation(id: string) {
	try {
		const res = await request.delete('/evaluation', {
			params: {
				id,
			},
		});
		return res.data;
	} catch (error) {
		return error;
	}
}

export async function deleteUser(username: string) {
	try {
		const res = await request.delete('/account', {
			params: {
				username,
			},
		});
		return res.data;
	} catch (error) {
		return error;
	}
}
