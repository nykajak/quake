<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { useRoute } from 'vue-router';

import { RouterLink } from 'vue-router';
import NavButton from '@/components/NavButton.vue';
import StaticQuestion from '@/components/StaticQuestion.vue';
import Pagination from '@/components/Pagination.vue';
import PerPage from '@/components/PerPage.vue';

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
    <div class="d-flex flex-column align-items-center w-100">
        <div class="d-flex flex-column align-items-center w-100">
            <h3>Questions</h3>
            <div class="option-div">
                <NavButton text="Modify questions" :url="`${props.qid}/search`" color="primary"/>
                <NavButton text="View responses" :url="`${props.qid}/responses`" color="secondary"/>
            </div>
            
            <div class="d-flex gap-2 align-items-center">
                Questions per page: <PerPage/>
            </div>
            <div v-if="questions && pages" class="d-flex p-2 w-100 justify-content-center" v-for="question in questions">
                <RouterLink class="w-75" :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                    <StaticQuestion class="w-100" :description="question.description" />
                </RouterLink>
            </div>
            <Pagination :url="route.fullPath" :pages="pages"/>
        </div>
    </div>
</template>

<style scoped>
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