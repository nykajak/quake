<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import UserSubjectCard from './UserSubjectCard.vue';

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
    <template v-for="subject in subjects">
        <UserSubjectCard :subject="subject" :active="1"/>
    </template>
</template>

<style scoped>
</style>