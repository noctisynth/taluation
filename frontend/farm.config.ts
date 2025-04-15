import { defineConfig } from '@farmfe/core';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
	vitePlugins: [vue()],
	compilation: {
		output: {
			path: '../dist',
		},
		resolve: {
			alias: {
				"@": path.join(process.cwd(), "src"),
			}
		},
	},
	plugins: [
		"@farmfe/plugin-sass"
	],
	server: {
		proxy: {
			"/api": {
				target: process.env.FARM_API_BASE_URL,
				changeOrigin: true,
				pathRewrite: (path: any) => path.replace(/^\/api/, ""),
			}
		}
	}
});
