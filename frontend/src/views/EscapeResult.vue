<template>
  <div class="escape-result-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <a-button class="back-button" size="large" @click="goBack">
        ← 返回首页
      </a-button>
      <h1 class="header-title">🎬 下班逃离计划</h1>
    </div>

    <div v-if="escapePlan" class="content-wrapper">
      <!-- 概览卡片 -->
      <div class="overview-section">
        <a-row :gutter="24">
          <a-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">🏢</div>
              <div class="stat-label">起点</div>
              <div class="stat-value">{{ escapePlan.origin }}</div>
            </div>
          </a-col>
          <a-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">🏠</div>
              <div class="stat-label">终点</div>
              <div class="stat-value">{{ escapePlan.destination }}</div>
            </div>
          </a-col>
          <a-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">⏱️</div>
              <div class="stat-label">总路程耗时</div>
              <div class="stat-value">{{ escapePlan.total_duration }}分钟</div>
            </div>
          </a-col>
          <a-col :span="6">
            <div class="stat-card">
              <div class="stat-icon">📍</div>
              <div class="stat-label">总距离</div>
              <div class="stat-value">{{ (escapePlan.total_distance / 1000).toFixed(1) }}公里</div>
            </div>
          </a-col>
        </a-row>
      </div>

      <a-row :gutter="24">
        <!-- 左侧: 时间线和详情 -->
        <a-col :span="16">
          <!-- 时间线 -->
          <a-card title="📅 逃离时间线" :bordered="false" class="timeline-card">
            <a-timeline mode="left">
              <a-timeline-item
                v-for="(event, index) in escapePlan.timeline"
                :key="index"
                :color="getEventColor(event.event)"
              >
                <template #label>
                  <span class="timeline-time">{{ event.time }}</span>
                </template>
                <div class="timeline-content">
                  <div class="timeline-event">{{ event.event }}</div>
                  <div class="timeline-location">📍 {{ event.location }}</div>
                  <div class="timeline-desc">{{ event.description }}</div>
                </div>
              </a-timeline-item>
            </a-timeline>
          </a-card>

          <!-- 电影信息 -->
          <a-card v-if="escapePlan.cinema" title="🎬 电影安排" :bordered="false" class="movie-card">
            <div class="movie-info">
              <div class="movie-header">
                <h3>{{ escapePlan.cinema.name }}</h3>
                <a-tag color="red">距离{{ escapePlan.cinema.distance }}米</a-tag>
              </div>
              <p class="cinema-address">📍 {{ escapePlan.cinema.address }}</p>

              <a-divider>可选场次</a-divider>

              <div class="showtimes">
                <a-radio-group
                  v-model:value="selectedShowtime"
                  size="large"
                  class="showtime-group"
                >
                  <a-radio-button
                    v-for="showtime in escapePlan.cinema.showtimes"
                    :key="showtime.time"
                    :value="showtime.time"
                    class="showtime-btn"
                  >
                    <div class="showtime-content">
                      <div class="showtime-time">{{ showtime.time }}</div>
                      <div class="showtime-movie">{{ showtime.movie_name }}</div>
                      <div class="showtime-detail">{{ showtime.hall }} | 余座{{ showtime.available_seats }}</div>
                    </div>
                  </a-radio-button>
                </a-radio-group>
              </div>
            </div>
          </a-card>

          <!-- 餐厅信息 -->
          <a-card v-if="escapePlan.restaurant" title="🍽️ 晚餐安排" :bordered="false" class="restaurant-card">
            <div class="restaurant-info">
              <div class="restaurant-header">
                <h3>{{ escapePlan.restaurant.name }}</h3>
                <a-space>
                  <a-tag v-if="escapePlan.restaurant.cuisine">{{ escapePlan.restaurant.cuisine }}</a-tag>
                  <a-tag v-if="escapePlan.restaurant.price_range" color="green">{{ escapePlan.restaurant.price_range }}</a-tag>
                </a-space>
              </div>
              <a-descriptions :column="2" size="small">
                <a-descriptions-item label="地址">{{ escapePlan.restaurant.address }}</a-descriptions-item>
                <a-descriptions-item label="距离">{{ escapePlan.restaurant.distance }}米</a-descriptions-item>
                <a-descriptions-item label="评分" v-if="escapePlan.restaurant.rating">
                  ⭐ {{ escapePlan.restaurant.rating }}
                </a-descriptions-item>
                <a-descriptions-item label="预估消费">
                  ¥{{ escapePlan.restaurant.estimated_cost }}
                </a-descriptions-item>
              </a-descriptions>
            </div>
          </a-card>
        </a-col>

        <!-- 右侧: 路线和地图 -->
        <a-col :span="8">
          <!-- 路线概览 -->
          <a-card title="🛣️ 路线概览" :bordered="false" class="route-card">
            <div class="route-summary">
              <div class="route-item">
                <div class="route-marker start">起</div>
                <div class="route-info">
                  <div class="route-name">{{ escapePlan.origin }}</div>
                  <div class="route-time">下班 {{ escapePlan.off_work_time }}</div>
                </div>
              </div>

              <div class="route-line"></div>

              <div class="route-item" v-if="escapePlan.cinema">
                <div class="route-marker cinema">影</div>
                <div class="route-info">
                  <div class="route-name">{{ escapePlan.cinema.name }}</div>
                  <div class="route-time">观影</div>
                </div>
              </div>

              <div class="route-line"></div>

              <div class="route-item" v-if="escapePlan.restaurant">
                <div class="route-marker restaurant">餐</div>
                <div class="route-info">
                  <div class="route-name">{{ escapePlan.restaurant.name }}</div>
                  <div class="route-time">晚餐</div>
                </div>
              </div>

              <div class="route-line"></div>

              <div class="route-item">
                <div class="route-marker end">终</div>
                <div class="route-info">
                  <div class="route-name">{{ escapePlan.destination }}</div>
                  <div class="route-time">回家</div>
                </div>
              </div>
            </div>
          </a-card>

          <!-- 公共交通信息 -->
          <a-card v-if="escapePlan.transit_to_cinema || escapePlan.transit_from_cinema" title="🚌 公交导航" :bordered="false" class="transit-card">
            <!-- 去电影院公交 -->
            <div v-if="escapePlan.transit_to_cinema" class="transit-section">
              <div class="transit-section-title">去电影院</div>
              <a-descriptions :column="3" size="small">
                <a-descriptions-item label="总耗时">{{ escapePlan.transit_to_cinema.total_duration }}分钟</a-descriptions-item>
                <a-descriptions-item label="总距离">{{ (escapePlan.transit_to_cinema.total_distance / 1000).toFixed(1) }}公里</a-descriptions-item>
                <a-descriptions-item label="费用">¥{{ escapePlan.transit_to_cinema.total_cost }}</a-descriptions-item>
              </a-descriptions>

              <div class="transit-segments">
                <div
                  v-for="(seg, index) in escapePlan.transit_to_cinema.segments"
                  :key="'to-' + index"
                  class="transit-segment"
                  :class="'segment-' + seg.type"
                >
                  <div class="segment-icon">
                    <span v-if="seg.type === 'walking'">🚶</span>
                    <span v-else-if="seg.type === 'bus'">🚌</span>
                    <span v-else-if="seg.type === 'subway'">🚇</span>
                  </div>
                  <div class="segment-content">
                    <div class="segment-name">{{ seg.name }}</div>
                    <div class="segment-detail" v-if="seg.type !== 'walking'">
                      {{ seg.start_stop }} → {{ seg.end_stop }}
                      <span v-if="seg.stops > 0">，{{ seg.stops }}站</span>
                    </div>
                    <div class="segment-duration" v-if="seg.type !== 'walking'">
                      约{{ seg.duration }}分钟
                    </div>
                    <div class="segment-desc">{{ seg.description }}</div>
                  </div>
                </div>
              </div>
            </div>

            <a-divider v-if="escapePlan.transit_to_cinema && escapePlan.transit_from_cinema"/>

            <!-- 电影院回家公交 -->
            <div v-if="escapePlan.transit_from_cinema" class="transit-section">
              <div class="transit-section-title">电影院 → 家</div>
              <a-descriptions :column="3" size="small">
                <a-descriptions-item label="总耗时">{{ escapePlan.transit_from_cinema.total_duration }}分钟</a-descriptions-item>
                <a-descriptions-item label="总距离">{{ (escapePlan.transit_from_cinema.total_distance / 1000).toFixed(1) }}公里</a-descriptions-item>
                <a-descriptions-item label="费用">¥{{ escapePlan.transit_from_cinema.total_cost }}</a-descriptions-item>
              </a-descriptions>

              <div class="transit-segments">
                <div
                  v-for="(seg, index) in escapePlan.transit_from_cinema.segments"
                  :key="'from-' + index"
                  class="transit-segment"
                  :class="'segment-' + seg.type"
                >
                  <div class="segment-icon">
                    <span v-if="seg.type === 'walking'">🚶</span>
                    <span v-else-if="seg.type === 'bus'">🚌</span>
                    <span v-else-if="seg.type === 'subway'">🚇</span>
                  </div>
                  <div class="segment-content">
                    <div class="segment-name">{{ seg.name }}</div>
                    <div class="segment-detail" v-if="seg.type !== 'walking'">
                      {{ seg.start_stop }} → {{ seg.end_stop }}
                      <span v-if="seg.stops > 0">，{{ seg.stops }}站</span>
                    </div>
                    <div class="segment-duration" v-if="seg.type !== 'walking'">
                      约{{ seg.duration }}分钟
                    </div>
                    <div class="segment-desc">{{ seg.description }}</div>
                  </div>
                </div>
              </div>
            </div>
          </a-card>

          <!-- 地图 -->
          <a-card title="📍 地图" :bordered="false" class="map-card">
            <div id="escape-amap-container" style="width: 100%; height: 300px"></div>
          </a-card>

          <!-- 建议 -->
          <a-card title="💡 逃离建议" :bordered="false" class="suggestions-card">
            <p>{{ escapePlan.overall_suggestions }}</p>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <a-empty v-else description="没有找到逃离计划数据">
      <template #image>
        <div style="font-size: 80px;">🎬</div>
      </template>
      <template #description>
        <span style="color: #999;">暂无逃离计划数据，请先创建计划</span>
      </template>
      <a-button type="primary" @click="goBack">返回首页创建计划</a-button>
    </a-empty>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import AMapLoader from '@amap/amap-jsapi-loader'
