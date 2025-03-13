<script setup>
    
    import { ref } from 'vue';
    import { api } from '@/api';

    import StaticResponse from '@/components/StaticResponse.vue';

    const props = defineProps(['sid','cid','qid'])
    const responses = ref(null);

    async function fetchResponses() {
        let res = await api.get(`/user/responses/quizes/${props.qid}`)
        responses.value = res.data.payload;
    }
    fetchResponses()
</script>

<template>
    <div v-if="responses" class="d-flex flex-column flex-grow-1 mt-3">
        <StaticResponse :response="response" v-for="response in responses" /> 
    </div>
</template>

<style scoped>
</style>