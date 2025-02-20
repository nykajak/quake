<script setup>
import { api } from '@/api';
import { ref } from 'vue';

import UserSubjectCard from './components/UserSubjectCard.vue';
import Loader from '@/components/Loader.vue';

const subjects = ref([]);

async function fetchSubjects(){
    let res = await api.get("/user/subjects");
    return res.data.payload.subjects
}

fetchSubjects().then((data)=>{
    subjects.value = data;
})

</script>

<template>
    <div v-if="subjects" class="mt-3">
        <template v-for="subject in subjects">
            <UserSubjectCard :subject="subject" :active="1"/>
        </template>
    </div>
    <Loader v-else/>
</template>

<style scoped>
</style>