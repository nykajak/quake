<script setup>
    
    import { ref } from 'vue';
    import { api } from '@/api';
    import { useRoute } from 'vue-router';

    import StaticResponse from '@/components/StaticResponse.vue';
    import Pagination from '@/components/Pagination.vue';
    import PerPage from '@/components/PerPage.vue';

    const props = defineProps(['sid','cid','qid'])
    const route = useRoute();
    const responses = ref(null);
    const pages = ref(null);

    async function fetchData(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 5;
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions?page=${page}&per_page=${per_page}`)
        responses.value = res.data.payload;
        pages.value = res.data.pages;
    }
    fetchData();
</script>

<template>
    <div class="d-flex w-100 justify-content-center align-items-center gap-2 mt-2">
        Number of questions per page: <PerPage/>
    </div>
    <div v-if="responses" class="d-flex flex-column flex-grow-1 mt-1">
        <div v-for="response in responses">
            <StaticResponse :response="response"/>
        </div>
        <Pagination :url="route.fullPath" :pages="pages"/>
    </div>
</template>

<style scoped>
</style>