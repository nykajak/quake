import { createRouter, createWebHistory } from 'vue-router'

import NotFound from '@/pages/anon/NotFound.vue'

import Login from '@/pages/anon/Login.vue'
import About from '@/pages/anon/About.vue'
import Register from '@/pages/anon/Register.vue'

import UserDashboard from '@/pages/user/UserDashboard.vue'
import UserSubjects from '@/pages/user/subject/UserSubjects.vue'
import UserSubject from '@/pages/user/subject/UserSubject.vue'

import AdminDashboard from '@/pages/admin/AdminDashboard.vue'

import AdminChapter from '@/pages/admin/chapter/AdminChapter.vue'
import AdminChapterAdd from '@/pages/admin/chapter/AdminChapterAdd.vue'
import AdminChapterEdit from '@/pages/admin/chapter/AdminChapterEdit.vue'

import AdminEnrolled from '@/pages/admin/enrolled/AdminEnrolled.vue'

import AdminQuestion from '@/pages/admin/question/AdminQuestion.vue'
import AdminQuestions from '@/pages/admin/question/AdminQuestions.vue'
import AdminQuestionAdd from '@/pages/admin/question/AdminQuestionAdd.vue'
import AdminQuestionEdit from '@/pages/admin/question/AdminQuestionEdit.vue'

import AdminQuiz from '@/pages/admin/quiz/AdminQuiz.vue'
import AdminQuizes from '@/pages/admin/quiz/AdminQuizes.vue'
import AdminQuizAdd from '@/pages/admin/quiz/AdminQuizAdd.vue'
import AdminQuizEdit from '@/pages/admin/quiz/AdminQuizEdit.vue'
import AdminQuizSearch from '@/pages/admin/quiz/AdminQuizSearch.vue'

import AdminSubject from '@/pages/admin/subject/AdminSubject.vue'
import AdminSubjects from '@/pages/admin/subject/AdminSubjects.vue'
import AdminSubjectAdd from '@/pages/admin/subject/AdminSubjectAdd.vue'
import AdminSubjectEdit from '@/pages/admin/subject/AdminSubjectEdit.vue'

import AdminUser from '@/pages/admin/user/AdminUser.vue'
import AdminUsers from '@/pages/admin/user/AdminUsers.vue'

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
          component: AdminSubjectAdd,
          props: true,
        },
        {
          path: "subjects/:sid",
          component: AdminSubject,
          props: true,
        },
        {
          path: "subjects/:sid/edit",
          component: AdminSubjectEdit,
          props: true,
        },
        {
          path: "subjects/:sid/enrolled",
          component: AdminEnrolled,
          props: true,
        },
        {
          path: "subjects/:sid/chapters/add",
          component: AdminChapterAdd,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid",
          component: AdminChapter,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/edit",
          component: AdminChapterEdit,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/quizes",
          component: AdminQuizes,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/quizes/add",
          component: AdminQuizAdd,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/quizes/:qid/edit",
          component: AdminQuizEdit,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/quizes/:qid",
          component: AdminQuiz,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/quizes/:qid/search",
          component: AdminQuizSearch,
          props: true
        },
        {
          path: "subjects/:sid/chapters/:cid/questions/add",
          component: AdminQuestionAdd,
          props:true
        },
        {
          path: "subjects/:sid/chapters/:cid/questions/:qid",
          component: AdminQuestion,
          props:true
        },
        {
          path: "subjects/:sid/chapters/:cid/questions/:qid/edit",
          component: AdminQuestionEdit,
          props:true
        },
        {
          path: "subjects/:sid/chapters/:cid/questions",
          component: AdminQuestions,
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
