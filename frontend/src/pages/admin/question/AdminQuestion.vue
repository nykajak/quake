<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { useRouter } from 'vue-router';

import StaticOption from './components/StaticOption.vue';
import StaticQuestion from './components/StaticQuestion.vue';

const router = useRouter();

const question = ref(null);
const props = defineProps(['sid','cid','qid'])

async function fetchQuestion(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}`)
    return res.data.payload;
}

fetchQuestion().then((data)=>{
    question.value = data;
})
</script>

<template>
    <div v-if="question" class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <div class="question-container">
            <StaticQuestion :index="question.id" :description="question.description" />
        </div>
        
        <div class="option-container">
            <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                <template v-for="n in 4">
                    <StaticOption :optionNo="n - 1" :correctOption="question.correct" :optionText="question.options[n - 1]"/>
                </template>
            </div>
        </div>

        <div class="d-flex justify-content-center mt-4">
            <button id="edit-button" @click="router.push(
                {
                    'path': `/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}/edit`
                }
            )">
                Edit Question
            </button>
        </div>
    </div>

</template>

<style scoped>

#edit-button{
    border: 1px solid var(--light-color);
    color: var(--light-color);
    background-color: var(--tertiary-color);
    padding: 0.5em;
    border-radius: 10px;
}

.option-button:has(.selected-option){
    input{
        background-color: green !important;
        border-color: green !important;    
        transition: none;
    }
    background-color: green !important;
}

.selected-option{
    background-color: green !important;
}

.question-container{
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 1px solid var(--light-color);
    padding: 0.33em;
    color: var(--light-color);
    background-color: var(--secondary-color);
}

.question-no-div{
    display: flex;
    flex-direction: row;
    height: 100%;
    margin: 0.33em;
    padding: 0.33em;
}

.question-no-div div{
    display: flex;
    border: 1px solid var(--light-color);
    width: 2em;
    height: 2em;
    justify-content: center;
    align-items: center;
    border-radius: 100%;
}

.question-statement-div{
    display: flex;
    justify-content: center;
    flex-grow: 1;
    text-align: center;
}

.option-container{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    margin-top: 2em;
}

.option-text{
    justify-content: center;
    display: flex;
    flex-grow: 1;
}

.option-button{
    max-width: 25%;
    display: flex;
    flex-grow: 1;
    justify-content: center;
    align-items: center;
    padding: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    border: 1px solid var(--light-color);
    background-color: var(--secondary-color);
    border-radius: 1em;
}

.rounded-div{
    border: 1px solid var(--light-color);
    border-radius: 100%;
    width: 1.5em;
    height: 1.5em;
    display: flex;
    flex-shrink: 0;
    justify-content: center;
    align-items: center;
    margin: 0.33em;
}
</style>