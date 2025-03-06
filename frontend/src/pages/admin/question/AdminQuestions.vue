<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { RouterLink, useRoute } from 'vue-router';
import Pagination from '@/components/Pagination.vue';
import PerPage from '@/components/PerPage.vue';

import StaticQuestion from '@/components/StaticQuestion.vue';

const props = defineProps(['sid','cid'])
const route = useRoute();
const questions = ref(null);
const numPages = ref(null);

async function fetchQuestions(){
    let page = route.query.page ?? 1
    let per_page = route.query.per_page ?? 5
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/?page=${page}&per_page=${per_page}`)
    numPages.value = res.data.pages
    questions.value = res.data.payload.questions;
}

fetchQuestions()
</script>

<template>
    <div v-if="questions" class="d-flex flex-column flex-grow-1 pt-4">
        <div class="d-flex flex-column align-items-center gap-4">
            <div class="d-flex align-items-center gap-2">
                Entries per page: <PerPage/>
            </div>
            <div class="d-flex p-2 w-100 justify-content-center" v-for="question in questions">
                <RouterLink class="w-100" :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                    <StaticQuestion :description="question.description" />
                </RouterLink>
            </div>
            
            <div class="d-flex justify-content-center">
                <Pagination :pages="numPages" :url="route.fullPath"/>
            </div>
        </div>
    </div>
</template>

<style scoped>
.question-div{
    display: flex;
    justify-content: center;
    width: 100%;
    height: 2em;
}

.question-div-layout{
    display: flex;
    width: 50em;
    overflow:clip;
    gap: 1em;
    border: 1px solid var(--secondary-color);
}

.question-div-decoration{
    display: flex;
    width: 2em;
    height: 2em;
    background-color: var(--secondary-color);
    color: var(--light-color);
    justify-content: center;
    align-items: center;
}

.question-div-description{
    display: flex;
}

.question-text{
    display: flex;
    align-items: center;
}
</style>