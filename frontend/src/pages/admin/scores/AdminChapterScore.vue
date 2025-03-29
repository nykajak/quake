<script setup>
    import { ref } from 'vue';
    import { useRouter, useRoute } from 'vue-router';    
    import { api } from '@/api';

    import AdminChapterScoreWidget from './AdminChapterScoreWidget.vue';
    import AdminQuizScoreWidget from './AdminQuizScoreWidget.vue';
    import PaginationToolBar from '@/components/PaginationToolBar.vue';

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
    <template v-if="quizes">
        <AdminChapterScoreWidget :uid="props.uid" :sid="props.sid" :cid="props.cid" />
        
        <div class="d-flex justify-content-center mt-4">
            <h1>
                Displaying quiz scores!
            </h1>
        </div>

        <div class="d-flex w-100 justify-content-center">
            <div class="d-flex flex-column align-items-center gap-4 w-75">
                <AdminQuizScoreWidget v-for="quiz in quizes" :quiz="quiz" :uid="props.uid" :sid="props.sid" :cid="props.cid"/>
            </div>
        </div>
    
        <PaginationToolBar :num-pages="pages"/>
    </template>
</template>

<style scoped>
</style>