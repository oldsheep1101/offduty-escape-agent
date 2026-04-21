<template>
  <div class="escape-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <!-- 页面标题 -->
    <div class="page-header">
      <div class="icon-wrapper">
        <span class="icon">🎬</span>
      </div>
      <h1 class="page-title">下班逃离助手</h1>
      <p class="page-subtitle">告别加班，来一场说走就走的电影+美食之旅</p>
    </div>

    <a-card class="form-card" :bordered="false">
      <a-form
        :model="formData"
        layout="vertical"
        @finish="handleSubmit"
      >
        <!-- 基本信息 -->
        <div class="form-section">
          <div class="section-header">
            <span class="section-icon">📍</span>
            <span class="section-title">出发与目的地</span>
          </div>

          <a-row :gutter="24">
            <a-col :span="12">
              <a-form-item
                name="origin"
                :rules="[{ required: true, message: '请输入公司/起点地址' }]"
              >
                <template #label>
                  <span class="form-label">公司/起点</span>
                </template>
                <a-input
                  v-model:value="formData.origin"
                  placeholder="例如: 北京市朝阳区望京SOHO"
                  size="large"
                  class="custom-input"
                >
                  <template #prefix>
                    <span style="color: #1890ff;">🏢</span>
                  </template>
                </a-input>
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                name="destination"
                :rules="[{ required: true, message: '请输入回家方向/终点地址' }]"
              >
                <template #label>
                  <span class="form-label">回家方向/终点</span>
                </template>
                <a-input
                  v-model:value="formData.destination"
                  placeholder="例如: 北京市海淀区五道口"
                  size="large"
                  class="custom-input"
                >
                  <template #prefix>
                    <span style="color: #52c41a;">🏠</span>
                  </template>
                </a-input>
              </a-form-item>
            </a-col>
          </a-row>
        </div>

        <!-- 时间与城市 -->
        <div class="form-section">
          <div class="section-header">
            <span class="section-icon">⏰</span>
            <span class="section-title">时间与地点</span>
          </div>

          <a-row :gutter="24">
            <a-col :span="8">
              <a-form-item
                name="off_work_time"
                :rules="[{ required: true, message: '请选择下班时间' }]"
              >
                <template #label>
                  <span class="form-label">下班时间</span>
                </template>
                <a-time-picker
                  v-model:value="formData.off_work_time"
                  format="HH:mm"
                  :minute-step="30"
                  placeholder="选择下班时间"
                  size="large"
                  class="custom-input"
                  suffix-icon="🕐"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                name="city"
                :rules="[{ required: true, message: '请输入城市' }]"
              >
                <template #label>
                  <span class="form-label">城市</span>
                </template>
                <a-input
                  v-model:value="formData.city"
                  placeholder="例如: 北京"
                  size="large"
                  class="custom-input"
                >
                  <template #prefix>
                    <span style="color: #722ed1;">🌆</span>
                  </template>
                </a-input>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item name="movie_preference">
                <template #label>
                  <span class="form-label">电影偏好(可选)</span>
                </template>
                <a-select v-model:value="formData.movie_preference" size="large" class="custom-select" placeholder="选择电影类型">
                  <a-select-option value="">不限</a-select-option>
                  <a-select-option value="动作片">🎬 动作片</a-select-option>
                  <a-select-option value="喜剧片">😂 喜剧片</a-select-option>
                  <a-select-option value="爱情片">💕 爱情片</a-select-option>
                  <a-select-option value="科幻片">🚀 科幻片</a-select-option>
                  <a-select-option value="动画片">🎨 动画片</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item name="cuisine">
                <template #label>
                  <span class="form-label">餐厅菜系(可选)</span>
                </template>
                <a-select v-model:value="formData.cuisine" size="large" class="custom-select" placeholder="选择菜系">
                  <a-select-option value="">不限</a-select-option>
                  <a-select-option value="川菜">🌶️ 川菜</a-select-option>
                  <a-select-option value="湘菜">🔥 湘菜</a-select-option>
                  <a-select-option value="粤菜">🍽️ 粤菜</a-select-option>
                  <a-select-option value="火锅">🍲 火锅</a-select-option>
                  <a-select-option value="烧烤">🍖 烧烤</a-select-option>
                  <a-select-option value="日本料理">🍣 日本料理</a-select-option>
                  <a-select-option value="韩国料理">🥘 韩国料理</a-select-option>
                  <a-select-option value="西餐">🍝 西餐</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="24">
            <a-col :span="8" :offset="8">
              <a-form-item name="budget_per_person">
                <template #label>
                  <span class="form-label">人均预算(元/人)</span>
                </template>
                <a-input-number
                  v-model:value="formData.budget_per_person"
                  :min="20"
                  :max="500"
                  :step="10"
                  placeholder="80"
                  size="large"
                  class="custom-input"
                  style="width: 100%"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item name="transportation">
                <template #label>
                  <span class="form-label">交通方式</span>
                </template>
                <a-select v-model:value="formData.transportation" size="large" class="custom-select" placeholder="选择交通方式">
                  <a-select-option value="driving">🚗 开车</a-select-option>
                  <a-select-option value="transit">🚌 公共交通</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>
        </div>

        <!-- 提交按钮 -->
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            :loading="loading"
            size="large"
            block
            class="submit-button"
          >
            <template v-if="!loading">
              <span class="button-icon">🚀</span>
              <span>开始规划我的逃离路线</span>
            </template>
            <template v-else>
              <span>正在规划中...</span>
            </template>
          </a-button>
        </a-form-item>

        <!-- 加载进度条 -->
        <a-form-item v-if="loading">
          <div class="loading-container">
            <a-progress
              :percent="loadingProgress"
              status="active"
              :stroke-color="{
                '0%': '#ff4d4f',
                '100%': '#ff7875',
              }"
              :stroke-width="10"
            />
            <p class="loading-status">
              {{ loadingStatus }}
            </p>
          </div>
        </a-form-item>
      </a-form>
    </a-card>

    <!-- 功能说明 -->
    <div class="features-section">
      <a-row :gutter="24">
        <a-col :span="8">
          <div class="feature-card">
            <div class="feature-icon">🎬</div>
            <h3>中间影院</h3>
            <p>在回家路上为你寻找最合适的电影院</p>
          </div>
        </a-col>
        <a-col :span="8">
          <div class="feature-card">
            <div class="feature-icon">🍽️</div>
            <h3>美食相伴</h3>
            <p>搜索影院附近的优质餐厅</p>
          </div>
        </a-col>
        <a-col :span="8">
          <div class="feature-card">
            <div class="feature-icon">⏱️</div>
            <h3>时间优化</h3>
            <p>智能规划时间，不耽误观影</p>
          </div>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { generateEscapePlan } from '@/services/api'
