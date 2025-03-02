<script setup>

import router from '@/router';
import { ref, onMounted } from 'vue';
import { api } from '@/api';
import { useRoute } from 'vue-router';

import StaticOption from '@/components/StaticOption.vue';
import StaticQuestion from '@/components/StaticQuestion.vue';

const props = defineProps(['question', 'index', 'length']);
const route = useRoute();
let correct = ref(-2);

async function submitResponse(){
    try{
        let f = new FormData();
        f.append("marked",correct.value)
        let res = await api.post(`/user/subjects/${props.question.sid}/chapters/${props.question.cid}/quizes/${props.question.quiz_id}/questions/${props.question.id}`, f);
  
    }
    catch(err){
        console.log(err)
    }
}

async function fetchResponse(){
    let res = await api.get(`/user/subjects/${route.params.sid}/chapters/${route.params.cid}/quizes/${route.params.quiz_id}/questions/${props.question.id}`);
    correct.value = res.data.payload
}

fetchResponse();
</script>

<template>
<div v-if="question && correct != -2" class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <div class="question-container">
            <StaticQuestion :index="props.index" :description="props.question.description"/>
        </div>
        
        <div class="option-container">
            <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                <template v-for="n in 4">
                    <StaticOption :optionNo="n-1" :correctOption="correct" :option-text="props.question.options[n-1]" :clickable="(x)=>{
                        correct = x;
                    }"/>
                </template>
            </div>
            
            <div class="d-flex mt-3 justify-content-center">
                <button id="clear-button" @click="correct = -1">
                    Clear choice
                </button>
            </div>

            <div class="d-flex mt-3 justify-content-between">
                <button class="nav-button" @click="async ()=>{
                    await submitResponse();
                    router.push({
                        'path': `/user/subjects/${props.question.sid}/chapters/${props.question.cid}/quizes/${props.question.quiz_id}/questions/${Number(props.index) - 1}`
                    })}" :disabled="props.index == 1">
                    Save and prev
                </button>
                <button class="nav-button" @click="async ()=>{
                    await submitResponse();
                    router.push({
                        'path': `/user/subjects/${props.question.sid}/chapters/${props.question.cid}/quizes/${props.question.quiz_id}/questions/${Number(props.index) + 1}`
                    })}" :disabled="props.index == props.length">
                    Save and next
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.nav-button{
    justify-content: center;
    align-items: center;
    padding-left: 0.5em;
    padding-right: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    border: 1px solid var(--light-color);
    background-color: var(--primary-color);
    border-radius: 1em;
}

#clear-button{
    justify-content: center;
    align-items: center;
    padding: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    border: 1px solid var(--light-color);
    background-color: var(--error-color);
    border-radius: 1em;
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

.option-container{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    margin-top: 2em;
}

</style>