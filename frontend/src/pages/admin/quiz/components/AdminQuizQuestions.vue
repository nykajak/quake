<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { RouterLink } from 'vue-router';
import NavButton from '@/components/NavButton.vue';
import StaticQuestion from '@/components/StaticQuestion.vue';

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
                <NavButton text="Modify questions" :url="`${props.sid}/search`" color="primary"/>
                <NavButton text="View responses" :url="`${props.sid}/responses`" color="secondary"/>
            </div>

            <div class="d-flex p-2 w-100 justify-content-center" v-for="question in questions">
                <RouterLink class="w-100" :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                    <StaticQuestion :description="question.description" />
                </RouterLink>
            </div>
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