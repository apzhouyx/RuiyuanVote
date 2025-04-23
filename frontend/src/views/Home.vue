<template>
  <div class="home-container">
    <el-row :gutter="20">
      <!-- 左侧楼栋列表 -->
      <el-col :span="16">
        <el-card class="buildings-card">
          <template #header>
            <div class="card-header">
              <span>楼栋投票进度</span>
            </div>
          </template>
          <el-row :gutter="10">
            <el-col :span="4" v-for="building in sortedBuildings" :key="building.id">
              <el-card class="building-item" @click="showBuildingDetail(building)" :body-style="{ padding: '5px' }">
                <h3>{{ building.building_number }}栋</h3>
                <el-progress 
                  type="circle" 
                  :percentage="calculateBuildingProgress(building)"
                  :color="getProgressColor"
                  :width="50"
                  :stroke-width="8"
                />
                <div class="building-info">
                  <span>{{ getVotedCount(building) }}/{{ building.total_units }}</span>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <!-- 右侧统计信息 -->
      <el-col :span="8">
        <el-card class="statistics-card" style="position: sticky; top: 20px;">
          <template #header>
            <div class="card-header">
              <span>投票统计</span>
            </div>
          </template>
          <div class="statistics-content">
            <div ref="pieChartRef" class="pie-chart"></div>
            <div class="statistics-info">
              <el-descriptions direction="vertical" :column="1" border>
                <el-descriptions-item label="总户数">{{ statistics.total }}</el-descriptions-item>
                <el-descriptions-item label="已投票">{{ statistics.voted }}</el-descriptions-item>
                <el-descriptions-item label="完成率">{{ statistics.percentage }}%</el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import axios from 'axios'

const router = useRouter()
const pieChartRef = ref<HTMLElement>()
let pieChart: echarts.ECharts | null = null

const statistics = ref({
  total: 0,
  voted: 0,
  percentage: 0
})

const buildings = ref([])

// 排序后的楼栋列表
const sortedBuildings = computed(() => {
  return [...buildings.value].sort((a: any, b: any) => {
    return parseInt(a.building_number) - parseInt(b.building_number)
  })
})

// WebSocket连接
const ws = new WebSocket('ws://localhost:8000/ws')

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  // 更新数据
  fetchStatistics()
  fetchBuildings()
}

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const response = await axios.get('/api/votes/statistics')
    statistics.value = response.data
    updatePieChart()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取楼栋数据
const fetchBuildings = async () => {
  try {
    const response = await axios.get('/api/buildings')
    buildings.value = response.data
  } catch (error) {
    console.error('获取楼栋数据失败:', error)
  }
}

// 初始化饼图
const initPieChart = () => {
  if (pieChartRef.value) {
    pieChart = echarts.init(pieChartRef.value)
    updatePieChart()
  }
}

// 更新饼图数据
const updatePieChart = () => {
  if (!pieChart) return

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: 0
    },
    series: [
      {
        name: '投票统计',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: true,
          position: 'inside',
          formatter: '{d}%',
          fontSize: 14,
          color: '#fff'
        },
        data: [
          { 
            value: statistics.value.voted, 
            name: '已投票',
            itemStyle: { color: '#67C23A' }
          },
          { 
            value: statistics.value.total - statistics.value.voted, 
            name: '未投票',
            itemStyle: { color: '#909399' }
          }
        ]
      }
    ]
  }

  pieChart.setOption(option)
}

// 计算楼栋投票进度
const calculateBuildingProgress = (building: any) => {
  const votedCount = getVotedCount(building)
  return Math.round((votedCount / building.total_units) * 100)
}

// 获取已投票数量
const getVotedCount = (building: any) => {
  return building.units.filter((unit: any) => unit.has_voted).length
}

// 进度条颜色
const getProgressColor = (percentage: number) => {
  if (percentage < 30) return '#F56C6C'
  if (percentage < 70) return '#E6A23C'
  return '#67C23A'
}

// 显示楼栋详情
const showBuildingDetail = (building: any) => {
  router.push(`/building/${building.id}`)
}

onMounted(() => {
  fetchStatistics()
  fetchBuildings()
  initPieChart()
  window.addEventListener('resize', () => pieChart?.resize())
})

onUnmounted(() => {
  pieChart?.dispose()
  ws.close()
})
</script>

<style scoped>
.home-container {
  max-width: 1400px;
  margin: 20px auto;
  padding: 0 20px;
}

.statistics-card {
  margin-bottom: 20px;
  height: calc(100vh - 40px);
  overflow-y: auto;
}

.statistics-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.pie-chart {
  width: 100%;
  height: 300px;
}

.statistics-info {
  width: 100%;
}

.buildings-card {
  margin-bottom: 20px;
  min-height: calc(100vh - 40px);
}

.building-item {
  text-align: center;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.building-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.1);
}

.building-info {
  margin-top: 5px;
  font-size: 12px;
  color: #606266;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

h3 {
  margin: 0 0 5px 0;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:deep(.el-descriptions__label) {
  font-weight: bold;
  width: 80px;
}

:deep(.el-descriptions__content) {
  font-size: 16px;
}

:deep(.el-progress__text) {
  font-size: 12px !important;
}
</style> 