<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import UserSubjectCard from './components/UserSubjectCard.vue';

const subjects = ref([]);

async function fetchSubjects(){
    let res = await api.get("/user/subjects");
    
    console.log(res.data)
    return res.data.payload.subjects
}

fetchSubjects().then((data)=>{
    subjects.value = data;
})

</script>

<template>
    <div class="mt-3">
        <template v-for="subject in subjects">
            <UserSubjectCard :subject="subject" :active="1"/>
        </template>
    </div>
</template>

<style scoped>
</style>