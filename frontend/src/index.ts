import { createApp } from 'vue';

import PrimeVue from 'primevue/config';

import Material from '@primeuix/themes/material';
import 'primeflex/primeflex.scss';
import 'primeicons/primeicons.css'
import './index.scss';

import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import { GridComponent, TooltipComponent, TitleComponent } from "echarts/components";

import App from './App.vue';
import router from './router';

use([
    CanvasRenderer,
    BarChart,
    GridComponent,
    TooltipComponent,
    TitleComponent
]);

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