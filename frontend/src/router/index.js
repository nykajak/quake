import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/pages/Login.vue'
import About from '@/pages/About.vue'
import Register from '@/pages/Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: "home",
      path: "/",
      component: About
    },
    {
      name: "login",
      path: "/login",
      component: Login
    },
    {
      name: "register",
      path: "/register",
      component: Register
    }
  ],
})

export default router
