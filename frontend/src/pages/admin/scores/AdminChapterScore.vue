<script setup>
    import { ref } from 'vue';
    import { useRouter, useRoute } from 'vue-router';    
    import { api } from '@/api';

    import AdminChapterScoreWidget from './AdminChapterScoreWidget.vue';
    import AdminQuizScoreWidget from './AdminQuizScoreWidget.vue';
    import Pagination from '@/components/Pagination.vue';
    import PerPage from '@/components/PerPage.vue';

    const props = defineProps(['uid','sid','cid']);
    const route = useRoute();
    const router = useRouter();

    const quizes = ref(null);
    const pages = ref(null);

    async function fetchQuizes(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 5;
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/?page=${page}&per_page=${per_page}&filter=past`)
        quizes.value = res.data.payload;
        pages.value = res.data.pages;
    }
    fetchQuizes()
</script>

<template>
    <AdminChapterScoreWidget :uid="props.uid" :sid="props.sid" :cid="props.cid" />
    
    <div class="d-flex w-100 justify-content-center gap-2 align-items-center mb-3">
        Quizes per page: <PerPage/>
    </div>
    <div class="d-flex flex-column gap-4">
        <div v-for="quiz in quizes">
            <AdminQuizScoreWidget :quiz="quiz" :uid="props.uid" :sid="props.sid" :cid="props.cid"/>
        </div>
    </div>

    <Pagination :url="route.fullPath" :pages="pages"/>
</template>

<style scoped>
</style>