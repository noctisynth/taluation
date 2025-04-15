<template>
  <transition name="fade">
    <div v-if="show" :class="[`banner`, `banner-${type}`]">
      <i :class="iconClass"></i> {{ message }}
    </div>
  </transition>
</template>

<script lang="ts">
export enum BannerType {
  Error = 'error',
  Info = 'info',
  Success = 'success',
  Warning = 'warning'
}
</script>

<script setup lang="ts">
import { watch, computed } from 'vue';

const props = defineProps<{
  message: string;
  show: boolean;
  type: BannerType;
  duration?: number;
}>();

const emit = defineEmits(['update:show']);

const iconClass = computed(() => {
  switch (props.type) {
    case 'error':
      return 'pi pi-exclamation-triangle';
    case 'info':
      return 'pi pi-info-circle';
    case 'success':
      return 'pi pi-check-circle';
    case 'warning':
      return 'pi pi-exclamation-triangle';
    default:
      return 'pi pi-info-circle';
  }
});

watch(() => props.show, (newVal) => {
  if (newVal && props.duration) {
    setTimeout(() => {
      emit('update:show', false);
    }, props.duration);
  }
});
</script>

<style scoped lang="scss">
.banner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 0.75rem;
  text-align: center;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-size: 0.95rem;
  
  i {
    margin-right: 0.5rem;
  }
}

.banner-error {
  background: linear-gradient(to right, #f87171, #fb7185);
  color: white;
}

.banner-info {
  background: linear-gradient(to right, #60a5fa, #3b82f6);
  color: white;
}

.banner-success {
  background: linear-gradient(to right, #4ade80, #22c55e);
  color: white;
}

.banner-warning {
  background: linear-gradient(to right, #fbbf24, #f59e0b);
  color: #422006;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}
</style> 