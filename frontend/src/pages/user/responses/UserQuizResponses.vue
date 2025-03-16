<script setup>
    
    import { ref } from 'vue';
    import { api } from '@/api';

    import StaticResponse from '@/components/StaticResponse.vue';
    import StaticQuestion from '@/components/StaticQuestion.vue';
    import StaticOptions from '@/components/StaticOptions.vue';

    const props = defineProps(['sid','cid','qid'])
    const responses = ref(null);
    const questions = ref(null);

    async function fetchQuestions(){
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions`)
        questions.value = res.data.payload;
    }

    async function fetchResponses() {
        let res = await api.get(`/user/responses/quizes/${props.qid}`)
        responses.value = res.data.payload;
    }
    fetchResponses();
    fetchQuestions();
</script>

<template>
    <div v-if="responses" class="d-flex flex-column flex-grow-1 mt-3">
        <div v-for="question in questions" class="d-flex flex-column">
            <StaticQuestion :description="question.description"/>
        </div>
        <StaticResponse :response="response" v-for="response in responses" /> 
    </div>
</template>

<style scoped>
</style>