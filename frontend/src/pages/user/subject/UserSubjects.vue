<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import UserSubjectCard from './components/UserSubjectCard.vue';
import Loader from '@/components/Loader.vue';
import PerPage from '@/components/PerPage.vue';
import Pagination from '@/components/Pagination.vue';

const subjects = ref(null);
const pages = ref(null);
const router = useRouter();
const route = useRoute()

const query_string = ref(route.query.q ?? "")

async function search(){
    router.push({
        "path": route.fullPath,
        "query": {
            ...route.query,
            "page": 1,
            "q": query_string.value,
        }
    })
}

async function fetchSubjects(){
    let page = route.query.page ?? 1;
    let per_page = route.query.per_page ?? 5;
    let q = route.query.q ?? "";
    let res = await api.get(`/user/subjects/?page=${page}&per_page=${per_page}&q=${q}`);
    subjects.value = res.data.payload.subjects
    pages.value = res.data.pages
}

fetchSubjects()
</script>

<template>
    <div v-if="subjects" class="mt-3">
        <div class="d-flex justify-content-center mb-3">
            <div class="d-flex justify-content-center align-items-center gap-1">
                Search enrolled: <input type="text" v-model="query_string">
            </div>
            <button id="search" @click="search">
                Search
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
#search{
    background-color: var(--primary-color);
    border: none;
    color: var(--light-color);
}
</style>