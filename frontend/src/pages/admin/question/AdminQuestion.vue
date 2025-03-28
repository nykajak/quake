<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { useRouter } from 'vue-router';

import StaticOptions from '../../../components/StaticOptions.vue';
import StaticQuestion from '../../../components/StaticQuestion.vue';
import NavButton from '@/components/NavButton.vue';
import DeleteButton from '@/components/DeleteButton.vue';
import AdminQuestionCard from './components/AdminQuestionCard.vue';

const router = useRouter();

const question = ref(null);
const props = defineProps(['sid','cid','qid'])

async function fetchQuestion(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}`)
    return res.data.payload;
}

fetchQuestion().then((data)=>{
    question.value = data;
})
</script>

<template>
    <div v-if="question" class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <AdminQuestionCard :question="question"/>
        <div class="d-flex justify-content-center mt-4">
            <NavButton :url="`${props.qid}/responses`" text="See Responses" color="primary"/>
            <NavButton :url="`${props.qid}/edit`" text="Edit Question" color="secondary"/>
            <DeleteButton :redirect="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/`" :url="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}`" color="error">
                Delete question
            </DeleteButton>
        </div>
    </div>

</template>

<style scoped>

#edit-button{
    border: 1px solid var(--light-color);
    color: var(--light-color);
    background-color: var(--tertiary-color);
    padding: 0.5em;
    border-radius: 10px;
}

.option-container{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    margin-top: 2em;
}


</style>