import type { EscapeFormData } from '@/types'
import type { Dayjs } from 'dayjs'

const router = useRouter()
const loading = ref(false)
const loadingProgress = ref(0)
const loadingStatus = ref('')

const formData = reactive<EscapeFormData & { off_work_time: Dayjs | null }>({
  origin: '',
  destination: '',
  off_work_time: null,
  city: '',
  movie_preference: '',
  cuisine: '',
  budget_per_person: 80,
  transportation: 'driving'
})

const handleSubmit = async () => {
  if (!formData.off_work_time) {
    message.error('请选择下班时间')
    return
  }

  loading.value = true
  loadingProgress.value = 0
  loadingStatus.value = '正在初始化...'

  // 模拟进度更新
  const progressInterval = setInterval(() => {
    if (loadingProgress.value < 90) {
      loadingProgress.value += 10

      if (loadingProgress.value <= 30) {
        loadingStatus.value = '🎬 正在搜索电影院...'
      } else if (loadingProgress.value <= 50) {
        loadingStatus.value = '🛣️ 正在规划路线...'
      } else if (loadingProgress.value <= 70) {
        loadingStatus.value = '🍽️ 正在搜索餐厅...'
      } else {
        loadingStatus.value = '📋 正在生成逃离计划...'
      }
    }
  }, 500)

  try {
    const requestData: EscapeFormData = {
      origin: formData.origin,
      destination: formData.destination,
      off_work_time: formData.off_work_time.format('HH:mm'),
      city: formData.city,
      movie_preference: formData.movie_preference,
      cuisine: formData.cuisine,
      budget_per_person: formData.budget_per_person,
      transportation: formData.transportation
    }

    const response = await generateEscapePlan(requestData)

    clearInterval(progressInterval)
    loadingProgress.value = 100
    loadingStatus.value = '✅ 完成!'

    if (response.success && response.data) {
      // 保存到sessionStorage
      sessionStorage.setItem('escapePlan', JSON.stringify(response.data))

      message.success('逃离计划生成成功!')

      // 短暂延迟后跳转
      setTimeout(() => {
        router.push('/escape-result')
      }, 500)
    } else {
      message.error(response.message || '生成失败')
    }
  } catch (error: any) {
    clearInterval(progressInterval)
    message.error(error.message || '生成逃离计划失败，请稍后重试')
  } finally {
    setTimeout(() => {
      loading.value = false
      loadingProgress.value = 0
      loadingStatus.value = ''
    }, 1000)
  }
}
</script>

