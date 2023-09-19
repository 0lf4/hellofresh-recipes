// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/views/WeeklyMenu.vue'),
  },
  {
    path: '/recipes',
    children: [
      {
        path: '/recipes',
        name: 'Recipe',
        component: () => import('@/views/Recipe.vue'),
      },
    ],
  },
  {
    path: '/weekly-menu',
    children: [
      {
        path: '/weekly-menu',
        name: 'WeeklyMenu',
        component: () => import('@/views/WeeklyMenu.vue'),
      },
    ],
  },
  {
    path: '/scrapper',
    children: [
      {
        path: '/scrapper',
        name: 'Scrapper',
        component: () => import('@/views/Scrapper.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
