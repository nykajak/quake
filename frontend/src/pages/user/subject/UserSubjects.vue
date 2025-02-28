<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import UserSubjectCard from './components/UserSubjectCard.vue';
import Loader from '@/components/Loader.vue';

const subjects = ref([]);
const router = useRouter();

async function fetchSubjects(){
    let res = await api.get("/user/subjects/");
    return res.data.payload.subjects
}

fetchSubjects().then((data)=>{
    subjects.value = data;
})

</script>

<template>
    <div v-if="subjects" class="mt-3">
        <div class="d-flex justify-content-center mb-4">
            <button id="enroll" @click = "() =>{
                router.push({
                    'path': `/user/subjects/enroll`
                })
            }">
                Enroll to course!
            </button>
        </div>

        <template v-for="subject in subjects">
            <UserSubjectCard :subject="subject" :active="1"/>
        </template>

    </div>
    <Loader v-else/>
</template>

<style scoped>
#enroll{
    background-color: var(--secondary-color);
    border: none;
    border-radius: 5px;
    color: var(--light-color);
}
</style>