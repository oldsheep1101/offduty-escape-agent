<template>
  <div id="app">
    <a-layout style="min-height: 100vh">
      <a-layout-header style="background: #001529; padding: 0 50px; display: flex; align-items: center; justify-content: space-between;">
        <div style="color: white; font-size: 24px; font-weight: bold">
          🌍 HelloAgents智能助手
        </div>
        <a-menu
          theme="dark"
          mode="horizontal"
          :selected-keys="[currentRoute]"
          style="flex: 1; justify-content: center; border-bottom: none;"
        >
          <a-menu-item key="home" @click="$router.push('/')">
            ✈️ 智能旅行助手
          </a-menu-item>
          <a-menu-item key="escape" @click="$router.push('/escape')">
            🎬 下班逃离助手
          </a-menu-item>
        </a-menu>
      </a-layout-header>
      <a-layout-content style="padding: 24px">
        <router-view />
      </a-layout-content>
      <a-layout-footer style="text-align: center">
        HelloAgents智能助手 ©2025 基于HelloAgents框架
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentRoute = computed(() => {
  if (route.path.includes('escape')) return 'escape'
  return 'home'
})
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif;
}
</style>

