<script setup>
    import { api} from '@/api';
    import { ref } from 'vue';
    
    import StaticQuestion from '@/components/StaticQuestion.vue';
    import StaticOption from '@/components/StaticOption.vue';

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
            <StaticQuestion :description="r.question.description" />
            <!-- {{ r }} -->
        </div>
    </div>
</template>

<style scoped>

</style>