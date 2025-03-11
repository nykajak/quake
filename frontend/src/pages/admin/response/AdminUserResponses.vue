<script setup>
    import { api} from '@/api';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    
    import StaticResponse from '@/components/StaticResponse.vue';

    const props = defineProps(['uid'])
    const route = useRoute();
    const responses = ref(null);

    async function fetchResponses(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 3;
        let res = await api.get(`/admin/responses/?user_id=${props.uid}&page=${page}&per_page=${per_page}`);
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