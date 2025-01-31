<script setup>
import { ref } from 'vue';
import { api } from '@/api';

import { RouterLink } from 'vue-router';

const props = defineProps(['sid','cid'])
const quizes = ref([]);

async function fetchQuizes(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes`);
    return res.data.payload.quizes;
}

fetchQuizes().then((data)=>{
    quizes.value = data;
})

</script>

<template>
    <div class="d-flex flex-column flex-grow-1">
        <div v-for="quiz in quizes" class="d-flex flex-column align-items-center mt-3">
            <h3>
                <RouterLink :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${quiz.id}`">
                    On {{ quiz.dated.day }}-{{ quiz.dated.month }}-{{ quiz.dated.year }}, at {{ quiz.dated.hour }}:{{ quiz.dated.minute }}
                </RouterLink>
            </h3>
            <p class="text-center">
                Description: {{ quiz.description }}
                <br>
                Quiz duration: {{ quiz.duration  }} minutes
            </p>
        </div>
    </div>
</template>

<style scoped>
</style>