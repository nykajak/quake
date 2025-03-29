<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { useRoute } from 'vue-router';

import { RouterLink } from 'vue-router';
import NavButton from '@/components/NavButton.vue';
import StaticQuestion from '@/components/StaticQuestion.vue';
import PaginationToolBar from '@/components/PaginationToolBar.vue';

const props = defineProps(['sid','cid','qid']);
const route = useRoute();
const questions = ref(null);
const pages = ref(null);

async function fetchQuestions(){
    let page = route.query.page ?? 1;
    let per_page = route.query.per_page ?? 5
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions?page=${page}&per_page=${per_page}`);
    questions.value = res.data.payload
    pages.value = res.data.pages;
}

fetchQuestions()

</script>

<template>
    <div class="d-flex flex-column align-items-center w-100 flex-grow-1">
        <div class="d-flex flex-column align-items-center w-100 flex-grow-1">
            <div v-if="questions && pages" class="d-flex p-2 w-100 justify-content-center" v-for="question in questions">
                <RouterLink class="w-75 remove-underline" :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                    <StaticQuestion class="w-100" :description="question.description" />
                </RouterLink>
            </div>
        </div>
        <PaginationToolBar :num-pages="pages"/>
    </div>
</template>

<style scoped>
.remove-underline{
    text-decoration: none;
}

.option-div{
    display: flex;
    flex-direction: row;
    margin-bottom: 1.5em;
}

.option-button{
    display: flex;
    border: none;
    color: var(--light-color);
}

#add-button{
    background-color: var(--tertiary-color);
}

#search-button{
    background-color: var(--secondary-color);
}

.question-decorator{
    display: flex;
    width: 1.5em;
    height: 1.5em;
    justify-content: center;
    background-color: var(--secondary-color);
    color: var(--light-color);  
}

.question-div{
    display: flex;
    width: 40em;
    padding: 0.5em;
    gap:0.5em;  
}

.results-div{
    display: flex;
    flex-direction: column;
    gap:0.5em;
}
</style>