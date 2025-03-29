<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import QuizSummary from './components/QuizSummary.vue';
    import Loader from '@/components/Loader.vue';
    import { RouterLink } from 'vue-router';

    const props = defineProps(['quiz','uid','sid','cid'])

    const correctResponses = ref(null);
    const wrongResponses = ref(null);
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
    <div v-if="quiz" class="container-quiz-score">
        <div class="d-flex flex-grow-1">
            <div class="d-flex flex-column align-items-center flex-grow-1">
                <div>
                    <h4 class="d-flex justify-content-center">
                        <RouterLink :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${quiz.id}`">
                            Quiz ID #{{ quiz.id }}
                        </RouterLink>
                        
                    </h4>
                    <p class="text-center">
                        {{ quiz.description ?? 'No description provideed!'}}
                    </p>
                    <RouterLink class="d-flex justify-content-center" :to="`${cid}/quizes/${quiz.id}`">
                        Show Responses
                    </RouterLink>
                </div>
            </div>
        </div>
        <div class="d-flex w-75 justify-content-end align-items-center">
            <div v-if="correctResponses + wrongResponses + unattemptedQuestions > 0">
                <QuizSummary :data="[correctResponses,wrongResponses,unattemptedQuestions]"/>
            </div>
            <div v-else>
                <QuizSummary :data="[correctResponses,wrongResponses,10000]"/>
            </div>
        </div>
    </div>
    <Loader v-else/>
</template>

<style scoped>
.container-quiz-score{
    display: flex;
    align-items: center;
    width: 100%;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
}
</style>