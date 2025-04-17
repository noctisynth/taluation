<template>
  <div class="layout">
    <aside class="sidebar" v-if="type === 'student'">
      <div class="sidebar-header">
        <h3>学生系统</h3>
      </div>
      <div class="sidebar-menu">
        <div class="menu-group">
          <div class="menu-title">课程管理</div>
          <router-link to="/courses" class="menu-item">
            <i class="pi pi-list"></i>
            <span>课程列表</span>
          </router-link>
          <router-link to="/my-evaluations" class="menu-item">
            <i class="pi pi-comment"></i>
            <span>我的评价</span>
          </router-link>
        </div>
        <div class="menu-group">
          <div class="menu-title">个人中心</div>
          <router-link to="/profile" class="menu-item">
            <i class="pi pi-user"></i>
            <span>个人信息</span>
          </router-link>
          <router-link to="/change-password" class="menu-item">
            <i class="pi pi-lock"></i>
            <span>修改密码</span>
          </router-link>
        </div>
      </div>
    </aside>
    <aside class="sidebar" v-if="type === 'teacher'">
      <div class="sidebar-header">
        <h3>教师系统</h3>
      </div>
      <div class="sidebar-menu">
        <div class="menu-group">
          <div class="menu-title">课程管理</div>
          <router-link to="/courses" class="menu-item">
            <i class="pi pi-list"></i>
            <span>课程列表</span>
          </router-link>
          <router-link to="/my-courses" class="menu-item">
            <i class="pi pi-book"></i>
            <span>我的课程</span>
          </router-link>
        </div>
        <div class="menu-group">
          <div class="menu-title">个人中心</div>
          <router-link to="/profile" class="menu-item">
            <i class="pi pi-user"></i>
            <span>个人信息</span>
          </router-link>
          <router-link to="/change-password" class="menu-item">
            <i class="pi pi-lock"></i>
            <span>修改密码</span>
          </router-link>
        </div>
      </div>
    </aside>
    <aside class="sidebar" v-if="type === 'admin'">
      <div class="sidebar-header">
        <h3>管理员系统</h3>
      </div>
      <div class="sidebar-menu">
        <div class="menu-group">
          <div class="menu-title">用户管理</div>
          <router-link to="/user-management" class="menu-item">
            <i class="pi pi-users"></i>
            <span>用户列表</span>
          </router-link>
        </div>
        <div class="menu-group">
          <div class="menu-title">评价管理</div>
          <router-link to="/evaluation-management" class="menu-item">
            <i class="pi pi-comment"></i>
            <span>评价管理</span>
          </router-link>
        </div>
        <div class="menu-group">
          <div class="menu-title">课程管理</div>
          <router-link to="/courses" class="menu-item">
            <i class="pi pi-list"></i>
            <span>课程列表</span>
          </router-link>
          <router-link to="/course-management" class="menu-item">
            <i class="pi pi-cog"></i>
            <span>课程管理</span>
          </router-link>
        </div>
        <div class="menu-group">
          <div class="menu-title">个人中心</div>
          <router-link to="/profile" class="menu-item">
            <i class="pi pi-user"></i>
            <span>个人信息</span>
          </router-link>
          <router-link to="/change-password" class="menu-item">
            <i class="pi pi-lock"></i>
            <span>修改密码</span>
          </router-link>
        </div>
      </div>
    </aside>
    <div class="main-content">
      <nav class="nav-bar">
        <div>
        </div>
        <button @click="handleLogout" class="logout-button" title="退出登录">
            <i class="pi pi-sign-out"></i>
        </button>
      </nav>
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import request from '@/utils/request';
import { logout } from '@/utils/api';

const type = ref('student');
const name = localStorage.getItem('username');

const handleLogout = () => logout();

onMounted(() => {
  const userType = localStorage.getItem('user_type');
  if (userType) {
    type.value = userType;
  } else {
    request.get('/account', {
      params: {
        name
      }
    }).then(res => {
      if (res.data.success) {
        type.value = res.data.data.type;
        localStorage.setItem('user_type', type.value);
      } else {
        logout();
        type.value = 'none';
      }
    }).catch(_ => {
      logout();
      type.value = 'none';
    });
  }
});
</script>

<style scoped lang="scss">
.layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 240px;
  background-color: #f8f9fa;
  border-right: 1px solid #e9ecef;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  
  h3 {
    margin: 0;
    color: #0d4880;
  }
}

.sidebar-menu {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.menu-group {
  margin-bottom: 20px;
}

.menu-title {
  padding: 0 20px;
  margin-bottom: 10px;
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 600;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  color: #212529;
  text-decoration: none;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: #e9ecef;
  }
  
  &.router-link-active {
    background-color: #e3f2fd;
    color: #0d4880;
    font-weight: 500;
  }
  
  i {
    font-size: 1.1rem;
  }
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  padding: 10px 20px;
  background-color: #fff;
  border-bottom: 1px solid #e9ecef;
  
  div {
    display: flex;
    gap: 20px;
  }

  a {
    color: #0d4880;
    text-decoration: none;
    padding: 5px 0;
    
    &.router-link-active {
      font-weight: bold;
      border-bottom: 2px solid #0d4880;
    }
  }

  .logout-button {
    background: none;
    border: none;
    cursor: pointer;
    color: #dc3545;
    padding: 8px 12px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: background-color 0.2s, color 0.2s;

    &:hover {
      background-color: #f8d7da;
      color: #721c24;
    }
  }
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
