<script setup>
    import { api} from '@/api';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    
    import AdminQuestionCard from '../question/components/AdminQuestionCard.vue';
    import StaticOption from '@/components/StaticOption.vue';
    import PaginationToolBar from '@/components/PaginationToolBar.vue';

    const props = defineProps(['sid','cid','qid'])
    const route = useRoute();
    const responses = ref(null);
    const question = ref(null);
    const pages = ref(null);

    async function fetchQuestion(){
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}`)
        question.value = res.data.payload;
    }

    async function fetchResponses(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 3;
        let res = await api.get(`/admin/responses/?question_id=${props.qid}&page=${page}&per_page=${per_page}`);
        responses.value = res.data.payload;
        pages.value = res.data.pages;
    }

    Promise.all([fetchQuestion(),fetchResponses()])
</script>

<template>
    <div class="d-flex flex-column mb-3">
        <AdminQuestionCard v-if="question" :question="question"/>   
    </div>

    <div class="d-flex flex-column flex-grow-1" v-if="responses">
        <template v-for="r in responses">
            <div class="mb-4">
                <div class="metadata">
                    <div>
                        {{ r.user.name }} answered at {{ r.dated.hour }}:{{ r.dated.minute }} on {{ r.dated.day }}/{{ r.dated.month }}/{{ r.dated.year }}
                    </div>
        
                    <div>
                        Quiz #{{ r.quiz.id }}
                    </div>
                </div>
        
                <div class="option-div d-flex justify-content-center">
                    <StaticOption :optionNo="r.marked" :correct-option="question.correct" :marked="r.marked" :option-text="question.options[r.marked]"/>
                </div>
            </div>
        </template>
    </div>

    <PaginationToolBar :num-pages="pages"/>
</template>

<style scoped>

.option-div{
    background-color: var(--secondary-color);
}

.metadata{
    display: flex;
    background-color: var(--primary-color);
    justify-content: space-between;
    padding-left: 1em;
    padding-right: 1em;
}
</style>