<style scoped>
.escape-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
  padding: 60px 20px;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 200px;
  height: 200px;
  bottom: 30%;
  left: -50px;
  animation-delay: 5s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  bottom: -50px;
  right: 30%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(180deg);
  }
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 50px;
  animation: fadeInDown 0.8s ease-out;
  position: relative;
  z-index: 1;
}

.icon-wrapper {
  margin-bottom: 20px;
}

.icon {
  font-size: 80px;
  display: inline-block;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.page-title {
  font-size: 56px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 16px;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
  letter-spacing: 2px;
}

.page-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
  font-weight: 300;
}

/* 表单卡片 */
.form-card {
  max-width: 1000px;
  margin: 0 auto;
  border-radius: 24px;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
  animation: fadeInUp 0.8s ease-out;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.98) !important;
}

/* 表单分区 */
.form-section {
  margin-bottom: 32px;
  padding: 24px;
  background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
  border-radius: 16px;
  border: 1px solid #ffedcd;
  transition: all 0.3s ease;
}

.form-section:hover {
  box-shadow: 0 8px 24px rgba(255, 77, 79, 0.15);
  transform: translateY(-2px);
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #ff4d4f;
}

.section-icon {
  font-size: 24px;
  margin-right: 12px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

/* 表单标签 */
.form-label {
  font-size: 15px;
  font-weight: 500;
  color: #555;
}

/* 自定义输入框 */
.custom-input :deep(.ant-input),
.custom-input :deep(.ant-picker) {
  border-radius: 12px;
  border: 2px solid #ffe7e7;
  transition: all 0.3s ease;
}

.custom-input :deep(.ant-input:hover),
.custom-input :deep(.ant-picker:hover) {
  border-color: #ff4d4f;
}

.custom-input :deep(.ant-input:focus),
.custom-input :deep(.ant-picker-focused) {
  border-color: #ff4d4f;
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.1);
}

/* 自定义选择框 */
.custom-select :deep(.ant-select-selector) {
  border-radius: 12px !important;
  border: 2px solid #ffe7e7 !important;
  transition: all 0.3s ease;
}

.custom-select:hover :deep(.ant-select-selector) {
  border-color: #ff4d4f !important;
}

.custom-select :deep(.ant-select-focused .ant-select-selector) {
  border-color: #ff4d4f !important;
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.1) !important;
}

/* 提交按钮 */
.submit-button {
  height: 56px;
  border-radius: 28px;
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
  border: none;
  box-shadow: 0 8px 24px rgba(255, 77, 79, 0.4);
  transition: all 0.3s ease;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(255, 77, 79, 0.5);
}

.submit-button:active {
  transform: translateY(0);
}

.button-icon {
  margin-right: 8px;
  font-size: 20px;
}

/* 加载容器 */
.loading-container {
  text-align: center;
  padding: 24px;
  background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
  border-radius: 16px;
  border: 2px dashed #ff4d4f;
}

.loading-status {
  margin-top: 16px;
  color: #ff4d4f;
  font-size: 18px;
  font-weight: 500;
}

/* 功能说明 */
.features-section {
  max-width: 1000px;
  margin: 40px auto 0;
  position: relative;
  z-index: 1;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(255, 77, 79, 0.2);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.feature-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px;
}

.feature-card p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* 动画 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
