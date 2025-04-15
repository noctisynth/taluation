<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import request  from '@/utils/request';
import Button from 'primevue/button';

const router = useRouter();
const route = useRoute();
const username = ref(localStorage.getItem('username') || '用户');

const isAuthenticated = computed(() => {
  const token = localStorage.getItem('token');
  const storedUsername = localStorage.getItem('username');
  return !!(token && storedUsername);
});

const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/register';
});

const type = computed(() => {
  request.get('/account', {}).then(res => {
    if (res.data.success) {
      return res.data.data.type;
    } else {
      return 'none';
    }
  }).catch(_ => {
    return 'none';
  });
});

function logout() {
  request.get('/account/logout').then(() => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    router.push('/login');
  });
}

onMounted(() => {
  window.addEventListener('login-success', handleLoginSuccess);
});

const forceRefresh = ref(0);

function handleLoginSuccess() {
  nextTick(() => {
    forceRefresh.value++;
  });
}
</script>

<template>
    <template v-if="isAuthenticated && !isAuthPage" :key="forceRefresh">
      <div class="app-layout">
        <div class="app-header">
          <div class="logo">
            <h1>评教系统</h1>
          </div>
          <div class="user-info">
            <span>欢迎, {{ username }}</span>
            <Button icon="pi pi-sign-out" label="退出" text @click="logout" />
          </div>
        </div>
        
        <div class="app-main">    
          <div class="app-sidebar">
            <!-- 侧边导航 -->
          </div>
          
          <div class="app-content">
            <!-- 内容区域 -->
            <router-view />
          </div>
        </div>
      </div>
    </template>
    <template v-else>
      <router-view />
    </template>
</template>

<style lang="scss">
#app {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}

.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  padding: 0 20px;
  background-color: var(--primary-color);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  .logo h1 {
    margin: 0;
    font-size: 1.5rem;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 15px;
  }
}

.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.app-sidebar {
  width: 240px;
  background-color: #f8f9fa;
  border-right: 1px solid #e9ecef;
  padding: 20px 0;
  overflow-y: auto;

  .menu-title {
    padding: 0 20px;
    margin-bottom: 10px;
    color: #6c757d;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
  }

  .menu-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 20px;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
      background-color: #e9ecef;
    }

    &.active {
      background-color: #e3f2fd;
      color: var(--primary-color);
      font-weight: 500;
    }

    i {
      font-size: 1.2rem;
    }
  }
}

.app-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>
