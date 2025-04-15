<template>
    <div class="change-password-container">
        <Banner :message="bannerInfo.message" v-model:show="bannerInfo.show" :duration="bannerInfo.duration" :type="bannerInfo.type" />
        <Card class="profile-card">
            <template #header>
                <div class="profile-header">
                    <Avatar icon="pi pi-lock" size="xlarge" class="profile-avatar" />
                    <div class="profile-title">
                        <h2>修改密码</h2>
                        <span class="profile-type">确保您的账户安全</span>
                    </div>
                </div>
            </template>
            <template #content>
                <Form v-slot="$form" :resolver="resolver" :initialValues="formData" @submit="handleSubmit" class="edit-form">
                    <div class="form-field">
                        <label for="oldpassword">当前密码</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-lock"></i>
                            </InputGroupAddon>
                            <Password id="oldpassword" name="oldpassword" 
                                      placeholder="请输入当前密码" :feedback="false" toggleMask 
                                      class="w-full" inputClass="w-full" />
                        </InputGroup>
                        <Message v-if="$form.oldpassword?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.oldpassword.error.message }}
                        </Message>
                    </div>
                    <div class="form-field">
                        <label for="newpassword">新密码</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-lock"></i>
                            </InputGroupAddon>
                            <Password id="newpassword" name="newpassword" 
                                      placeholder="请输入新密码" :feedback="false" toggleMask 
                                      class="w-full" inputClass="w-full" />
                        </InputGroup>
                        <Message v-if="$form.newpassword?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.newpassword.error.message }}
                        </Message>
                    </div>
                    <div class="form-field">
                        <label for="confirmPassword">确认新密码</label>
                        <InputGroup>
                            <InputGroupAddon>
                                <i class="pi pi-lock"></i>
                            </InputGroupAddon>
                            <Password id="confirmPassword" name="confirmPassword" 
                                      placeholder="请再次输入新密码" :feedback="false" toggleMask 
                                      class="w-full" inputClass="w-full" />
                        </InputGroup>
                        <Message v-if="$form.confirmPassword?.invalid" severity="error" size="small" variant="simple">
                            {{ $form.confirmPassword.error.message }}
                        </Message>
                    </div>
                    <div class="profile-actions">
                        <Button type="submit" icon="pi pi-check" label="确认修改" class="p-button-outlined p-button-secondary" />
                        <Button type="button" icon="pi pi-arrow-left" label="返回" class="p-button-outlined p-button-secondary" @click="goBack" />
                    </div>
                </Form>
            </template>
        </Card>
    </div>
</template>

<script setup lang="ts">
import Banner from '@/components/Banner.vue';
import { BannerType } from '@/components/Banner.vue';
import auth from '@/utils/api';
import { ref } from 'vue';
import Card from 'primevue/card';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Password from 'primevue/password';
import { Form, FormSubmitEvent } from '@primevue/forms';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import Message from 'primevue/message';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import { useRouter } from 'vue-router';

const router = useRouter();

const bannerInfo = ref({
    message: '',
    show: false,
    duration: 3000,
    type: BannerType.Success
});

const formData = {
    newpassword: '',
    oldpassword: '',
    confirmPassword: ''
};

const resolver = ref(zodResolver(
    z.object({
        oldpassword: z.string().min(1, { message: '请输入当前密码' }),
        newpassword: z.string()
            .min(8, { message: '密码至少需要8个字符' })
            .regex(/[A-Z]/, { message: '密码需要包含至少一个大写字母' })
            .regex(/[a-z]/, { message: '密码需要包含至少一个小写字母' })
            .regex(/[0-9]/, { message: '密码需要包含至少一个数字' })
            .regex(/[^A-Za-z0-9]/, { message: '密码需要包含至少一个特殊字符' }),
        confirmPassword: z.string().min(1, { message: '请确认密码' }),
    }).refine((data) => data.newpassword === data.confirmPassword, {
        message: "两次输入的密码不一致",
        path: ["confirmPassword"],
    })
));

function handleSubmit(form: FormSubmitEvent<Record<string, any>>) {
    const data = form.values as typeof formData;
    auth.changePassword(data.newpassword, data.oldpassword).then(res => {
        if (res.success) {
            bannerInfo.value.message = '密码修改成功';
            bannerInfo.value.type = BannerType.Success;
            bannerInfo.value.show = true;
            auth.logout(false);
        } else {
            bannerInfo.value.message = res.message;
            bannerInfo.value.type = BannerType.Error;
            bannerInfo.value.show = true;
        }
    }).catch((error) => {
        bannerInfo.value.message = error.message;
        bannerInfo.value.type = BannerType.Error;
        bannerInfo.value.show = true;
    });
}

function goBack() {
    router.push('/profile');
}

</script>

<style scoped lang="scss">
.change-password-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.profile-card {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-radius: 0.5rem;
}

.profile-header {
    display: flex;
    align-items: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #f6f8fa 0%, #eef2f5 100%);
    border-radius: 0.5rem 0.5rem 0 0;
}

.profile-avatar {
    width: 4rem;
    height: 4rem;
    background-color: #3b82f6;
    color: #ffffff;
    font-size: 2rem;
}

.profile-title {
    margin-left: 1rem;
    
    h2 {
        margin: 0;
        font-size: 1.5rem;
    }
    
    .profile-type {
        color: #64748b;
        font-size: 0.9rem;
    }
}

.edit-form {
    padding: 1rem 0;
}

.form-field {
    margin-bottom: 1.5rem;
    
    label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
}

.profile-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    
    button {
        flex: 1;
    }
}
</style>