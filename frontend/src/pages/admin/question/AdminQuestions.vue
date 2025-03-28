<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { RouterLink, useRoute } from 'vue-router';
import PaginationToolBar from '@/components/PaginationToolBar.vue';
import NavButton from '@/components/NavButton.vue';

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
    questions.value = res.data.payload;
}

fetchQuestions()
</script>

<template>
    <div v-if="questions" class="d-flex flex-column flex-grow-1 pt-4">
        <div class="d-flex flex-column align-items-center gap-4 flex-grow-1">
            <h3 class="headingInfo">
                Showing all questions in current chapter
            </h3>
            <div>
                <NavButton url="questions/add" color="primary" text="Add new question"/>
            </div>
            <div class="d-flex flex-grow-1 flex-column w-100">
                <div class="d-flex p-2 w-100 justify-content-center" v-for="question in questions">
                    <RouterLink class="w-75" :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                        <StaticQuestion :description="question.description" />
                    </RouterLink>
                </div>
            </div>
            <PaginationToolBar :num-pages="numPages"/>
        </div>
    </div>
</template>

<style scoped>
.headingInfo{
    font-size: 2.5em;
}

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