<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';
    import { useRoute } from 'vue-router';

    import AdminQuizScoreWidget from './AdminQuizScoreWidget.vue';
    import StaticResponse from '@/components/StaticResponse.vue';
    import Pagination from '@/components/Pagination.vue';
    import PerPage from '@/components/PerPage.vue';

    const props = defineProps(['uid','sid','cid','qid']);
    const route = useRoute();
    const responses = ref(null);
    const pages = ref(null);

    async function fetchResponses(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 5;
        let res = await api.get(`/admin/responses/?quiz_id=${props.qid}&user_id=${props.uid}&page=${page}&per_page=${per_page}`)
        responses.value = res.data.payload;
        pages.value = res.data.pages;
    }
    fetchResponses()
</script>

<template>
    <div class="d-flex gap-2 justify-content-center w-100 mt-2 align-items-center">
        Number of responses per page: <PerPage/>
    </div>
    <div v-if="responses">
        <div v-for="response in responses">
            <StaticResponse :response="response"/>
        </div>
    </div>
    <Pagination :url="route.fullPath" :pages="pages"/>

</template>

<style scoped>
</style>