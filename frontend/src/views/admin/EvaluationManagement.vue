<template>
    <div class="evaluation-management-container">
        <Banner :message="bannerInfo.message" v-model:show="bannerInfo.show" :duration="bannerInfo.duration" :type="bannerInfo.type" />
        
        <div class="page-header">
            <h2 class="page-title">评价管理</h2>
            <div class="evaluations-summary" v-if="evaluations.length > 0">共 {{ evaluations.length }} 个评价</div>
        </div>
        
        <DataTable :value="evaluations" 
                  :paginator="true" 
                  :rows="10"
                  :rowsPerPageOptions="[5, 10, 20, 50]"
                  :loading="loading"
                  stripedRows
                  paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
                  currentPageReportTemplate="{first} - {last} / {totalRecords}"
                  responsiveLayout="scroll"
                  class="evaluation-table">
            <Column field="id" header="ID"></Column>
            <Column field="user" header="用户" sortable></Column>
            <Column field="cls" header="课程" sortable></Column>
            <Column field="score" header="评分" sortable>
                <template #body="{ data }">
                    <Rating :modelValue="data.score" readonly :cancel="false" />
                </template>
            </Column>
            <Column field="comment" header="评价内容" sortable></Column>
            <Column header="">
                <template #body="{ data }">
                    <div class="table-actions">
                        <Button icon="pi pi-trash" 
                                class="p-button-rounded p-button-text p-button-danger" 
                                @click="openDeleteDialog(data)" 
                                tooltip="删除评价" 
                                tooltipOptions="{ position: 'top' }" />
                    </div>
                </template>
            </Column>
        </DataTable>
        
        <!-- 删除评价确认对话框 -->
        <Dialog v-model:visible="deleteDialogVisible" modal header="确认删除" :style="{width: '450px'}">
            <div class="delete-confirmation">
                <i class="pi pi-exclamation-triangle" style="font-size: 2rem; color: var(--red-500)"></i>
                <p>确定要删除此评价吗？此操作不可撤销。</p>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="deleteDialogVisible = false" />
                <Button label="删除" icon="pi pi-trash" class="p-button-danger" @click="confirmDeleteEvaluation" :loading="deleting" />
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { getEvaluations, deleteEvaluation } from '@/utils/api';
import { ref, onMounted } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Rating from 'primevue/rating';
import Banner from '@/components/Banner.vue';
import { BannerType } from '@/components/Banner.vue';

interface Evaluation {
	id: string;
	user: string;
	cls: string;
	score: number;
	comment: string;
}

const evaluations = ref<Evaluation[]>([]);
const loading = ref(true);
const selectedEvaluation = ref<Evaluation | null>(null);

const deleteDialogVisible = ref(false);
const deleting = ref(false);

const bannerInfo = ref({
	message: '',
	show: false,
	duration: 3000,
	type: BannerType.Success,
});

onMounted(async () => {
	await loadEvaluations();
});

const loadEvaluations = async () => {
	loading.value = true;
	try {
		const response = await getEvaluations({});
		if (response.success) {
			evaluations.value = response.data;
		} else {
			showBanner(response.message, BannerType.Error);
		}
	} catch (error: any) {
		showBanner(error.message || '获取评价列表失败', BannerType.Error);
	} finally {
		loading.value = false;
	}
};

const openDeleteDialog = (evaluation: Evaluation) => {
	selectedEvaluation.value = evaluation;
	deleteDialogVisible.value = true;
};

const confirmDeleteEvaluation = async () => {
	if (!selectedEvaluation.value) return;

	deleting.value = true;
	try {
		const response = await deleteEvaluation(selectedEvaluation.value.id);
		if (response.success) {
			showBanner('评价删除成功', BannerType.Success);
			deleteDialogVisible.value = false;
			await loadEvaluations();
		} else {
			showBanner(response.message, BannerType.Error);
		}
	} catch (error: any) {
		showBanner(error.message || '删除评价失败', BannerType.Error);
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
.evaluation-management-container {
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

.evaluations-summary {
    color: #6c757d;
    font-size: 1rem;
    background-color: #f8f9fa;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: 500;
}

.evaluation-table {
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

.table-actions {
    display: flex;
    gap: 8px;
    justify-content: center;
    align-items: center;
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