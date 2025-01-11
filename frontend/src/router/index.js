import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/pages/Login.vue'
import About from '@/pages/About.vue'
import Register from '@/pages/Register.vue'
import AdminDashboard from '@/pages/AdminDashboard.vue'
import NotFound from '@/pages/NotFound.vue'

import AdminUsers from '@/components/AdminUsers.vue'

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
    },
    {
      name: "adminDash",
      path: "/admin",
      component: AdminDashboard,
      children: [
        {
          path:"users",
          component: AdminUsers
        }
      ]
    },
    { 
      path: '/:pathMatch(.*)*', 
      name: 'NotFound',
      component: NotFound
    },
  ],
})

export default router
