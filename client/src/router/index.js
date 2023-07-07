import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import PrimeVueComponentsView from '@/views/PrimeVueComponentsView.vue'
import RouterView from '@/views/RouterView.vue'
import ComponentsView from '@/views/ComponentsView.vue'
import DirectivesView from '@/views/DirectivesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
    },
    {
      path: '/pv-components',
      name: 'PrimeVueComponents',
      component: PrimeVueComponentsView,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('../views/AboutView.vue')
    },
    {
      path: '/router',
      name: 'Router',
      component: RouterView,
    },
    {
      path: '/components',
      name: 'Components',
      component: ComponentsView,
    },
    {
      path: '/directives',
      name: 'Directives',
      component: DirectivesView,
    },
  ],
})

export default router
