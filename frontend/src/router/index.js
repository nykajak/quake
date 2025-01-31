import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/pages/anon/Login.vue'
import About from '@/pages/anon/About.vue'
import Register from '@/pages/anon/Register.vue'
import NotFound from '@/pages/anon/NotFound.vue'

import UserDashboard from '@/pages/user/UserDashboard.vue'

import AdminDashboard from '@/pages/admin/AdminDashboard.vue'
import AdminUsers from '@/components/AdminUser/AdminUsers.vue'
import AdminUser from '@/components/AdminUser/AdminUser.vue'
import AdminSubjects from '@/components/AdminSubject/AdminSubjects.vue'
import AdminSubject from '@/components/AdminSubject/AdminSubject.vue'
import AdminChapter from '@/components/AdminChapter/AdminChapter.vue'
import AdminEnrolled from '@/components/AdminEnrolled/AdminEnrolled.vue'
import AddSubject from '@/components/AdminSubject/AddSubject.vue'
import UserSubjects from '@/pages/user/subject/UserSubjects.vue'
import UserSubject from '@/pages/user/subject/UserSubject.vue'
import AddChapter from '@/components/AdminSubject/AddChapter.vue'
import QuestionCard from '@/components/AdminQuestion/QuestionCard.vue'
import QuestionAdd from '@/components/AdminQuestion/QuestionAdd.vue'
import QuestionEdit from '@/components/AdminQuestion/QuestionEdit.vue'
import AllQuestion from '@/components/AdminQuestion/AllQuestion.vue'
import AdminQuizes from '@/components/AdminQuiz/AdminQuizes.vue'
import AdminQuiz from '@/components/AdminQuiz/AdminQuiz.vue'

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
      name:"userDash",
      path: "/user",
      component: UserDashboard,
      children: [
        {
          path:"subjects",
          component: UserSubjects,
        },
        {
          path:"subjects/:sid",
          component: UserSubject,
          props: true
        },
      ]
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
          path: "subjects/:sid/chapters/add",
          component: AddChapter,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid",
          component: AdminChapter,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/quizes",
          component: AdminQuizes,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/quizes/:qid",
          component: AdminQuiz,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/questions/add",
          component: QuestionAdd,
          props:true
        },
        {
          path: "subjects/:sid/chapters/:cid/questions/:qid",
          component: QuestionCard,
          props:true
        },
        {
          path: "subjects/:sid/chapters/:cid/questions/:qid/edit",
          component: QuestionEdit,
          props:true
        },
        {
          path: "subjects/:sid/chapters/:cid/questions",
          component: AllQuestion,
          props:true
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
