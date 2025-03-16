<script setup>
    
    import { ref } from 'vue';
    import { api } from '@/api';

    import StaticResponse from '@/components/StaticResponse.vue';

    const props = defineProps(['sid','cid','qid'])
    const responses = ref(null);

    async function fetchData(){
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions`)
        responses.value = res.data.payload;
    }
    fetchData();
</script>

<template>
    <div v-if="responses" class="d-flex flex-column flex-grow-1 mt-3">
        <div v-for="response in responses">
            <StaticResponse :response="response"/>
        </div>
    </div>
</template>

<style scoped>
</style>