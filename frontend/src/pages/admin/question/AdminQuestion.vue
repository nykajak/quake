<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { useRouter } from 'vue-router';

import StaticOption from '../../../components/StaticOption.vue';
import StaticQuestion from '../../../components/StaticQuestion.vue';

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
        <StaticQuestion :index="question.id" :description="question.description" />
        
        <div class="option-container">
            <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                <template v-for="n in 4">
                    <StaticOption :optionNo="n - 1" :correctOption="question.correct" :optionText="question.options[n - 1]"/>
                </template>
            </div>
        </div>

        <div class="d-flex justify-content-center mt-4">
            <button id="edit-button" @click="router.push(
                {
                    'path': `/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}/edit`
                }
            )">
                Edit Question
            </button>
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