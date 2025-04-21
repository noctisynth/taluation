import axios from 'axios';

const request = axios.create({
	baseURL: process.env.FARM_BASE_URL + '/api',
	timeout: 5000,
});

request.interceptors.request.use(
	(config) => {
		if (config.headers) {
			config.headers['Content-Type'] = 'application/json';
		}

		const token = localStorage.getItem('token');
		const username = localStorage.getItem('username');

		if (token && username) {
			const url = config.url || '';
			const isAuthRequest = url.includes('/login') || url.includes('/register');

			if (config.method === 'get' && !isAuthRequest) {
				config.params = {
					...config.params,
					username,
					token,
				};
			} else if (!isAuthRequest) {
				const originalData = config.data || {};

				config.data = {
					auth: {
						username,
						token,
					},
					data: originalData,
				};
			}
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	},
);

export default request;
