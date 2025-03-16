<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import Accuracy from './components/Accuracy.vue'
    import Coverage from './components/Coverage.vue'
    import { RouterLink } from 'vue-router';

    const color1 = window.getComputedStyle(document.body).getPropertyValue('--tertiary-color');
    const color2 = window.getComputedStyle(document.body).getPropertyValue('--error-color');

    const props = defineProps(['quiz','uid','sid','cid'])

    const correctResponses = ref(null);
    const wrongResponses = ref(null);

    const attemptedQuestions = ref(null);
    const unattemptedQuestions = ref(null);

    async function fetchQuizStats(){
        let res = await api.get(`/admin/scores/users/${props.uid}/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz.id}`);
        correctResponses.value = res.data.correct
        wrongResponses.value = res.data.count - res.data.correct

        res = await api.get(`/admin/scores/users/${props.uid}/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz.id}/coverage`);
        attemptedQuestions.value = res.data.attempted
        unattemptedQuestions.value = res.data.count - res.data.attempted
    }

    fetchQuizStats();
</script>

<template>
    <div class="d-flex align-items-center">
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
            <Accuracy :correct-responses="correctResponses" :wrong-responses="wrongResponses" :color1="color1" :color2="color2"/>
            <Coverage :attempted-questions="attemptedQuestions" :unattempted-questions="unattemptedQuestions" :color1="color1" :color2="color2" />
        </div>
    </div>
</template>

<style scoped>

</style>