<template>
  <div class="building-detail">
    <el-page-header @back="goBack">
      <template #content>
        <div class="page-header-content">
          <span class="building-title">{{ buildingTitle }}</span>
          <el-tag :type="getProgressType" size="large">
            完成率: {{ completionRate }}%
          </el-tag>
        </div>
      </template>
    </el-page-header>

    <div class="main-content">
      <div class="left-content">
        <el-card class="units-grid">
          <template #header>
            <div class="card-header">
              <div class="legend">
                <div class="legend-item">
                  <div class="legend-color not-voted"></div>
                  <span>未投票</span>
                </div>
                <div class="legend-item">
                  <div class="legend-color selected"></div>
                  <span>已选择</span>
                </div>
                <div class="legend-item">
                  <div class="legend-color voted"></div>
                  <span>已投票</span>
                </div>
              </div>
            </div>
          </template>
          
          <div v-if="searchQuery && searchResults.length > 0" class="search-results">
            <h3>搜索结果</h3>
            <div class="room-grid">
              <div
                v-for="room in searchResults"
                :key="room.id"
                class="room-item"
                :class="{
                  'voted': room.has_voted,
                  'selected': selectedRooms.includes(room.id)
                }"
                @click="toggleRoomSelection(room)"
              >
                {{ room.unit_number }}-{{ room.floor }}-{{ room.room_number }}
              </div>
            </div>
          </div>

          <div v-if="!searchQuery" class="units-container">
            <div 
              v-for="unit in building.unit_count" 
              :key="unit" 
              :class="['unit-section', `unit-${unit}`]"
            >
              <div class="unit-header">
                <h3>{{ unit }}单元</h3>
                <el-button 
                  type="primary" 
                  size="big" 
                  :disabled="!hasSelectedRooms"
                  @click="submitSelectedVotes"
                >
                  提交选中投票
                </el-button>
              </div>
              <el-table 
                :data="getUnitFloors(unit)" 
                border 
                size="big"
                class="unit-table"
              >
                <el-table-column label="楼层" width="80" align="center">
                  <template #default="scope">
                    {{ scope.row.floor }}层
                  </template>
                </el-table-column>
                <el-table-column label="房间">
                  <template #default="scope">
                    <div class="room-grid">
                      <div
                        v-for="room in scope.row.rooms"
                        :key="room.id"
                        class="room-item"
                        :class="{
                          'voted': room.has_voted,
                          'selected': selectedRooms.includes(room.id)
                        }"
                        @click="toggleRoomSelection(room)"
                      >
                        {{ room.room_number }}
                      </div>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-card>
      </div>

      <div class="right-content">
        <el-card class="building-info">
          <template #header>
            <div class="card-header">
              <span>楼栋信息</span>
              <el-button 
                v-if="showResetButton"
                type="danger" 
                size="small"
                @click="showResetDialog = true"
              >
                重置数据
              </el-button>
            </div>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="单元数">{{ building.unit_count }}</el-descriptions-item>
            <el-descriptions-item label="楼层数">{{ building.floor_count }}</el-descriptions-item>
            <el-descriptions-item label="每层户数">{{ building.units_per_floor }}</el-descriptions-item>
            <el-descriptions-item label="总户数">{{ building.total_units }}</el-descriptions-item>
            <el-descriptions-item label="已投票">{{ votedCount }}</el-descriptions-item>
            <el-descriptions-item label="完成率">{{ completionRate }}%</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>
    </div>

    <el-dialog
      v-model="showConfirmDialog"
      title="确认投票"
      width="30%"
    >
      <span>确认以下房间已提交投票？</span>
      <div class="selected-rooms">
        <el-tag 
          v-for="room in getSelectedRoomsInfo" 
          :key="room.id"
          class="selected-room-tag"
        >
          {{ room.fullNumber }}
        </el-tag>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showConfirmDialog = false">取消</el-button>
          <el-button type="primary" @click="confirmVote">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="showResetDialog"
      title="确认重置"
      width="30%"
    >
      <span>确认要重置该楼栋所有投票数据吗？此操作不可恢复！</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showResetDialog = false">取消</el-button>
          <el-button type="danger" @click="resetBuildingData">
            确认重置
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const building = ref<any>({})
const selectedRooms = ref<number[]>([])
const showConfirmDialog = ref(false)
const showResetDialog = ref(false)

const buildingTitle = computed(() => `${building.value.building_number}栋`)
const votedCount = computed(() => building.value.units?.filter((u: any) => u.has_voted).length || 0)
const completionRate = computed(() => {
  if (!building.value.total_units) return 0
  return Math.round((votedCount.value / building.value.total_units) * 100)
})

const getProgressType = computed(() => {
  const rate = completionRate.value
  if (rate < 30) return 'danger'
  if (rate < 70) return 'warning'
  return 'success'
})

const hasSelectedRooms = computed(() => selectedRooms.value.length > 0)

