<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import QuizSummary from './components/QuizSummary.vue';
    import Loader from '@/components/Loader.vue';
    import { RouterLink } from 'vue-router';

    const color1 = window.getComputedStyle(document.body).getPropertyValue('--tertiary-color');
    const color2 = window.getComputedStyle(document.body).getPropertyValue('--error-color');
    const color3 = window.getComputedStyle(document.body).getPropertyValue('--contrast-color');

    const props = defineProps(['quiz','uid','sid','cid'])

    const correctResponses = ref(null);
    const wrongResponses = ref(null);

    const attemptedQuestions = ref(null);
    const unattemptedQuestions = ref(null);

    async function fetchQuizStats(){
        let res = await api.get(`/admin/scores/users/${props.uid}/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz.id}`);
        correctResponses.value = res.data.correct_count
        wrongResponses.value = res.data.response_count - res.data.correct_count
        unattemptedQuestions.value = res.data.question_count - res.data.response_count
    }

    fetchQuizStats();
</script>

<template>
    <div v-if="quiz" class="d-flex align-items-center">
        <div class="d-flex flex-grow-1">
            <div class="d-flex flex-column align-items-center flex-grow-1">
                <RouterLink :to="`${cid}/quizes/${quiz.id}`">
                    <h4>
                        Quiz ID #{{ quiz.id }}
                    </h4>
                </RouterLink>
                {{ quiz.description ?? 'No description provideed!'}}
            </div>
        </div>
        <div class="d-flex w-75 justify-content-between align-items-center">
            <QuizSummary :correct-responses="correctResponses" :wrong-responses="wrongResponses" :unattempted-questions="unattemptedQuestions" :color1="color1" :color2="color2" :color3="color3"/>
        </div>
    </div>
    <Loader v-else/>
</template>

<style scoped>

</style>