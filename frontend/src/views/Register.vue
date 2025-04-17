<template>
<div id="register-container" class="auth-container">
    <Banner :message="errorMessage" v-model:show="showError" :duration="5000" :type="BannerType.Error" />
    <div class="auth-card-wrapper">
        <div class="logo-area">
            <h1>评教系统</h1>
            <div class="divider"></div>
        </div>
        <Card class="auth-card">
            <template #content>
                <Form v-slot="$form" :initialValues="registerData" :resolver="resolver" @submit="register" class="auth-form">
                    <div class="form-field">
                        <label for="username">用户名</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-user"></i>
                            </InputGroupAddon>
                            <InputText id="username" name="username" placeholder="请输入用户名" :feedback="false" class="w-full" />
                        </InputGroup>
                        <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">{{ $form.username.error.message }}</Message>
                    </div>
                    <div class="form-field">
                        <label for="email">邮箱</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-envelope"></i>
                            </InputGroupAddon>
                            <InputText id="email" name="email" placeholder="请输入邮箱" :feedback="false" class="w-full" />
                        </InputGroup>
                        <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple">{{ $form.email.error.message }}</Message>
                    </div>
                    <div class="form-field">
                        <label for="phone">手机号</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-phone"></i>
                            </InputGroupAddon>
                            <InputText id="phone" name="phone" placeholder="请输入手机号" :feedback="false" class="w-full" />
                        </InputGroup>
                        <Message v-if="$form.phone?.invalid" severity="error" size="small" variant="simple">{{ $form.phone.error.message }}</Message>
                    </div>
                    <div class="form-field">
                        <label for="type">角色</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-id-card"></i>
                            </InputGroupAddon>
                            <Select id="type" name="type" :options="typeOptions" optionLabel="label" optionValue="value" placeholder="请选择角色" class="w-full" />
                        </InputGroup>
                        <Message v-if="$form.type?.invalid" severity="error" size="small" variant="simple">{{ $form.type.error.message }}</Message>
                    </div>
                    <div class="form-field">
                        <label for="password">密码</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-lock"></i>
                            </InputGroupAddon>
                            <Password id="password" name="password" placeholder="请输入密码" :feedback="false" toggleMask class="w-full" inputClass="w-full" />
                        </InputGroup>
                        <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple">{{ $form.password.error.message }}</Message>
                    </div>
                    <div class="form-field">
                        <label for="confirmPassword">确认密码</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-lock"></i>
                            </InputGroupAddon>
                            <Password id="confirmPassword" name="confirmPassword" placeholder="请再次输入密码" :feedback="false" toggleMask class="w-full" inputClass="w-full" />
                        </InputGroup>
                        <Message v-if="$form.confirmPassword?.invalid" severity="error" size="small" variant="simple">{{ $form.confirmPassword.error.message }}</Message>
                    </div>
                    <div class="button-container">
                        <button type="submit" class="general-button" >
                            注 册
                        </button>
                    </div>
                    <div class="auth-link">
                        已有账号？<router-link to="/login">返回登录</router-link>
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
import Select from 'primevue/select';
import { Form, type FormSubmitEvent } from '@primevue/forms';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import Banner from '@/components/Banner.vue';
import { BannerType } from '@/components/Banner.vue';
import Message from 'primevue/message';

import request from '@/utils/request';
import router from '@/router';
import { ref } from 'vue';
import { z } from "zod";

const typeOptions = [
    { label: '学生', value: 'student' },
    { label: '教师', value: 'teacher' },
    { label: '管理员', value: 'admin' }
];

const registerData = {
    username: '',
    password: '',
    confirmPassword: '',
    email: '',
    phone: '',
    type: 'student'
};

const errorMessage = ref('');
const showError = ref(false);

const resolver = ref(zodResolver(
    z.object(
    {
        username: z.string().min(8, { message: '用户名至少需要8个字符' }),
        email: z.string().email({ message: '请输入有效的邮箱地址' }),
        phone: z.string()
            .regex(/^1[3-9]\d{9}$/, { message: '请输入有效的11位手机号' })
            .length(11, { message: '手机号必须为11位' }),
        type: z.string().min(1, { message: '请选择角色' }),
        password: z.string()
            .min(8, { message: '密码至少需要8个字符' })
            .regex(/[A-Z]/, { message: '密码需要包含至少一个大写字母' })
            .regex(/[a-z]/, { message: '密码需要包含至少一个小写字母' })
            .regex(/[0-9]/, { message: '密码需要包含至少一个数字' })
            .regex(/[^A-Za-z0-9]/, { message: '密码需要包含至少一个特殊字符' }),
        confirmPassword: z.string().min(1, { message: '请确认密码' }),
    }
)));



function register(form: FormSubmitEvent<Record<string, any>>) {
    const data = form.values as typeof registerData;
    
    request.post("/account/register", {
        id: null,
        username: data.username,
        password: data.password,
        email: data.email,
        phone: data.phone,
        type: data.type
    })
    .then(res => {
        if (res.data.success) {
            router.push('/login');
        } else {
            errorMessage.value = res.data.message || '注册失败';
            showError.value = true;
        }
    })
    .catch(_ => {
      errorMessage.value = '注册失败，请检查网络连接';
      showError.value = true;
    });
}
</script>

<style lang="scss" scoped>

</style>