const getSelectedRoomsInfo = computed(() => {
  return selectedRooms.value.map(id => {
    const room = building.value.units.find((u: any) => u.id === id)
    return {
      id: room.id,
      fullNumber: `${building.value.building_number}栋${room.unit_number}单元${room.floor}层${room.room_number}室`
    }
  })
})

// 获取楼栋数据
const fetchBuildingData = async () => {
  try {
    const response = await axios.get(`/api/buildings/${route.params.id}`)
    building.value = response.data
  } catch (error) {
    console.error('获取楼栋数据失败:', error)
    ElMessage.error('获取楼栋数据失败')
  }
}

// 获取单元楼层数据
const getUnitFloors = (unit: number) => {
  const floors = []
  for (let floor = 1; floor <= building.value.floor_count; floor++) {
    const rooms = building.value.units?.filter((u: any) => {
      return u.unit_number === String(unit) && u.floor === floor
    }) || []
    floors.push({ floor, rooms })
  }
  return floors
}

// 切换房间选择状态
const toggleRoomSelection = (room: any) => {
  if (room.has_voted) return
  const index = selectedRooms.value.indexOf(room.id)
  if (index === -1) {
    selectedRooms.value.push(room.id)
  } else {
    selectedRooms.value.splice(index, 1)
  }
}

// 提交选中的投票
const submitSelectedVotes = () => {
  if (selectedRooms.value.length === 0) return
  showConfirmDialog.value = true
}

// 确认投票
const confirmVote = async () => {
  try {
    await Promise.all(
      selectedRooms.value.map(roomId => 
        axios.post(`/api/votes/${roomId}`)
      )
    )
    ElMessage.success('投票成功')
    showConfirmDialog.value = false
    selectedRooms.value = []
    await fetchBuildingData()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '投票失败')
  }
}

// 重置楼栋数据
const resetBuildingData = async () => {
  try {
    await axios.post(`/api/buildings/${route.params.id}/reset`)
    ElMessage.success('数据重置成功')
    showResetDialog.value = false
    selectedRooms.value = []
    await fetchBuildingData()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '重置失败')
  }
}

const goBack = () => {
  router.push('/')
}

// 添加一个计算属性来控制重置按钮的显示
const showResetButton = computed(() => {
  // 这里可以根据需要添加显示条件
  return false; // 默认不显示
})

onMounted(() => {
  fetchBuildingData()
})
</script>

<style scoped>
.building-detail {
  max-width: 1400px;
  margin: 20px auto;
  padding: 0 20px;
}

.main-content {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.left-content {
  flex: 1;
  min-width: 0;
}

.right-content {
  width: 300px;
  flex-shrink: 0;
}

.building-info {
  position: sticky;
  top: 20px;
}

.page-header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.building-title {
  font-size: 20px;
  font-weight: bold;
}

.units-grid {
  margin-top: 20px;
}

.units-container {
  display: flex;
  gap: 20px;
  margin: 0 -10px;
}

.unit-section {
  flex: 1;
  min-width: 0;
  padding: 0 10px;
}

.unit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.unit-header h3 {
  margin: 0;
  font-size: 16px;
}

.room-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 10px;
  border-left: 1px solid #dcdfe6;
}

.room-item {
  width: 80px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s;
  position: relative;
}

.room-item::after {
  content: '';
  position: absolute;
  right: -15px;
  top: 0;
  height: 100%;
  width: 1px;
  background-color: #dcdfe6;
}

.room-item:last-child::after {
  display: none;
}

.room-item:not(.voted):hover {
  border-color: #409eff;
  color: #409eff;
}

.room-item.voted {
  background-color: #67c23a;
  border-color: #67c23a;
  color: white;
  cursor: not-allowed;
}

.room-item.selected {
  background-color: #f56c6c;
  border-color: #f56c6c;
  color: white;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.legend {
  display: flex;
  gap: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  font-weight: normal;
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}

.legend-color.not-voted {
  background-color: white;
}

.legend-color.selected {
  background-color: #f56c6c;
  border-color: #f56c6c;
}

.legend-color.voted {
  background-color: #67c23a;
  border-color: #67c23a;
}

.unit-table {
  margin-top: 10px;
  width: 100%;
}

:deep(.el-table) {
  --el-table-border-color: #dcdfe6;
  --el-table-header-bg-color: #f5f7fa;
}

:deep(.el-table th) {
  background-color: #f5f7fa;
  font-weight: bold;
  font-size: 16px;
  height: 50px;
}

:deep(.el-table td) {
  height: auto;
  padding: 0;
}

:deep(.el-table--border .el-table__cell) {
  border-right: 2px solid #dcdfe6;
}

.selected-rooms {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.selected-room-tag {
  margin: 5px;
}

:deep(.el-descriptions__label) {
  font-weight: bold;
  background-color: #f5f7fa;
}

:deep(.el-descriptions__content) {
  font-size: 14px;
}

:deep(.el-descriptions) {
  --el-descriptions-item-bordered-label-background: #f5f7fa;
}

.header-left,
.search-input,
.search-results,
:deep(.el-input__wrapper),
:deep(.el-input__inner) {
  display: none;
}
</style> 