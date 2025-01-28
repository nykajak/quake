<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import { RouterLink } from 'vue-router';

const questions = ref([]);
const props = defineProps(['sid','cid'])

async function fetchQuestion(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions`)
    return res.data.payload.questions;
}

fetchQuestion().then((data)=>{
    questions.value = data;
})
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 border pt-4">
        <div class="d-flex flex-column align-items-center gap-4">
            <div v-for="question in questions">
                <RouterLink :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                    {{ question.description }}
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>