<script setup>

import { api } from '@/api';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import Message from '@/components/Message.vue';

const router = useRouter();

const quiz = ref(null);
const date = ref(null);
const errorMessage = ref('');
const loading = ref(false);
const ready = ref(false);
const props = defineProps(['sid','cid','qid'])

async function fetchQuiz(){
    try{
        loading.value = true;
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}`);
        loading.value = false;
        return res.data.payload
    }

    catch(err){
        loading.value = false;
        router.push({"name":"NotFound"})
        return -1
    }
}

fetchQuiz().then(data => {
    if (data != -1){
        quiz.value = data;
        ready.value = true;
        date.value = quiz.value.dated.year + "-" + String(quiz.value.dated.month).padStart(2, '0') + "-" + String(quiz.value.dated.day).padStart(2, '0') + "T" + String(quiz.value.dated.hour).padStart(2, '0') + ":" + String(quiz.value.dated.minute).padStart(2, '0')
    }
})

async function editQuiz(e){
    try{
        let res = await api.put(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}`,new FormData(e.target));
    }
    catch(err){
        errorMessage.value = err.response.data.msg
        return
    }

    router.push({
        'path': `/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}`
    })
}

</script>

<template>
    <Message v-if='errorMessage' level="danger" :hide-function="()=>{
        errorMessage = ''
    }">
        {{ errorMessage }}
    </Message>
    <div v-if="quiz" class="d-flex flex-column flex-grow-1">
        <form @submit.prevent="editQuiz" class="form-container-div">
            <legend class="text-center">Edit quiz details</legend>
            <div class="form-info-div">
                <div class="form-info-inner-div">
                    <label class="form-label" for="dated">Quiz Timing: </label>
                    <input class="border-input" type="datetime-local" id="dated" name="dated" required :value="date">
                </div>
                <div class="form-info-inner-div">
                    <label class="form-label" for="duration">Quiz duration (mins): </label>
                    <input class="border-input" type="number" id="duration" name="duration" required :value="quiz.duration">
                </div>
            </div>
            <div class="form-input-div">
                <label class="form-label" for="description">Description: </label>
                <input class="form-input border-input" type="text" name="description" id="description" :value = "quiz.description">
            </div>
            <div class="form-input-div">
                <input class="form-input submit-button" type="submit" value="Edit Quiz">
            </div>
        </form>
    </div>
</template>

<style scoped>

#dated,#duration{
    text-align: center;
}

#description{
    padding-left: 1em;
}

.submit-button{
    background-color: var(--secondary-color);
    color: var(--light-color);
}

.border-input{
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.form-container-div{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1em;
    padding-top: 2em;
}

label,input{
    height: 100%;   
    display:flex;
    align-items:center;
    background-color: light-dark(var(--light-color),var(--dark-color));
    outline: none;
    border:none;
}

.form-input-div{
    display: flex;
    justify-content: space-between;
    gap:1em;
    width: 75%;
}

.form-info-div{
    display: flex;
    width: 75%;
    gap: 2em;
    justify-content: start;
}

.form-info-inner-div{
    display: flex;
    gap: 1em;
}

.form-input{
    display: flex;
    flex-grow: 1;
}

.form-label{
    display: flex;
    min-width: fit-content;
    justify-content: center;
}
</style>