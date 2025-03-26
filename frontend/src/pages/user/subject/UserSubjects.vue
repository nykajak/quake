<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import UserSubjectCard from './components/UserSubjectCard.vue';
import Loader from '@/components/Loader.vue';
import PerPage from '@/components/PerPage.vue';
import Pagination from '@/components/Pagination.vue';

const subjects = ref([]);
const pages = ref(null);
const router = useRouter();
const route = useRoute()

async function fetchSubjects(){
    let page = route.query.page ?? 1;
    let per_page = route.query.per_page ?? 5;
    let res = await api.get(`/user/subjects/?page=${page}&per_page=${per_page}`);
    subjects.value = res.data.payload.subjects
    pages.value = res.data.pages
}

fetchSubjects()
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

        <div class="d-flex justify-content-center">
            <PerPage/>
            <div class="d-flex">
                <Pagination :url="`/user/subjects/`" :pages="pages"/>
            </div>
        </div>
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