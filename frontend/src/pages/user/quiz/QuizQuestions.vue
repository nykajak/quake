<script setup>
    import { api } from '@/api';
    import { ref } from 'vue';
    import QuizQuestion from './QuizQuestion.vue';

    const props = defineProps(['sid','cid','quiz_id','question_id'])

    let questions = ref([]);

    async function fetchQuestions(){
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`);
        questions.value = res.data.payload.map((x)=>{
            let y = {...x, 'sid':props.sid, 'cid':props.cid, 'quiz_id':props.quiz_id}
            return y;
        });
    }

    fetchQuestions();
</script>

<template>
    <QuizQuestion :question="questions[props.question_id - 1]" :index="props.question_id" :length="questions.length"/>
</template>

<style scoped>
</style>