<script setup>

import { api } from '@/api';
import { useRouter } from 'vue-router';

const props = defineProps(['sid','cid'])
const router = useRouter()

async function createQuiz(e){
    let res = await api.post(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/`,new FormData(e.target));
    router.push({
        'path': `/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${res.data.payload}`
    })
}

</script>

<template>
    <div class="d-flex flex-column flex-grow-1">
        <form @submit.prevent="createQuiz" class="form-container-div">
            <legend class="text-center">Quiz creation form</legend>
            <div class="form-info-div">
                <div class="form-info-inner-div">
                    <label class="form-label" for="dated">Quiz Timing: </label>
                    <input class="border-input" type="datetime-local" id="dated" name="dated" required>
                </div>
                <div class="form-info-inner-div">
                    <label class="form-label" for="duration">Quiz duration (mins): </label>
                    <input class="border-input" type="number" id="duration" name="duration" value="30" required>
                </div>
            </div>
            <div class="form-input-div">
                <label class="form-label" for="description">Description: </label>
                <input class="form-input border-input" type="text" name="description" id="description">
            </div>
            <div class="form-input-div">
                <input class="form-input submit-button" type="submit" value="Create Quiz">
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