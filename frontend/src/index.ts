import { createApp } from 'vue';

import PrimeVue from 'primevue/config';

import Material from '@primeuix/themes/material';
import 'primeflex/primeflex.scss';
import 'primeicons/primeicons.css'
import './index.scss';


import App from './App.vue';

import router from './router';

const app = createApp(App);
app.use(PrimeVue, {
    theme: {
        preset: Material,
        options: {
            darkModeSelector: '.dark',
        }
    },
});
app.use(router);
app.mount('#app');