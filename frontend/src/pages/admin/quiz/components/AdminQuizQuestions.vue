<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { RouterLink } from 'vue-router';

const props = defineProps(['sid','cid','qid']);
const questions = ref([]);

async function fetchQuestions(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions`);
    return res.data.payload
}

fetchQuestions().then((data)=>{
    questions.value = data;
})

</script>

<template>
    <div class="d-flex flex-column align-items-center">
        <div class="d-flex flex-column align-items-center">
            <h3>Questions</h3>
            <div class="option-div">
                <button class="option-button" id="add-button">Modify</button>
                <button class="option-button" id="search-button">Search</button>
            </div>

            <div class="results-div mt-2">
                <div v-for="question in questions" class="question-div">
                    <div class="question-decorator">
                        Q
                    </div>
                    <div class="d-flex flex-grow-1">
                        <RouterLink :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                            {{ question.description.length < 90 ? question.description : question.description.slice(0,85) + "..." }}
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.option-div{
    display: flex;
    flex-direction: row;
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