<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import { getAnnounce, addAnnounce } from '@/utils/api'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Textarea from 'primevue/textarea'

const showDialog = ref(false)

const userType = ref(localStorage.getItem('user_type'));

const changeAnnounce = async () => {
   const response = await addAnnounce(announce.value)
    if (response.status === 200) {
         showDialog.value = false
         announce.value = response.data || ''
    } else {
         console.error('Failed to update announcement:', response.statusText)
    }
    showDialog.value = false
}

const announce = ref('')
onMounted(async () => {
    const response = await getAnnounce()
    if (response.status === 200) {
        announce.value = response.data || ''
    } else {
        console.error('Failed to fetch announcement:', response.statusText)
    }
    if (announce.value === '') {
        announce.value = '暂无公告'
    }
})
</script>

<template>
    <div class="container">
        <Card class="card">
            <template #header>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <h2 class="title">公告</h2>
                    <Button v-if="userType === 'admin'" @click="showDialog = !showDialog" icon="pi pi-pencil" size="small" style="margin-right: 1.5rem"></Button>
                </div>
            </template>
            <template #content>
                <div class="announce-content">
                    <p>{{ announce }}</p>
                </div>
            </template>
        </Card>
        <Dialog v-model:visible="showDialog" header="公告" :modal="true" class="edit-profile-dialog">
            <div class="form-field">
                <label for="announce">公告内容</label>
                <Textarea id="announce" v-model="announce" rows="10" cols="50"></Textarea>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                <Button type="button" icon="pi pi-times" label="取消" class="p-button-outlined p-button-secondary" @click="showDialog = false" />
                <Button type="button" icon="pi pi-check" label="保存" @click="changeAnnounce" />
            </div>
        </Dialog>
    </div>
</template>

<style scoped lang="scss">
.container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.card {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-radius: 0.5rem;
    padding-left: 1.5rem;
}

.title {
    font-size: 1.5rem;
    color: #0d4880;
}
</style>