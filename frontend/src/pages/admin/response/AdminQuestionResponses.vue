<script setup>
    import { api} from '@/api';
    import { ref } from 'vue';
    
    import StaticOption from '@/components/StaticOption.vue';
    import AdminQuestion from '../question/AdminQuestion.vue';

    const props = defineProps(['sid','cid','qid'])
    const responses = ref(null);

    async function fetchResponses(){
        let res = await api.get(`/admin/responses/?question_id=${props.qid}`);
        responses.value = res.data.payload;
    }

    fetchResponses()
</script>

<template>
    <AdminQuestion :sid="props.sid" :cid="props.cid" :qid="props.qid"/>

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