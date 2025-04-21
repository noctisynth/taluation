<template>
    <div class="course-management-container">
        <Banner :message="bannerInfo.message" v-model:show="bannerInfo.show" :duration="bannerInfo.duration" :type="bannerInfo.type" />
        
        <div class="page-header">
            <h2 class="page-title">课程管理</h2>
            <div class="courses-summary" v-if="courses.length > 0">共 {{ courses.length }} 门课程</div>
        </div>
        
        <DataTable :value="courses" 
                  :paginator="true" 
                  :rows="10"
                  :rowsPerPageOptions="[5, 10, 20, 50]"
                  :loading="loading"
                  stripedRows
                  paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
                  currentPageReportTemplate="{first} - {last} / {totalRecords}"
                  responsiveLayout="scroll"
                  class="course-table">
            <Column field="name" header="课程名称" sortable>
                <template #body="{ data }">
                    <div class="course-name">
                        <i class="pi pi-book mr-2"></i>
                        {{ data.name }}
                    </div>
                </template>
            </Column>
            <Column field="category" header="分类" sortable></Column>
            <Column field="teacher" header="教师" sortable></Column>
            <Column field="description" header="描述">
                <template #body="{ data }">
                    <div class="course-description">
                        {{ data.description.length > 50 ? data.description.substring(0, 50) + '...' : data.description }}
                    </div>
                </template>
            </Column>
            <Column header="">
                <template #body="{ data }">
                    <div class="table-actions">
                        <Button icon="pi pi-pencil" 
                                class="p-button-rounded p-button-text p-button-info" 
                                @click="openEditDialog(data)" 
                                tooltip="编辑课程" 
                                tooltipOptions="{ position: 'top' }" />
                        <Button icon="pi pi-trash" 
                                class="p-button-rounded p-button-text p-button-danger" 
                                @click="openDeleteDialog(data)" 
                                tooltip="删除课程" 
                                tooltipOptions="{ position: 'top' }" />
                    </div>
                </template>
            </Column>
        </DataTable>
        
        <!-- 编辑课程对话框 -->
        <Dialog v-model:visible="editDialogVisible" modal header="编辑课程" :style="{width: '500px'}" class="course-form-dialog">
            <div class="course-form" v-if="selectedCourse">
                <div class="form-field">
                    <label for="editCourseName">课程名称</label>
                    <InputText id="editCourseName" v-model="editFormData.newname" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="editCourseCategory">课程分类</label>
                    <InputText id="editCourseCategory" v-model="editFormData.category" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="editCourseTeacher">教师</label>
                    <InputText id="editCourseTeacher" v-model="editFormData.teacher" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="editCourseDescription">课程描述</label>
                    <Textarea id="editCourseDescription" v-model="editFormData.description" rows="5" class="w-full" />
                </div>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="editDialogVisible = false" />
                <Button label="保存" icon="pi pi-check" @click="saveCourseChanges" :loading="submitting" />
            </template>
        </Dialog>
        
        <!-- 删除课程确认对话框 -->
        <Dialog v-model:visible="deleteDialogVisible" modal header="确认删除" :style="{width: '450px'}">
            <div class="delete-confirmation">
                <i class="pi pi-exclamation-triangle" style="font-size: 2rem; color: var(--red-500)"></i>
                <p>确定要删除课程 <strong>{{ selectedCourse?.name }}</strong> 吗？此操作不可撤销。</p>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="deleteDialogVisible = false" />
                <Button label="删除" icon="pi pi-trash" class="p-button-danger" @click="confirmDeleteCourse" :loading="deleting" />
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { getClasses, deleteClass, updateClass } from '@/utils/api';
import { ref, onMounted, reactive } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Banner from '@/components/Banner.vue';
import { BannerType } from '@/components/Banner.vue';

interface Course {
	id: string;
	name: string;
	category: string;
	description: string;
	teacher: string;
}

const courses = ref<Course[]>([]);
const loading = ref(true);
const selectedCourse = ref<Course | null>(null);

const editDialogVisible = ref(false);
const editFormData = reactive({
	name: '',
	newname: '',
	category: '',
	description: '',
	teacher: '',
});
const submitting = ref(false);

const deleteDialogVisible = ref(false);
const deleting = ref(false);

const bannerInfo = ref({
	message: '',
	show: false,
	duration: 3000,
	type: BannerType.Success,
});

onMounted(async () => {
	await loadCourses();
});

const loadCourses = async () => {
	loading.value = true;
	try {
		const response = await getClasses({});
		if (response.success) {
			courses.value = response.data;
		} else {
			showBanner(response.message, BannerType.Error);
		}
	} catch (error: any) {
		showBanner(error.message || '获取课程列表失败', BannerType.Error);
	} finally {
		loading.value = false;
	}
};

const openEditDialog = (course: Course) => {
	selectedCourse.value = course;
	editFormData.name = course.name;
	editFormData.newname = course.name;
	editFormData.category = course.category;
	editFormData.description = course.description;
	editFormData.teacher = course.teacher;
	editDialogVisible.value = true;
};

const saveCourseChanges = async () => {
	if (!selectedCourse.value) return;

	submitting.value = true;
	try {
		const updateData: {
			name: string;
			newname?: string;
			teacher?: string;
			description?: string;
			category?: string;
		} = {
			name: editFormData.name,
		};

		if (editFormData.newname !== editFormData.name) {
			updateData.newname = editFormData.newname;
		}

		if (editFormData.category !== selectedCourse.value.category) {
			updateData.category = editFormData.category;
		}

		if (editFormData.description !== selectedCourse.value.description) {
			updateData.description = editFormData.description;
		}

		if (editFormData.teacher !== selectedCourse.value.teacher) {
			updateData.teacher = editFormData.teacher;
		}

		const response = await updateClass(updateData);

		if (response.success) {
			showBanner('课程信息更新成功', BannerType.Success);
			editDialogVisible.value = false;
			await loadCourses();
		} else {
			showBanner(response.message, BannerType.Error);
		}
	} catch (error: any) {
		showBanner(error.message || '更新课程信息失败', BannerType.Error);
	} finally {
		submitting.value = false;
	}
};

const openDeleteDialog = (course: Course) => {
	selectedCourse.value = course;
	deleteDialogVisible.value = true;
};

const confirmDeleteCourse = async () => {
	if (!selectedCourse.value) return;

	deleting.value = true;
	try {
		const response = await deleteClass({
			name: selectedCourse.value.name,
		});
		if (response.success) {
			showBanner('课程删除成功', BannerType.Success);
			deleteDialogVisible.value = false;
			await loadCourses();
		} else {
			showBanner(response.message, BannerType.Error);
		}
	} catch (error: any) {
		showBanner(error.message || '删除课程失败', BannerType.Error);
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
.course-management-container {
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

.courses-summary {
    color: #6c757d;
    font-size: 1rem;
    background-color: #f8f9fa;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: 500;
}

.course-table {
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

.course-name {
    display: flex;
    align-items: center;
    gap: 8px;
}

.course-description {
    max-width: 300px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
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