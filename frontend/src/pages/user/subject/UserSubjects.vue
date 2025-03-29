<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import UserSubjectCard from './components/UserSubjectCard.vue';
import Loader from '@/components/Loader.vue';
import PaginationToolBar from '@/components/PaginationToolBar.vue';
import SearchButton from '@/components/SearchButton.vue';

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
    <div v-if="subjects" class="d-flex flex-column align-items-center mt-3">
        <h1>
            Search for enrolled subject
        </h1>
        <div class="d-flex justify-content-center mb-3 w-75">
            <input class="d-flex flex-grow-1" type="text" v-model="query_string" placeholder="Subject">
            <SearchButton :query_str="query_string">
                Search Subject
            </SearchButton>
        </div>

        <template v-for="subject in subjects">
            <UserSubjectCard :subject="subject" :active="1"/>
        </template>

        <PaginationToolBar :num-pages="pages"/>
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