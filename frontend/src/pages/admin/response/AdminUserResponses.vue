<script setup>
    import { api} from '@/api';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    
    import StaticResponse from '@/components/StaticResponse.vue';
    import Pagination from '@/components/Pagination.vue';
    import PerPage from '@/components/PerPage.vue';

    const props = defineProps(['uid'])
    const route = useRoute();
    const responses = ref(null);
    const pages = ref(null);

    async function fetchResponses(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 3;
        let res = await api.get(`/admin/responses/?user_id=${props.uid}&page=${page}&per_page=${per_page}`);
        responses.value = res.data.payload;
        pages.value = res.data.pages;
    }

    fetchResponses()
</script>

<template>
    <div class="d-flex w-100 justify-content-center mt-3 align-items-center gap-1">
        Number of responses per page: <PerPage/>
    </div>
    <div v-if="responses">
        <div v-for="r in responses">
            <StaticResponse :response="r"/>
        </div>
    </div>

    <Pagination :url="route.fullPath" :pages="pages"/>
</template>

<style scoped>

</style>