import type { EscapePlan } from '@/types'

const router = useRouter()
const escapePlan = ref<EscapePlan | null>(null)
const selectedShowtime = ref('19:30')
let map: any = null

onMounted(async () => {
  const data = sessionStorage.getItem('escapePlan')
  if (data) {
    escapePlan.value = JSON.parse(data)

    if (escapePlan.value?.cinema?.showtimes) {
      const defaultShowtime = escapePlan.value.cinema.showtimes.find(
        (s: any) => s.time === '19:30'
      ) || escapePlan.value.cinema.showtimes[0]
      selectedShowtime.value = defaultShowtime.time
    }

    await nextTick()
    initMap()
  }
})

const goBack = () => {
  router.push('/escape')
}

const getEventColor = (event: string) => {
  if (event.includes('下班')) return 'green'
  if (event.includes('晚餐')) return 'orange'
  if (event.includes('电影') || event.includes('观影')) return 'red'
  if (event.includes('到家')) return 'blue'
  return 'gray'
}

const initMap = async () => {
  try {
    if (!escapePlan.value) return

    const AMap = await AMapLoader.load({
      key: import.meta.env.VITE_AMAP_WEB_JS_KEY,
      version: '2.0',
      plugins: ['AMap.Marker', 'AMap.Polyline', 'AMap.InfoWindow']
    })

    // 计算地图中心点 - 基于所有位置
    let centerLng = 121.4737  // 默认上海
    let centerLat = 31.2304

    const validLocations: [number, number][] = []

    // 收集所有有效坐标
    if (escapePlan.value.origin_location) {
      validLocations.push([escapePlan.value.origin_location.longitude, escapePlan.value.origin_location.latitude])
    }
    if (escapePlan.value.restaurant?.location) {
      validLocations.push([escapePlan.value.restaurant.location.longitude, escapePlan.value.restaurant.location.latitude])
    }
    if (escapePlan.value.cinema?.location) {
      validLocations.push([escapePlan.value.cinema.location.longitude, escapePlan.value.cinema.location.latitude])
    }
    if (escapePlan.value.destination_location) {
      validLocations.push([escapePlan.value.destination_location.longitude, escapePlan.value.destination_location.latitude])
    }

    // 如果有有效位置，计算中心点
    if (validLocations.length > 0) {
      const sumLng = validLocations.reduce((sum, loc) => sum + loc[0], 0)
      const sumLat = validLocations.reduce((sum, loc) => sum + loc[1], 0)
      centerLng = sumLng / validLocations.length
      centerLat = sumLat / validLocations.length
    }

    map = new AMap.Map('escape-amap-container', {
      zoom: 13,
      center: [centerLng, centerLat]
    })

    // 添加标记
    const markers: any[] = []
    const polylines: any[] = []

    // 起点标记
    if (escapePlan.value.origin_location) {
      const startMarker = new AMap.Marker({
        position: [escapePlan.value.origin_location.longitude, escapePlan.value.origin_location.latitude],
        title: '起点',
        label: {
          content: '<div style="background: #52c41a; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">🏢 起点</div>',
          offset: new AMap.Pixel(0, -30)
        }
      })
      markers.push(startMarker)
    }

    // 餐厅标记
    if (escapePlan.value.restaurant?.location) {
      const restaurantMarker = new AMap.Marker({
        position: [escapePlan.value.restaurant.location.longitude, escapePlan.value.restaurant.location.latitude],
        title: escapePlan.value.restaurant.name,
        label: {
          content: '<div style="background: #fa8c16; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">🍽️ 餐厅</div>',
          offset: new AMap.Pixel(0, -30)
        }
      })
      markers.push(restaurantMarker)
    }

    // 电影院标记
    if (escapePlan.value.cinema?.location) {
      const cinemaMarker = new AMap.Marker({
        position: [escapePlan.value.cinema.location.longitude, escapePlan.value.cinema.location.latitude],
        title: escapePlan.value.cinema.name,
        label: {
          content: '<div style="background: #ff4d4f; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">🎬 电影院</div>',
          offset: new AMap.Pixel(0, -30)
        }
      })
      markers.push(cinemaMarker)
    }

    // 终点标记
    if (escapePlan.value.destination_location) {
      const endMarker = new AMap.Marker({
        position: [escapePlan.value.destination_location.longitude, escapePlan.value.destination_location.latitude],
        title: '终点',
        label: {
          content: '<div style="background: #1890ff; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">🏠 终点</div>',
          offset: new AMap.Pixel(0, -30)
        }
      })
      markers.push(endMarker)
    }

    // 绘制路线连线
    const lineColor = ['#52c41a', '#fa8c16', '#ff4d4f', '#1890ff'] // 绿、橙、红、蓝

    // 构建路线点顺序
    const routePoints: [number, number][] = []
    if (escapePlan.value.origin_location) {
      routePoints.push([escapePlan.value.origin_location.longitude, escapePlan.value.origin_location.latitude])
    }
    if (escapePlan.value.restaurant?.location) {
      routePoints.push([escapePlan.value.restaurant.location.longitude, escapePlan.value.restaurant.location.latitude])
    }
    if (escapePlan.value.cinema?.location) {
      routePoints.push([escapePlan.value.cinema.location.longitude, escapePlan.value.cinema.location.latitude])
    }
    if (escapePlan.value.destination_location) {
      routePoints.push([escapePlan.value.destination_location.longitude, escapePlan.value.destination_location.latitude])
    }

    // 绘制完整路线
    if (routePoints.length >= 2) {
      const routeLine = new AMap.Polyline({
        path: routePoints,
        strokeColor: '#667eea',
        strokeWeight: 4,
        strokeOpacity: 0.8,
        strokeStyle: 'solid',
        showDir: true
      })
      polylines.push(routeLine)
    }

    // 添加标记和线到地图
    if (markers.length > 0) {
      map.add(markers)
    }
    if (polylines.length > 0) {
      map.add(polylines)
    }
    if (validLocations.length > 0) {
      map.setFitView(markers.concat(polylines))
    }

    message.success('地图加载成功')
  } catch (error) {
    console.error('地图加载失败:', error)
  }
}
</script>

