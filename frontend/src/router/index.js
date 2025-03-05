import { createRouter, createWebHistory } from 'vue-router'
import { api } from '@/api'

import NotFound from '@/pages/anon/NotFound.vue'

import Login from '@/pages/anon/Login.vue'
import About from '@/pages/anon/About.vue'
import Register from '@/pages/anon/Register.vue'

import UserDashboard from '@/pages/user/UserDashboard.vue'
import UserSubjects from '@/pages/user/subject/UserSubjects.vue'
import UserSubject from '@/pages/user/subject/UserSubject.vue'
import UserChapter from '@/pages/user/chapter/UserChapter.vue'
import UserEnroll from '@/pages/user/enroll/UserEnroll.vue'
import QuizQuestions from '@/pages/user/quiz/QuizQuestions.vue'
import QuizStart from '@/pages/user/quiz/QuizStart.vue'

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
import AdminRequests from '@/pages/admin/enrolled/AdminRequests.vue'
import UserQuizResponses from '@/pages/user/responses/UserQuizResponses.vue'
import AdminResponse from '@/pages/admin/response/AdminResponse.vue'
import AdminQuizResponses from '@/pages/admin/response/AdminQuizResponses.vue'
import AdminUserResponses from '@/pages/admin/response/AdminUserResponses.vue'
import AdminQuestionResponses from '@/pages/admin/response/AdminQuestionResponses.vue'

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
      beforeEnter: async (to,from) => {
        let res = await api.get("/");
        if (res.data.role == "user"){
          return true;
        }
        else if (res.data.role == "admin"){
          return {"path": "/admin"};
        }
        return {"name" : "login"};
      },
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
        {
          path:"subjects/:sid/chapters/:cid",
          component: UserChapter,
          props: true
        },
        {
          path:"subjects/:sid/chapters/:cid/quizes/:qid",
          component: QuizStart,
          props: true
        },
        {
          path:"subjects/:sid/chapters/:cid/quizes/:qid/responses",
          component: UserQuizResponses,
          props: true
        },
        {
          path:"subjects/:sid/chapters/:cid/quizes/:quiz_id/questions/:question_id",
          component: QuizQuestions,
          props: true
        },
        {
          path: "subjects/enroll",
          component: UserEnroll,
          props: true
        }
      ]
    },
    {
      name: "adminDash",
      path: "/admin",
      component: AdminDashboard,
      beforeEnter: async (to,from) => {
        let res = await api.get("/");
        if (res.data.role == "admin"){
          return true;
        }
        else if (res.data.role == "user"){
          return {"path": "/user"};
        }
        return {"name" : "login"};
      },
      children: [
        {
          name: "test",
          path: "test",
          component: AdminResponse
        },
        {
          path:"requests",
          component: AdminRequests,
        },
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
          path: "users/:uid/responses",
          component: AdminUserResponses,
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
          path: "subjects/:sid/chapters/:cid/quizes/:qid/responses",
          component: AdminQuizResponses,
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
          path: "subjects/:sid/chapters/:cid/questions/:qid/responses",
          component: AdminQuestionResponses,
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
