<template>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import router from '@/router';

onMounted(() => {
  setTimeout(() => {
    router.push('/courses');
  }, 100);
});
</script>

<style lang="scss" scoped>


</style>