<style scoped>
.escape-result-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
  padding: 40px 20px;
}

.page-header {
  max-width: 1200px;
  margin: 0 auto 30px;
  display: flex;
  align-items: center;
  gap: 20px;
  animation: fadeInDown 0.6s ease-out;
}

.back-button {
  border-radius: 8px;
  font-weight: 500;
}

.header-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #333;
}

/* 内容布局 */
.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* 概览卡片 */
.overview-section {
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(255, 77, 79, 0.15);
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 时间线卡片 */
.timeline-card {
  margin-bottom: 24px;
}

.timeline-time {
  font-size: 14px;
  font-weight: 600;
  color: #ff4d4f;
}

.timeline-content {
  background: #fff5f5;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 8px;
}

.timeline-event {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.timeline-location {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.timeline-desc {
  font-size: 13px;
  color: #999;
}

/* 电影卡片 */
.movie-card {
  margin-bottom: 24px;
}

.movie-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.movie-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.cinema-address {
  color: #666;
  margin: 8px 0;
}

.showtimes {
  margin-top: 16px;
}

.showtime-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.showtime-btn {
  width: 100%;
  height: auto !important;
  padding: 12px !important;
  text-align: left;
}

.showtime-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.showtime-time {
  font-size: 20px;
  font-weight: 700;
  color: #ff4d4f;
  min-width: 60px;
}

.showtime-movie {
  font-size: 16px;
  font-weight: 600;
  flex: 1;
}

.showtime-detail {
  font-size: 12px;
  color: #999;
}

/* 餐厅卡片 */
.restaurant-card {
  margin-bottom: 24px;
}

.restaurant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.restaurant-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

/* 路线卡片 */
.route-card {
  margin-bottom: 24px;
}

.route-summary {
  padding: 16px;
  background: #fafafa;
  border-radius: 12px;
}

.route-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.route-marker {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: white;
}

.route-marker.start {
  background: linear-gradient(135deg, #52c41a, #73d13d);
}

.route-marker.cinema {
  background: linear-gradient(135deg, #ff4d4f, #ff7875);
}

.route-marker.restaurant {
  background: linear-gradient(135deg, #fa8c16, #ffc53d);
}

.route-marker.end {
  background: linear-gradient(135deg, #1890ff, #69c0ff);
}

.route-info {
  flex: 1;
}

.route-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.route-time {
  font-size: 12px;
  color: #999;
}

.route-line {
  width: 2px;
  height: 30px;
  background: #e8e8e8;
  margin-left: 17px;
  margin-top: 8px;
  margin-bottom: 8px;
}

/* 地图卡片 */
.map-card {
  margin-bottom: 24px;
}

.map-card :deep(.ant-card-body) {
  padding: 0;
}

/* 建议卡片 */
.suggestions-card {
  background: linear-gradient(135deg, #fff5f5, #fff0f0);
}

.suggestions-card p {
  margin: 0;
  color: #666;
  line-height: 1.8;
}

/* 公交导航卡片 */
.transit-card {
  margin-bottom: 24px;
}

.transit-segments {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.transit-section {
  margin-bottom: 16px;
}

.transit-section-title {
  font-weight: 600;
  font-size: 16px;
  color: #333;
  margin-bottom: 12px;
}

.transit-segment {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.transit-segment.segment-walking {
  border-left-color: #999;
  background: #f5f5f5;
}

.transit-segment.segment-bus {
  border-left-color: #52c41a;
}

.transit-segment.segment-subway {
  border-left-color: #1890ff;
}

.segment-icon {
  font-size: 24px;
  width: 36px;
  text-align: center;
}

.segment-content {
  flex: 1;
}

.segment-name {
  font-weight: 600;
  font-size: 16px;
  color: #333;
}

.segment-detail {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.segment-duration {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}

.segment-desc {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

/* 卡片通用样式 */
:deep(.ant-card) {
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

:deep(.ant-card:hover) {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

:deep(.ant-card-head) {
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
  color: white !important;
  border-radius: 16px 16px 0 0;
}

:deep(.ant-card-head-title) {
  color: white !important;
  font-size: 16px;
  font-weight: 600;
}

:deep(.ant-card-head) {
  border-radius: 16px 16px 0 0;
}

/* 动画 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
