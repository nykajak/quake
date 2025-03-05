<script setup>
    import { api} from '@/api';
    import { ref } from 'vue';
    
    import StaticResponse from '@/components/StaticResponse.vue';

    const props = defineProps(['sid','cid','qid'])
    const responses = ref(null);

    async function fetchResponses(){
        let res = await api.get(`/admin/responses/?quiz_id=${props.qid}`);
        responses.value = res.data.payload;
    }

    fetchResponses()
</script>

<template>
    <div v-if="responses">
        <div v-for="r in responses">
            <StaticResponse :response="r"/>
        </div>
    </div>
</template>

<style scoped>

</style>