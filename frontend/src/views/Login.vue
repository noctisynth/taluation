<template>
<div id="login-container" class="auth-container">
    <Banner :message="errorMessage" v-model:show="showError" :duration="5000" :type="BannerType.Error" />
    <div class="auth-card-wrapper">
        <div class="logo-area">
            <h1>评教系统</h1>
            <div class="divider"></div>
        </div>
        <Card class="auth-card">
            <template #content>
                <Form :initialValues="logindata" @submit="login" class="auth-form">
                    <div class="form-field">
                        <label for="username">用户名</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-user"></i>
                            </InputGroupAddon>
                            <InputText id="username" name="username" placeholder="请输入用户名" :feedback="false" class="w-full general-input" />
                        </InputGroup>
                    </div>
                    <div class="form-field">
                        <label for="password">密码</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-lock"></i>
                            </InputGroupAddon>
                            <Password id="password" name="password" placeholder="请输入密码" :feedback="false" toggleMask class="w-full general-input" />
                        </InputGroup>
                    </div>
                    <div class="button-container">
                        <button type="submit" class="general-button">
                            登 录
                        </button>
                    </div>
                    <div class="auth-link">
                        还没有账号？<router-link to="/register">立即注册</router-link>
                    </div>
                </Form>
            </template>
        </Card>
        <div class="copyright">© 2025 评教系统</div>
    </div>
</div>
</template>

<script setup lang="ts">
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import { Form, type FormSubmitEvent } from '@primevue/forms';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import { ref } from 'vue';
import { RouterLink } from 'vue-router';

import request from '@/utils/request';
import Banner from '@/components/Banner.vue';
import { BannerType } from '@/components/Banner.vue';
import router from '@/router';

const logindata = {
	username: '',
	password: '',
};

const errorMessage = ref('');
const showError = ref(false);

function login(form: FormSubmitEvent<Record<string, any>>) {
	const data = form.values as typeof logindata;

	request
		.post('/account/login', data)
		.then((res) => {
			if (res.data.success) {
				localStorage.setItem('username', data.username);
				localStorage.setItem('token', res.data.data.token);
				router.push('/');
			} else {
				errorMessage.value = res.data.message || '登录失败';
				showError.value = true;
			}
		})
		.catch((err) => {
			console.error('登录失败:', err);
			errorMessage.value = '登录失败，请检查网络连接';
			showError.value = true;
		});
}
</script>

<style lang="scss" scoped>
</style>
