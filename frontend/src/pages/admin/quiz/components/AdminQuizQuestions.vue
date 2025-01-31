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
            <div v-for="question in questions">
                <div class="d-flex justify-content-center">
                    <RouterLink :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                        {{ question.description }}
                    </RouterLink>
                </div>
            </div>
        </div>

        <div class="d-flex flex-column mt-3">
            <div>
                Search: <input type="text">
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>