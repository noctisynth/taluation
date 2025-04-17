<template>
    <div class="user-management-container">
        <Banner :message="bannerInfo.message" v-model:show="bannerInfo.show" :duration="bannerInfo.duration" :type="bannerInfo.type" />
        
        <div class="page-header">
            <h2 class="page-title">用户管理</h2>
            <div class="users-summary" v-if="users.length > 0">共 {{ users.length }} 个用户</div>
        </div>
        
        <DataTable :value="users" 
                  :paginator="true" 
                  :rows="10"
                  :rowsPerPageOptions="[5, 10, 20, 50]"
                  :loading="loading"
                  stripedRows
                  paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
                  currentPageReportTemplate="{first} - {last} / {totalRecords}"
                  responsiveLayout="scroll"
                  class="user-table">
            <Column field="username" header="用户名" sortable>
                <template #body="{ data }">
                    <div class="user-name">
                        <Avatar :label="data.username.charAt(0).toUpperCase()" shape="circle" class="mr-2" />
                        {{ data.username }}
                    </div>
                </template>
            </Column>
            <Column field="email" header="邮箱" sortable></Column>
            <Column field="phone" header="手机号" sortable></Column>
            <Column field="type" header="用户类型" sortable>
                <template #body="{ data }">
                    <div class="general-tag">{{ data.type }}</div>
                </template>
            </Column>
            <Column header="">
                <template #body="{ data }">
                    <div class="table-actions">
                        <Button icon="pi pi-pencil" 
                                class="p-button-rounded p-button-text p-button-info" 
                                @click="openEditDialog(data)" 
                                tooltip="编辑用户" 
                                tooltipOptions="{ position: 'top' }" />
                        <Button icon="pi pi-trash" 
                                class="p-button-rounded p-button-text p-button-danger" 
                                @click="openDeleteDialog(data)" 
                                tooltip="删除用户" 
                                tooltipOptions="{ position: 'top' }" />
                    </div>
                </template>
            </Column>
        </DataTable>
        
        <!-- 编辑用户对话框 -->
        <Dialog v-model:visible="editDialogVisible" modal header="编辑用户" :style="{width: '500px'}" class="user-form-dialog">
            <div class="user-form" v-if="selectedUser">
                <div class="form-field">
                    <label for="editUsername">用户名</label>
                    <InputText id="editUsername" v-model="editFormData.newname" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="editEmail">邮箱</label>
                    <InputText id="editEmail" v-model="editFormData.email" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="editPhone">手机号</label>
                    <InputText id="editPhone" v-model="editFormData.phone" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="editType">用户类型</label>
                    <Dropdown id="editType" v-model="editFormData.type" :options="userTypes" optionLabel="label" optionValue="value" class="w-full" />
                </div>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="editDialogVisible = false" />
                <Button label="保存" icon="pi pi-check" @click="saveUserChanges" :loading="submitting" />
            </template>
        </Dialog>
        
        <!-- 删除用户确认对话框 -->
        <Dialog v-model:visible="deleteDialogVisible" modal header="确认删除" :style="{width: '450px'}">
            <div class="delete-confirmation">
                <i class="pi pi-exclamation-triangle" style="font-size: 2rem; color: var(--red-500)"></i>
                <p>确定要删除用户 <strong>{{ selectedUser?.username }}</strong> 吗？此操作不可撤销。</p>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="deleteDialogVisible = false" />
                <Button label="删除" icon="pi pi-trash" class="p-button-danger" @click="confirmDeleteUser" :loading="deleting" />
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { getUsers, updateProfile, deleteUser } from '@/utils/api';
import { ref, onMounted, reactive } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Avatar from 'primevue/avatar';
import Banner from '@/components/Banner.vue';
import { BannerType } from '@/components/Banner.vue';

interface User {
    id: string;
    username: string;
    email: string;
    phone: string;
    type: string;
}

const users = ref<User[]>([]);
const loading = ref(true);
const selectedUser = ref<User | null>(null);

