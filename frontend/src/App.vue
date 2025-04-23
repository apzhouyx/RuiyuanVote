<template>
  <el-container class="app-container">
    <el-header>
      <h1>瑞园二期投票统计系统</h1>
    </el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ElContainer, ElHeader, ElMain } from 'element-plus'
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.el-header {
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}
</style> 