<script setup>
    import { api} from '@/api';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    
    import AdminQuestion from '../question/AdminQuestion.vue';
    import Pagination from '@/components/Pagination.vue';
    import PerPage from '@/components/PerPage.vue';

    const props = defineProps(['sid','cid','qid'])
    const route = useRoute();
    const responses = ref(null);
    const pages = ref(null);

    async function fetchResponses(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 3;
        let res = await api.get(`/admin/responses/?question_id=${props.qid}&page=${page}&per_page=${per_page}`);
        responses.value = res.data.payload;
        pages.value = res.data.pages;
    }

    fetchResponses()
</script>

<template>
    <AdminQuestion :sid="props.sid" :cid="props.cid" :qid="props.qid"/>

    <div class="d-flex w-100 justify-content-center mb-2 align-items-center gap-1">
        Number of responses per page: <PerPage/>
    </div>

    <div v-if="responses">
        <template v-for="r in responses">
            <div class="metadata">
                <div>
                    {{ r.user.name }} answered at {{ r.dated.hour }}:{{ r.dated.minute }} on {{ r.dated.day }}/{{ r.dated.month }}/{{ r.dated.year }}
                </div>
    
                <div>
                    Quiz #{{ r.quiz.id }}
                </div>
            </div>
    
            <div>
                {{ r.marked }}
            </div>
        </template>
    </div>

    <Pagination :url="route.fullPath" :pages="pages"/>
</template>

<style scoped>
.metadata{
    display: flex;
    background-color: var(--primary-color);
    justify-content: space-between;
    padding-left: 1em;
    padding-right: 1em;
}
</style>