const editDialogVisible = ref(false);
const editFormData = reactive({
    username: '',
    newname: '',
    email: '',
    phone: '',
    type: ''
});
const submitting = ref(false);

const deleteDialogVisible = ref(false);
const deleting = ref(false);

const bannerInfo = ref({
    message: '',
    show: false,
    duration: 3000,
    type: BannerType.Success
});

const userTypes = [
    { label: '学生', value: 'student' },
    { label: '教师', value: 'teacher' },
    { label: '管理员', value: 'admin' }
];

onMounted(async () => {
    await loadUsers();
});

const loadUsers = async () => {
    loading.value = true;
    try {
        const response = await getUsers();
        if (response.success) {
            users.value = response.data;
        } else {
            showBanner(response.message, BannerType.Error);
        }
    } catch (error: any) {
        showBanner(error.message || '获取用户列表失败', BannerType.Error);
    } finally {
        loading.value = false;
    }
};

const openEditDialog = (user: User) => {
    selectedUser.value = user;
    editFormData.username = user.username;
    editFormData.newname = user.username;
    editFormData.email = user.email;
    editFormData.phone = user.phone;
    editFormData.type = user.type;
    editDialogVisible.value = true;
};

const saveUserChanges = async () => {
    if (!selectedUser.value) return;
    
    submitting.value = true;
    try {
        const response = await updateProfile({
            username: editFormData.username,
            newname: editFormData.newname !== editFormData.username ? editFormData.newname : undefined,
            email: editFormData.email,
            phone: editFormData.phone,
            type: editFormData.type
        });
        
        if (response.success) {
            showBanner('用户信息更新成功', BannerType.Success);
            editDialogVisible.value = false;
            await loadUsers();
        } else {
            showBanner(response.message, BannerType.Error);
        }
    } catch (error: any) {
        showBanner(error.message || '更新用户信息失败', BannerType.Error);
    } finally {
        submitting.value = false;
    }
};

const openDeleteDialog = (user: User) => {
    selectedUser.value = user;
    deleteDialogVisible.value = true;
};

const confirmDeleteUser = async () => {
    if (!selectedUser.value) return;
    
    deleting.value = true;
    try {
        const response = await deleteUser(selectedUser.value.username);
        if (response.success) {
            showBanner('用户删除成功', BannerType.Success);
            deleteDialogVisible.value = false;
            await loadUsers();
        } else {
            showBanner(response.message, BannerType.Error);
        }
    } catch (error: any) {
        showBanner(error.message || '删除用户失败', BannerType.Error);
    } finally {
        deleting.value = false;
    }
};

const showBanner = (message: string, type: BannerType) => {
    bannerInfo.value.message = message;
    bannerInfo.value.type = type;
    bannerInfo.value.show = true;
};
</script>

<style scoped lang="scss">
.user-management-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    color: #333;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 2px solid #e9ecef;
}

.page-title {
    font-size: 1.8rem;
    color: #0d4880;
    margin: 0;
}

.users-summary {
    color: #6c757d;
    font-size: 1rem;
    background-color: #f8f9fa;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: 500;
}

.user-table {
    background: white;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    
    :deep(.p-datatable-header) {
        background-color: #f8f9fa;
        border-bottom: 1px solid #e9ecef;
    }
    
    :deep(.p-datatable-thead > tr > th) {
        background-color: #f8f9fa;
        color: #495057;
        font-weight: 600;
        padding: 1rem;
    }
    
    :deep(.p-datatable-tbody > tr) {
        transition: background-color 0.2s;
        
        &:hover {
            background-color: #f8f9fa;
        }
    }
    
    :deep(.p-datatable-tbody > tr > td) {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e9ecef;
    }
}

.user-name {
    display: flex;
    align-items: center;
    gap: 8px;
}

.table-actions {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;
}

.form-field {
    margin-bottom: 20px;
    
    label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: #495057;
    }
}

.delete-confirmation {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    text-align: center;
    padding: 20px 0;
    
    p {
        margin: 0;
        font-size: 1.1rem;
        line-height: 1.5;
    }
}
</style>