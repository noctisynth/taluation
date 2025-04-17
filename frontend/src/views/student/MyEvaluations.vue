<template>
    <div class="evaluations-container">
        <Banner :message="bannerInfo.message" v-model:show="bannerInfo.show" :duration="bannerInfo.duration" :type="bannerInfo.type" />
        
        <div class="page-header">
            <h1>我的评价</h1>
            <div class="evaluations-summary" v-if="evaluations.length > 0">共 {{ evaluations.length }} 条评价</div>
        </div>
        
        <div v-if="loading" class="loading-container">
            <i class="pi pi-spin pi-spinner"></i>
            <p>加载中...</p>
        </div>
        
        <div v-else-if="evaluations.length > 0" class="evaluations-list">
            <div v-for="evaluation in evaluations" :key="evaluation.id" class="evaluation-card">
                <div class="evaluation-header">
                    <div class="course-name">
                        <i class="pi pi-book"></i>
                        <h3>{{ evaluation.cls }}</h3>
                    </div>
                    <div class="evaluation-rating">
                        <Rating v-model="evaluation.score" :readonly="true" :cancel="false" />
                        <span class="rating-text">{{ evaluation.score }}/5</span>
                    </div>
                </div>
                <div class="evaluation-content">
                    <div class="evaluation-comment">
                        <i class="pi pi-comment"></i>
                        <p>{{ evaluation.comment }}</p>
                    </div>
                </div>
                <div class="evaluation-actions">
                    <Button icon="pi pi-trash" class="p-button-rounded p-button-danger p-button-text" 
                           @click="confirmDelete(evaluation)" />
                </div>
            </div>
        </div>
        <div v-else class="empty-state">
            <i class="pi pi-comments"></i>
            <p>暂无评价记录</p>
            <small>您还没有对任何课程进行评价</small>
        </div>
        
        <Dialog v-model:visible="deleteDialogVisible" header="确认删除" :modal="true" :style="{width: '450px'}">
            <div>
                <i class="pi pi-exclamation-triangle" style="font-size: 2rem; color: var(--red-500)"></i>
                <span>确定要删除此评价吗？此操作不可撤销。</span>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="deleteDialogVisible = false" />
                <Button label="删除" icon="pi pi-trash" class="p-button-danger" @click="deleteEvaluationConfirmed" :loading="deleting" />
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getEvaluations, deleteEvaluation } from '@/utils/api';
import Banner from '@/components/Banner.vue';
import { BannerType } from '@/components/Banner.vue';
import Rating from 'primevue/rating';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';

interface Evaluation {
    id: string;
    user: string;
    cls: string;
    score: number;
    comment: string;
}

const evaluations = ref<Evaluation[]>([]);
const loading = ref(true);
const deleteDialogVisible = ref(false);
const deleting = ref(false);
const selectedEvaluation = ref<Evaluation | null>(null);

const bannerInfo = ref({
    message: '',
    show: false,
    duration: 3000,
    type: BannerType.Success
});

const fetchEvaluations = async () => {
    try {
        loading.value = true;
        const response = await getEvaluations({
            user_name: localStorage.getItem('username') ?? ''
        });
        if (response.success) {
            evaluations.value = response.data;
        } else {
            bannerInfo.value.message = response.message || '获取评价失败';
            bannerInfo.value.show = true;
            bannerInfo.value.type = BannerType.Error;
        }
    } catch (error: any) {
        bannerInfo.value.message = error.message || '获取评价失败';
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
    } finally {
        loading.value = false;
    }
};

const confirmDelete = (evaluation: Evaluation) => {
    selectedEvaluation.value = evaluation;
    deleteDialogVisible.value = true;
};

const deleteEvaluationConfirmed = async () => {
    if (!selectedEvaluation.value) return;
    
    try {
        deleting.value = true;
        const response = await deleteEvaluation(selectedEvaluation.value.id);
        
        if (response.success) {
            bannerInfo.value.message = '评价已成功删除';
            bannerInfo.value.show = true;
            bannerInfo.value.type = BannerType.Success;
            
            evaluations.value = evaluations.value.filter(e => e.id !== selectedEvaluation.value?.id);
        } else {
            bannerInfo.value.message = response.message || '删除评价失败';
            bannerInfo.value.show = true;
            bannerInfo.value.type = BannerType.Error;
        }
    } catch (error: any) {
        bannerInfo.value.message = error.message || '删除评价失败';
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
    } finally {
        deleting.value = false;
        deleteDialogVisible.value = false;
    }
};

onMounted(() => {
    fetchEvaluations();
});
</script>

<style scoped lang="scss">
.evaluations-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
    color: #333;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 15px;
    border-bottom: 2px solid #e9ecef;
    
    h1 {
        margin: 0;
        color: #0d4880;
        font-size: 1.8rem;
    }
    
    .evaluations-summary {
        color: #6c757d;
        font-size: 1rem;
        background-color: #f8f9fa;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 500;
    }
}

.evaluations-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
}

.evaluation-card {
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.1);
    padding: 25px;
    position: relative;
    transition: transform 0.3s, box-shadow 0.3s;
    
    &:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
}

.evaluation-header {
    margin-bottom: 20px;
    
    .course-name {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        
        i {
            color: #3b82f6;
            margin-right: 12px;
            font-size: 1.2rem;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: rgba(59, 130, 246, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        h3 {
            margin: 0;
            font-size: 1.3rem;
            color: #0d4880;
            font-weight: 600;
        }
    }
    
    .evaluation-rating {
        display: flex;
        align-items: center;
        background-color: #f8f9fa;
        padding: 8px 15px;
        border-radius: 10px;
        
        .rating-text {
            margin-left: 10px;
            font-weight: 600;
            color: #3b82f6;
        }
    }
}

.evaluation-content {
    padding: 5px 0;
    
    .evaluation-comment {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        
        i {
            color: #3b82f6;
            font-size: 1.1rem;
            margin-top: 3px;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background-color: rgba(59, 130, 246, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        p {
            margin: 0;
            color: #334155;
            line-height: 1.6;
            flex: 1;
        }
    }
}

.evaluation-actions {
    position: absolute;
    top: 20px;
    right: 20px;
    
    :deep(.p-button-rounded) {
        width: 40px;
        height: 40px;
        background-color: rgba(220, 38, 38, 0.05);
        
        &:hover {
            background-color: rgba(220, 38, 38, 0.1);
        }
        
        .pi-trash {
            font-size: 1rem;
        }
    }
}

.empty-state {
    text-align: center;
    padding: 80px 0;
    color: #6c757d;
    background-color: #f8f9fa;
    border-radius: 15px;
    margin-top: 20px;
    
    i {
        font-size: 4rem;
        margin-bottom: 20px;
        opacity: 0.5;
        color: #3b82f6;
    }
    
    p {
        font-size: 1.4rem;
        margin-bottom: 10px;
        font-weight: 500;
        color: #334155;
    }
    
    small {
        color: #94a3b8;
        font-size: 1rem;
    }
}

.loading-container {
    text-align: center;
    padding: 80px 0;
    color: #6c757d;
    
    i {
        font-size: 3rem;
        margin-bottom: 20px;
        color: #3b82f6;
    }
    
    p {
        margin: 0;
        font-size: 1.1rem;
    }
}
</style>