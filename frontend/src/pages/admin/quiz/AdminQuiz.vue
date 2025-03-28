<script setup>
import { ref } from 'vue';
import { api } from '@/api';
import AdminQuizQuestions from './components/AdminQuizQuestions.vue';
import NavButton from '@/components/NavButton.vue';
import DeleteButton from '@/components/DeleteButton.vue';

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
    <div v-if="quiz" class="d-flex flex-column flex-grow-1 align-items-center mt-3">
        <h3>
            On {{ quiz.dated.day }}-{{ quiz.dated.month }}-{{ quiz.dated.year }}, at {{ quiz.dated.hour }}:{{ quiz.dated.minute }}
        </h3>
        <p class="text-center">
            Description: {{ quiz.description }}
            <br>
            Quiz duration: {{ quiz.duration  }} minutes
        </p>
        <div class="d-flex mb-3">
            <NavButton text="Modify questions" :url="`${props.qid}/search`" color="primary"/>
            <NavButton text="View responses" :url="`${props.qid}/responses`" color="secondary"/>
            <NavButton text="Edit quiz" :url="`${props.qid}/edit`" color="tertiary"/>
            <DeleteButton :redirect="`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/`" :url="`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}`" color="error">
                Delete quiz
            </DeleteButton>
        </div>
        <AdminQuizQuestions :sid="props.sid" :cid="props.cid" :qid="props.qid"/>
    </div>
</template>

<style scoped>
</style>