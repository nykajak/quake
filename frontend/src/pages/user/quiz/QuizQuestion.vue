<script setup>

import { ref, onMounted } from 'vue';
import { api } from '@/api';
import { useRoute,useRouter } from 'vue-router';

import StaticOption from '@/components/StaticOption.vue';
import StaticQuestion from '@/components/StaticQuestion.vue';
import QuizNavigation from './components/QuizNavigation.vue';
import Loader from '@/components/Loader.vue';

const route = useRoute();
const router = useRouter();
const props = defineProps(['sid','cid','quiz_id','question_id']);

const correct = ref(-2);
const question = ref(null);
const num = ref(null);
const time = ref(null);
const shown = ref(false)

function formatTime(time){
    if (time > 0){
        return `${Math.floor(time / 60)}  minutes and ${time % 60} seconds left!`;
    }
    else{
        return `You are out of time!`
    }
}

async function fetchQuestion(){
    let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}/questions/${props.question_id}`);
    correct.value = res.data.payload;
    question.value = res.data.question;
    num.value = res.data.num;
    time.value = res.data.time;
}

async function submitResponse(){
    try{
        let f = new FormData();
        f.append("marked",correct.value)
        let res = await api.post(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}/questions/${props.question_id}`, f);
  
    }
    catch(err){
        console.log(err)
        router.go(-1);
    }
}

fetchQuestion();

let interval_id = setInterval(() => {
    time.value -= 1;
    if (time.value <= 0){
        clearInterval(interval_id);
        router.push({
            "path": `/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`
        })
    }
},1000)

</script>

<template>
    <template v-if="time > 0">

        <div v-if="question" class="d-flex w-100 flex-column align-self-center m-1 p-1">
            <div class="timerDiv">
                {{formatTime(time)}}
            </div>
            <div class="question-container">
                <StaticQuestion :index="props.question_id" :description="question.description"/>
            </div>
            
            <div class="option-container">
                <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                    <template v-for="n in 4">
                        <StaticOption :optionNo="n-1" :correctOption="correct" :option-text="question.options[n-1]" :clickable="(x)=>{
                            correct = x;
                        }"/>
                    </template>
                </div>

                <div class="d-flex mt-3 justify-content-between">
                    <button class="nav-button" @click="async ()=>{
                        await submitResponse();
                        router.push({
                            'path': `/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}/questions/${Number(props.question_id) - 1}`
                        })}" :disabled="props.question_id == 1">
                        Save and prev
                    </button>
                    <button id="clear-button" @click="correct = -1">
                        Clear choice
                    </button>
                    <button class="nav-button" @click="async ()=>{
                        await submitResponse();
                        router.push({
                            'path': `/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}/questions/${Number(props.question_id) + 1}`
                        })}" :disabled="props.question_id == num">
                        Save and next
                    </button>
                </div>
            </div>
        </div>
        
        <div class="d-flex flex-grow-1 flex-column justify-content-end">
            <div v-if="shown">
                <QuizNavigation :length="num" :beforeSubmit="submitResponse" :current="props.question_id" :url="`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}/questions`"/>
            </div>
            <button id="toggleButton" @click="shown = !shown">
                <template v-if="!shown">
                    Show navigation bar
                </template>
                <template v-else>
                    Hide navigation bar
                </template>
            </button>
            <div class="d-flex justify-content-center">
            </div>
        </div>
    </template>
    <Loader v-else/>

</template>

<style scoped>
#toggleButton{
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background-color: var(--primary-color);
    color: var(--light-color);
}

.timerDiv{
    display: flex;
    justify-content: end;
    padding: 0.2em;
    background-color: var(--primary-color);
    color: var(--light-color);
    margin-bottom: 0;
}
.nav-button{
    justify-content: center;
    align-items: center;
    padding-left: 0.5em;
    padding-right: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    background-color: var(--primary-color);
    border: none;
}

#clear-button{
    justify-content: center;
    align-items: center;
    padding: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    background-color: var(--error-color);
    border: none;
}

.question-container{
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0.33em;
    width: 100%;
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