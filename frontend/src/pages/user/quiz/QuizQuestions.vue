<script setup>
    import { api } from '@/api';
    import QuizQuestion from './QuizQuestion.vue';

    const props = defineProps(['sid','cid','quiz_id','question_id'])

    let question = ref(null);

    async function fetchQuestion(){
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}/questions/${props.question_id}`);
        question.value = res.data.payload;
    }

    fetchQuestion();
</script>

<template>
    <QuizQuestion :question="question"/>
</template>

<style scoped>
</style>