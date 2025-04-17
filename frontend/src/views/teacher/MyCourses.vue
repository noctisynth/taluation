<template>
    <div class="courses-container">
        <Banner :message="bannerInfo.message" v-model:show="bannerInfo.show" :duration="bannerInfo.duration" :type="bannerInfo.type" />
        
        <div class="page-header">
            <h2 class="courses-title">我的课程</h2>
            <div class="actions">
                <div class="courses-summary" v-if="courses.length > 0">共 {{ courses.length }} 门课程</div>
                <Button label="添加课程" icon="pi pi-plus" class="" @click="openAddCourseDialog" />
            </div>
        </div>
        
        <div class="courses-grid" v-if="courses.length > 0">
            <Card v-for="course in courses" :key="course.name" class="course-card">
                <template #header>
                    <div class="course-header">
                        <div class="course-title-row">
                            <h3>{{ course.name }}</h3>
                            <div class="general-tag">{{ course.category }}</div>
                        </div>
                    </div>
                </template>
                <template #content>
                    <div class="course-info">
                        <div class="info-item">
                            <i class="pi pi-user"></i>
                            <div class="info-content">
                                <label>教师</label>
                                <p>{{ course.teacher }}</p>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="pi pi-info-circle"></i>
                            <div class="info-content">
                                <label>描述</label>
                                <p>{{ course.description }}</p>
                            </div>
                        </div>
                        <div class="view-details">
                            <Button label="编辑" icon="pi pi-pencil" class="p-button-text p-button-secondary" 
                                  @click.stop="openEditCourseDialog(course)" />
                            <Button label="查看详细" icon="pi pi-external-link" class="p-button-text" 
                                  @click.stop="openCourseDetails(course)" />
                        </div>
                    </div>
                </template>
            </Card>
        </div>
        
        <div class="empty-state" v-else>
            <i class="pi pi-book"></i>
            <p>暂无课程信息</p>
        </div>

        <!-- 课程详情对话框 -->
        <Dialog v-model:visible="courseDetailsVisible" modal :header="selectedCourse?.name || '课程详情'" :style="{width: '90vw'}" class="course-details-dialog">
            <div v-if="selectedCourse" class="course-details-content">
                <TabView>
                    <TabPanel header="统计信息" value="stats">
                        <div class="stats-container">
                            <div class="stats-summary">
                                <div class="stat-card">
                                    <h3>平均评分</h3>
                                    <div class="stat-value">{{ courseStats.average ? courseStats.average.toFixed(1) : '暂无' }}</div>
                                    <div class="rating-display">
                                        <Rating v-model="courseStats.average" :readonly="true" :cancel="false" />
                                        <span class="rating-text">{{ courseStats.average ? courseStats.average.toFixed(1) : '0' }}/5</span>
                                    </div>
                                </div>
                                <div class="stat-card">
                                    <h3>评价数量</h3>
                                    <div class="stat-value">{{ courseStats.count }}</div>
                                    <div class="stat-icon"><i class="pi pi-comments"></i></div>
                                </div>
                                <div class="stat-card">
                                    <h3>最高评分</h3>
                                    <div class="stat-value">{{ courseStats.max }}</div>
                                    <div class="stat-icon"><i class="pi pi-arrow-up"></i></div>
                                </div>
                                <div class="stat-card">
                                    <h3>最低评分</h3>
                                    <div class="stat-value">{{ courseStats.min }}</div>
                                    <div class="stat-icon"><i class="pi pi-arrow-down"></i></div>
                                </div>
                            </div>
                            
                            <div class="stats-chart" v-if="evaluations.length > 0">
                                <VChart :option="chartOption" style="height: 400px" />
                            </div>
                        </div>
                    </TabPanel>
                    <TabPanel header="评价列表" value="evaluations">
                        <div class="evaluations-list">
                        
                            <div v-if="evaluations.length > 0" class="evaluation-cards">
                                <div v-for="(evaluation, index) in evaluations" :key="index" class="evaluation-card">
                                    <div class="evaluation-header">
                                        <div class="evaluation-rating">
                                            <Rating v-model="evaluation.score" :readonly="true" :cancel="false" />
                                        </div>
                                        <div class="evaluation-user">
                                            <i class="pi pi-user"></i> {{ evaluation.user }}
                                        </div>
                                    </div>
                                    <div class="evaluation-content">
                                        <div class="evaluation-comment">
                                            <i class="pi pi-comment"></i>
                                            <p>{{ evaluation.comment }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="empty-evaluations">
                                <i class="pi pi-comments"></i>
                                <p>暂无评价</p>
                            </div>
                        </div>
                    </TabPanel>
                </TabView>
            </div>
        </Dialog>

        <!-- 添加课程对话框 -->
        <Dialog v-model:visible="addCourseVisible" modal header="添加新课程" :style="{width: '500px'}" class="course-form-dialog">
            <div class="course-form">
                <div class="form-field">
                    <label for="courseName">课程名称</label>
                    <InputText id="courseName" v-model="newCourse.name" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="courseCategory">课程分类</label>
                    <InputText id="courseCategory" v-model="newCourse.category" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="courseDescription">课程描述</label>
                    <Textarea id="courseDescription" v-model="newCourse.description" rows="5" class="w-full" />
                </div>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="addCourseVisible = false" />
                <Button label="添加" icon="pi pi-check" :loading="submitting" @click="submitAddCourse" />
            </template>
        </Dialog>
        
        <!-- 编辑课程对话框 -->
        <Dialog v-model:visible="editCourseVisible" modal header="编辑课程" :style="{width: '500px'}" class="course-form-dialog">
            <div class="course-form" v-if="editingCourse">
                <div class="form-field">
                    <label for="editCourseName">课程名称</label>
                    <InputText id="editCourseName" v-model="editingCourse.newname" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="editCourseCategory">课程分类</label>
                    <InputText id="editCourseCategory" v-model="editingCourse.category" class="w-full" />
                </div>
                <div class="form-field">
                    <label for="editCourseDescription">课程描述</label>
                    <Textarea id="editCourseDescription" v-model="editingCourse.description" rows="5" class="w-full" />
                </div>
            </div>
            <template #footer>
                <Button label="取消" icon="pi pi-times" class="p-button-text" @click="editCourseVisible = false" />
                <Button label="保存" icon="pi pi-check" :loading="submitting" @click="submitEditCourse" />
            </template>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import Banner from '@/components/Banner.vue';
import { getClasses, getEvaluationStats, getEvaluations, updateClass, addClass } from '@/utils/api';
import { ref, onMounted, reactive, computed } from 'vue';
import { BannerType } from '@/components/Banner.vue';
import Card from 'primevue/card';
import Dialog from 'primevue/dialog';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Rating from 'primevue/rating';
import Button from 'primevue/button';
import Textarea from 'primevue/textarea';
import InputText from 'primevue/inputtext';
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import { GridComponent, TooltipComponent, TitleComponent } from "echarts/components";
import VChart from "vue-echarts";


interface Course {
    id: string;
    name: string;
    category: string;
    description: string;
    teacher: string;
}

interface Evaluation {
    id: string;
    user: string;
    cls: string;
    score: number;
    comment: string;
}

interface CourseStats {
    count: number;
    average: number;
    max: number;
    min: number;
    class_id: string;
    class_name: string;
    distribution: {[key: string]: number};
}

const courses = ref<Course[]>([]);
const selectedCourse = ref<Course | null>(null);
const courseDetailsVisible = ref(false);
const evaluations = ref<Evaluation[]>([]);
const courseStats = reactive<CourseStats>({
    count: 0,
    average: 0,
    max: 0,
    min: 0,
    class_id: '',
    class_name: '',
    distribution: {}
});

const userType = ref(localStorage.getItem('user_type'));
const isStudent = computed(() => userType.value === 'student');

const showAddEvaluationForm = ref(false);
const submitting = ref(false);
const newEvaluation = reactive({
    score: 5,
    comment: ''
});

const chartOption = computed(() => {
    const data = [
        courseStats.distribution['1'] || 0,
        courseStats.distribution['2'] || 0,
        courseStats.distribution['3'] || 0,
        courseStats.distribution['4'] || 0,
        courseStats.distribution['5'] || 0
    ];
    
    return {
        title: {
            text: '评分分布',
            left: 'center',
            textStyle: {
                fontSize: 14,
                color: '#6c757d'
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['1分', '2分', '3分', '4分', '5分'],
            axisTick: {
                alignWithLabel: true
            }
        },
        yAxis: {
            type: 'value',
            minInterval: 1
        },
        series: [
            {
                name: '评价数',
                type: 'bar',
                barWidth: '60%',
                data: data,
                itemStyle: {
                    color: '#60a5fa'
                }
            }
        ]
    };
});

const bannerInfo = ref({
    message: '',
    show: false,
    type: BannerType.Success,
    duration: 3000
});

const addCourseVisible = ref(false);
const newCourse = reactive({
    name: '',
    category: '',
    description: '',
    teacher: localStorage.getItem('username') || ''
});

const editCourseVisible = ref(false);
const editingCourse = ref<{
    name: string;
    newname?: string;
    category?: string;
    description?: string;
} | null>(null);

const openCourseDetails = async (course: Course) => {
    selectedCourse.value = course;
    courseDetailsVisible.value = true;
    
    try {
        const evalResponse = await getEvaluations({ class_id: course.id });
        if (evalResponse.success) {
            evaluations.value = evalResponse.data;
        }
        
        const statsResponse = await getEvaluationStats({ class_id: course.id });
        if (statsResponse.success) {
            Object.assign(courseStats, statsResponse.data);
        }
    } catch (err: any) {
        bannerInfo.value.message = err.message;
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
    }
};

const openAddCourseDialog = () => {
    newCourse.name = '';
    newCourse.category = '';
    newCourse.description = '';
    addCourseVisible.value = true;
};

const submitAddCourse = async () => {
    if (!newCourse.name || !newCourse.category) {
        bannerInfo.value.message = '课程名称和分类不能为空';
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
        return;
    }
    
    submitting.value = true;
    try {
        const res = await addClass(newCourse);
        if (res.success) {
            bannerInfo.value.message = '课程添加成功';
            bannerInfo.value.show = true;
            bannerInfo.value.type = BannerType.Success;
            addCourseVisible.value = false;
            
            const classesRes = await getClasses({
                teacher: localStorage.getItem('username') ?? undefined
            });
            if (classesRes.success) {
                courses.value = classesRes.data;
            }
        } else {
            bannerInfo.value.message = res.message || '添加失败';
            bannerInfo.value.show = true;
            bannerInfo.value.type = BannerType.Error;
        }
    } catch (err: any) {
        bannerInfo.value.message = err.message || '添加失败';
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
    } finally {
        submitting.value = false;
    }
};

const openEditCourseDialog = (course: Course) => {
    editingCourse.value = {
        name: course.name,
        newname: course.name,
        category: course.category,
        description: course.description
    };
    editCourseVisible.value = true;
};

const submitEditCourse = async () => {
    if (!editingCourse.value || !editingCourse.value.newname || !editingCourse.value.category) {
        bannerInfo.value.message = '课程名称和分类不能为空';
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
        return;
    }
    
    const originalCourse = courses.value.find(c => c.name === editingCourse.value?.name);
    if (!originalCourse) {
        bannerInfo.value.message = '找不到原始课程信息';
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
        return;
    }
    
    const updateData: {
        name: string;
        newname?: string;
        category?: string;
        description?: string;
    } = {
        name: editingCourse.value.name
    };
    
    if (editingCourse.value.newname !== originalCourse.name) {
        updateData.newname = editingCourse.value.newname;
    }
    
    if (editingCourse.value.category !== originalCourse.category) {
        updateData.category = editingCourse.value.category;
    }
    
    if (editingCourse.value.description !== originalCourse.description) {
        updateData.description = editingCourse.value.description;
    }
    
    const hasOnlyNameChange = Object.keys(updateData).length === 2 && updateData.newname;
    const hasNoChanges = Object.keys(updateData).length === 1;
    
    if (hasNoChanges || hasOnlyNameChange) {
        bannerInfo.value.message = '未检测到需要更新的信息';
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Info;
        editCourseVisible.value = false;
        return;
    }
    
    submitting.value = true;
    try {
        const res = await updateClass(updateData);
        if (res.success) {
            bannerInfo.value.message = '课程更新成功';
            bannerInfo.value.show = true;
            bannerInfo.value.type = BannerType.Success;
            editCourseVisible.value = false;
            
            const classesRes = await getClasses({
                teacher: localStorage.getItem('username') ?? undefined
            });
            if (classesRes.success) {
                courses.value = classesRes.data;
            }
        } else {
            bannerInfo.value.message = res.message || '更新失败';
            bannerInfo.value.show = true;
            bannerInfo.value.type = BannerType.Error;
        }
    } catch (err: any) {
        bannerInfo.value.message = err.message || '更新失败';
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
    } finally {
        submitting.value = false;
    }
};

onMounted(() => {
    getClasses({
        teacher: localStorage.getItem('username') ?? undefined
    }).then(res => {
        if (res.success) {
            courses.value = res.data;
        } else {
            bannerInfo.value.message = res.message;
            bannerInfo.value.show = true;
            bannerInfo.value.type = BannerType.Error;
        }
    }).catch(err => {
        bannerInfo.value.message = err.message;
        bannerInfo.value.show = true;
        bannerInfo.value.type = BannerType.Error;
    });
});
</script>

<style scoped lang="scss">
.courses-container {
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

.courses-title {
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

.courses-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
}

.course-card {
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    overflow: hidden;
    
    &:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    :deep(.p-card-body) {
        padding: 0;
    }
    
    :deep(.p-card-content) {
        padding: 1rem;
    }
}

.course-header {
    padding: 20px;
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    
    h3 {
        margin: 0;
        font-size: 1.5rem;
        color: #0d4880;
        font-weight: 600;
    }
}

.course-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.course-info {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.info-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    
    i {
        color: #3b82f6;
        font-size: 1.2rem;
        margin-top: 3px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: rgba(59, 130, 246, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .info-content {
        flex: 1;
        
        label {
            color: #6c757d;
            font-size: 0.85rem;
            display: block;
            margin-bottom: 4px;
            font-weight: 500;
        }
        
        p {
            margin: 0;
            color: #212529;
            line-height: 1.5;
        }
    }
}

.view-details {
    display: flex;
    justify-content: flex-end;
    margin-top: 15px;
    padding-top: 12px;
    border-top: 1px solid #e9ecef;
    
    :deep(.p-button-text) {
        color: #3b82f6;
        font-weight: 500;
        
        &:hover {
            background-color: rgba(59, 130, 246, 0.08);
        }
        
        .p-button-icon {
            font-size: 0.9rem;
        }
    }
}

.empty-state {
    text-align: center;
    padding: 80px 0;
    color: #6c757d;
    
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
    }
}

.course-details-dialog {
    :deep(.p-dialog-header) {
        background-color: #f8f9fa;
        border-bottom: 1px solid #e9ecef;
    }
    
    :deep(.p-dialog-content) {
        max-height: 80vh;
        overflow-y: auto;
        padding: 0;
    }
}

.course-details-content {
    :deep(.p-tabview-nav) {
        background-color: #f8f9fa;
        border-bottom: 1px solid #e9ecef;
        padding: 0 1rem;
        
        li {
            margin-right: 10px;
            
            .p-tabview-nav-link {
                padding: 1rem 1.5rem;
                color: #6c757d;
                font-weight: 500;
                border: none;
                border-radius: 0;
                
                &:hover {
                    background-color: transparent;
                    color: #3b82f6;
                    border-bottom: 2px solid rgba(59, 130, 246, 0.3);
                }
            }
            
            &.p-highlight .p-tabview-nav-link {
                color: #3b82f6;
                border-bottom: 2px solid #3b82f6;
            }
        }
    }
    
    :deep(.p-tabview-panels) {
        padding: 2rem;
    }
}

.stats-container {
    display: flex;
    flex-direction: column;
    gap: 40px;
}

.stats-summary {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 25px;
}

.stat-card {
    background-color: #fff;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    position: relative;
    overflow: hidden;
    
    &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(to right, #60a5fa, #3b82f6);
    }
    
    h3 {
        margin: 0 0 15px 0;
        color: #6c757d;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0d4880;
        margin-bottom: 10px;
    }
    
    .rating-display {
        display: flex;
        align-items: center;
        gap: 10px;
        
        .rating-text {
            font-weight: 500;
            color: #6c757d;
        }
    }
    
    .stat-icon {
        position: absolute;
        top: 20px;
        right: 20px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: rgba(59, 130, 246, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        
        i {
            color: #3b82f6;
            font-size: 1.2rem;
        }
    }
}

.stats-chart {
    background-color: #fff;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}

.evaluations-list {
    padding: 10px 0;
}

.evaluation-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 25px;
}

.evaluation-card {
    background-color: #fff;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    position: relative;
    transition: transform 0.2s, box-shadow 0.2s;
    
    &:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.12);
    }
}

.evaluation-header {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 15px;
    
    .evaluation-user {
        color: #6c757d;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
        
        i {
            color: #3b82f6;
            font-size: 0.9rem;
        }
    }
}

.evaluation-content {
    .evaluation-comment {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-top: 5px;
        
        i {
            color: #3b82f6;
            font-size: 1rem;
            margin-top: 3px;
        }
        
        p {
            margin: 0;
            color: #212529;
            line-height: 1.6;
            flex: 1;
        }
    }
}

.empty-evaluations {
    text-align: center;
    padding: 50px 0;
    color: #6c757d;
    
    i {
        font-size: 3rem;
        margin-bottom: 15px;
        opacity: 0.5;
        color: #3b82f6;
    }
    
    p {
        font-size: 1.2rem;
        margin-bottom: 5px;
        font-weight: 500;
    }
    
    small {
        color: #adb5bd;
    }
}

.add-evaluation-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 25px;
}

.add-evaluation-form {
    padding: 10px;
    
    .form-field {
        margin-bottom: 20px;
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #495057;
        }
        
        .rating-input {
            display: flex;
            align-items: center;
            gap: 10px;
            
            .rating-value {
                font-weight: 500;
                color: #3b82f6;
            }
        }
    }
}

.empty-action {
    margin-top: 20px;
}

.actions {
    display: flex;
    align-items: center;
    gap: 15px;
}

.course-form-dialog {
    :deep(.p-dialog-header) {
        background-color: #f8f9fa;
        border-bottom: 1px solid #e9ecef;
    }
}

.course-form {
    padding: 20px 10px;
    
    .form-field {
        margin-bottom: 20px;
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #495057;
        }
    }
}
</style>