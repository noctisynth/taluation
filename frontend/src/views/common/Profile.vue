<template>
    <div class="profile-container">
        <Banner :message="bannerInfo.message" v-model:show="bannerInfo.show" :duration="bannerInfo.duration" :type="bannerInfo.type" />
        <Card class="profile-card" v-if="profileData.username !== ''">
            <template #header>
                <div class="profile-header">
                    <Avatar icon="pi pi-user" size="xlarge" class="profile-avatar" />
                    <div class="profile-title">
                        <h2>{{ profileData.username }}</h2>
                        <span class="profile-type">{{ userTypeText }}</span>
                    </div>
                </div>
            </template>
            <template #content>
                <div class="profile-info">
                    <div class="info-item">
                        <i class="pi pi-envelope"></i>
                        <div class="info-content">
                            <label>邮箱</label>
                            <p>{{ profileData.email }}</p>
                        </div>
                    </div>
                    <div class="info-item">
                        <i class="pi pi-phone"></i>
                        <div class="info-content">
                            <label>手机号</label>
                            <p>{{ profileData.phone }}</p>
                        </div>
                    </div>
                </div>
                <div class="profile-actions">
                    <Button icon="pi pi-pencil" label="修改资料" class="p-button-outlined p-button-secondary" @click="showEditDialog = true" />
                    <Button icon="pi pi-lock" label="修改密码" class="p-button-outlined p-button-secondary" @click="navigateToChangePassword" />
                </div>
            </template>
        </Card>

        <Dialog v-model:visible="showEditDialog" header="修改个人资料" :modal="true" class="edit-profile-dialog">
            <Form v-slot="$form" :initialValues="editFormData" :resolver="resolver" @submit="handleSubmit" class="edit-form">
                <div class="form-field">
                    <label for="newname">用户名</label>
                    <InputGroup>
                        <InputGroupAddon>
                            <i class="pi pi-user"></i>
                        </InputGroupAddon>
                        <InputText id="newname" name="newname" placeholder="请输入用户名" :feedback="false" class="w-full" />
                    </InputGroup>
                    <Message v-if="$form.newname?.invalid" severity="error" size="small" variant="simple">{{ $form.newname.error.message }}</Message>
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
                
                <div class="profile-actions">
                    <Button type="submit" label="保存" icon="pi pi-check" class="p-button-outlined p-button-secondary" />
                    <Button type="button" label="取消" icon="pi pi-times" class="p-button-outlined p-button-secondary" @click="showEditDialog = false" />
                </div>
            </Form>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { getProfile, updateProfile } from '@/utils/api';
import { ref, computed, onMounted } from 'vue';
import Card from 'primevue/card';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import { Form, type FormSubmitEvent } from '@primevue/forms';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import Banner from '@/components/Banner.vue';
import { BannerType } from '@/components/Banner.vue';
import Message from 'primevue/message';
import { useRouter } from 'vue-router';
import { z } from 'zod';

const router = useRouter();
const profileData = ref({
	username: '',
	email: '',
	phone: '',
	type: '',
});

const showEditDialog = ref(false);
const bannerInfo = ref({
	message: '',
	show: false,
	duration: 5000,
	type: BannerType.Success,
});

const editFormData = {
	newname: '',
	email: '',
	phone: '',
};

const userTypeText = computed(() => {
	const types = {
		student: '学生',
		teacher: '教师',
		admin: '管理员',
	};
	return (
		types[profileData.value.type as keyof typeof types] ||
		profileData.value.type
	);
});

const zodSchema = z.object({
	newname: z.string().min(8, { message: '用户名至少需要8个字符' }),
	email: z.string().email({ message: '请输入有效的邮箱地址' }),
	phone: z
		.string()
		.regex(/^1[3-9]\d{9}$/, { message: '请输入有效的11位手机号' })
		.length(11, { message: '手机号必须为11位' }),
});

// @ts-ignore 忽略类型实例化过深的问题
const resolver = ref(zodResolver(zodSchema));

onMounted(() => {
	fetchProfileData();
});

function fetchProfileData() {
	getProfile()
		.then((res) => {
			if (res.success) {
				profileData.value = res.data;
				editFormData.newname = res.data.username;
				editFormData.email = res.data.email;
				editFormData.phone = res.data.phone;
			} else {
				showBanner(res.message, BannerType.Error);
			}
		})
		.catch((err) => {
			showBanner(err.message, BannerType.Error);
		});
}

function handleSubmit(form: FormSubmitEvent<Record<string, any>>) {
	const data = form.values;
	const updateData = {
		username: profileData.value.username,
		newname: undefined,
		email: undefined,
		phone: undefined,
	};
	if (data.newname && data.newname !== profileData.value.username) {
		updateData.newname = data.newname;
	}
	if (data.email && data.email !== profileData.value.email) {
		updateData.email = data.email;
	}
	if (data.phone && data.phone !== profileData.value.phone) {
		updateData.phone = data.phone;
	}
	updateProfileData(updateData);
	showEditDialog.value = false;
}

function updateProfileData(data: {
	username: string;
	newname?: string;
	email?: string;
	phone?: string;
}) {
	updateProfile(data)
		.then((res) => {
			if (res.success) {
				if (data.newname) {
					showBanner('用户名更新成功, 请重新登录', BannerType.Success);
				} else {
					showBanner('个人资料更新成功', BannerType.Success);
					fetchProfileData();
				}
			} else {
				showBanner(res.message || '更新失败', BannerType.Error);
			}
		})
		.catch((err) => {
			showBanner('更新失败', BannerType.Error);
			console.error(err);
		});
}

function navigateToChangePassword() {
	router.push('/change-password');
}

function showBanner(message: string, type: BannerType) {
	bannerInfo.value = {
		message,
		show: true,
		duration: 5000,
		type,
	};
}
</script>

<style scoped lang="scss">
.profile-container {
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

.profile-info {
    padding: 1rem 0;
    
    .info-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        padding: 0.75rem;
        background-color: #f9fafb;
        border-radius: 0.5rem;
        
        i {
            color: #64748b;
            font-size: 1.25rem;
            margin-right: 1rem;
            margin-top: 0.25rem;
        }
        
        .info-content {
            flex: 1;
            
            label {
                display: block;
                color: #64748b;
                font-size: 0.85rem;
                margin-bottom: 0.25rem;
            }
            
            p {
                margin: 0;
                font-size: 1rem;
                font-weight: 500;
            }
        }
    }
}

.profile-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    
    button {
        flex: 1;
    }
}

.edit-profile-dialog {
    max-width: 500px;
    
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
        margin-top: 1rem;
        
        button {
            flex: 1;
        }
    }
}
</style>