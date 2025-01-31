<script setup>
import { api } from '@/api';
import { ref } from 'vue';

const props = defineProps(['sid','cid']);
const questions = ref([]);

async function fetchQuestions(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions`);
    return res.data.payload.questions
}

fetchQuestions().then((data)=>{
    questions.value = data;
})

</script>

<template>
    <div>
        <div class="quiz-query-header">
            <input type="text">
            <button>Search</button>
        </div>

        <div class="quiz-query-body">
            <div v-for="question in questions">
                <div>{{ question.description }}</div>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>