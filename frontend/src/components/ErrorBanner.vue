<template>
  <transition name="fade">
    <div v-if="show" class="error-banner">
      <i class="pi pi-exclamation-triangle"></i> {{ message }}
    </div>
  </transition>
</template>

<script setup lang="ts">
import { watch } from 'vue';

const props = defineProps<{
  message: string;
  show: boolean;
  duration?: number;
}>();

const emit = defineEmits(['update:show']);

watch(() => props.show, (newVal) => {
  if (newVal && props.duration) {
    setTimeout(() => {
      emit('update:show', false);
    }, props.duration);
  }
});
</script>

<style scoped lang="scss">
.error-banner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #f87171;
  background: linear-gradient(to right, #f87171, #fb7185);
  color: white;
  padding: 0.75rem;
  text-align: center;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-size: 0.95rem;
  
  i {
    margin-right: 0.5rem;
  }
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
