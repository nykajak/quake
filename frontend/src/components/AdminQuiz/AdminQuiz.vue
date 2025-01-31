<script setup>
import { ref } from 'vue';
import { api } from '@/api';

const props = defineProps(['sid','cid','qid'])
const quiz = ref(null);

async function fetchQuiz(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}`);
    return res.data.payload;
}


fetchQuiz().then((data)=>{
    quiz.value = data;
})
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 align-items-center mt-3">
        <h3>
            On {{ quiz.dated.day }}-{{ quiz.dated.month }}-{{ quiz.dated.year }}, at {{ quiz.dated.hour }}:{{ quiz.dated.minute }}
        </h3>
        <p class="text-center">
            Description: {{ quiz.description }}
            <br>
            Quiz duration: {{ quiz.duration  }} minutes
        </p>
    </div>
    {{ quiz }}
</template>

<style scoped>
</style>