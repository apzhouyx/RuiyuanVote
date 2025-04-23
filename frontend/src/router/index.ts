import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import BuildingDetail from '../views/BuildingDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/building/:id',
    name: 'BuildingDetail',
    component: BuildingDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 