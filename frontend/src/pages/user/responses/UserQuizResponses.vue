<script setup>
    
    import { ref } from 'vue';
    import { api } from '@/api';

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
        <div class="d-flex flex-column align-items-center gap-2">
            <div v-for="response in responses"> 
                {{  response.marked }} - {{  response.question.description }}
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>