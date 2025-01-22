import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/pages/Login.vue'
import About from '@/pages/About.vue'
import Register from '@/pages/Register.vue'
import NotFound from '@/pages/NotFound.vue'

import AdminDashboard from '@/pages/admin/AdminDashboard.vue'
import AdminUsers from '@/components/AdminUser/AdminUsers.vue'
import AdminUser from '@/components/AdminUser/AdminUser.vue'
import AdminSubjects from '@/components/AdminSubject/AdminSubjects.vue'
import AdminSubject from '@/components/AdminSubject/AdminSubject.vue'
import ChapterCard from '@/components/AdminChapter/ChapterCard.vue'
import AdminChapter from '@/components/AdminChapter/AdminChapter.vue'
import AdminEnrolled from '@/components/AdminEnrolled/AdminEnrolled.vue'
import AddSubject from '@/components/AdminSubject/AddSubject.vue'

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
          component: AdminUsers,
        },
        {
          path: "users/:uid",
          component: AdminUser,
          props: true,
        },
        {
          path:"subjects",
          component: AdminSubjects,
        },
        {
          path: "subjects/add",
          component: AddSubject,
          props: true,
        },
        {
          path: "subjects/:sid",
          component: AdminSubject,
          props: true,
        },
        {
          path: "subjects/:sid/enrolled",
          component: AdminEnrolled,
          props: true,
        },
        {
          path: "subjects/:sid/chapters/:cid",
          component: AdminChapter,
          props: true
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
