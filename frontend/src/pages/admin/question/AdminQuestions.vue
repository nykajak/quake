<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { RouterLink, useRoute } from 'vue-router';

const props = defineProps(['sid','cid'])
const route = useRoute();
const questions = ref([]);

async function fetchQuestions(){
    let page = route.query.page ?? 1
    let per_page = route.query.per_page ?? 5
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/?page=${page}&per_page=${per_page}`)
    questions.value = res.data.payload.questions;
}

fetchQuestions()
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 pt-4">
        <div class="d-flex flex-column align-items-center gap-4">
            <div class="question-div" v-for="question in questions">
                <div class="question-div-layout">
                    <div class="question-div-decoration">
                        Q
                    </div>
                    <div class="question-div-description">
                        <RouterLink :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                            <p class="question-text">{{ question.description.length < 100 ? question.description: question.description.slice(0,100) + "..." }}</p>
                        </RouterLink>
                    </div>
                </div>
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