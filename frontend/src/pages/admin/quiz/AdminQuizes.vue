<script setup>
import { ref, watch } from 'vue';
import { api } from '@/api';

import { RouterLink, useRouter, useRoute } from 'vue-router';

import NavButton from '@/components/NavButton.vue';
import Loader from '@/components/Loader.vue';
import PaginationToolBar from '@/components/PaginationToolBar.vue';
import ObjectNotFound from '@/components/ObjectNotFound.vue';

const router = useRouter()
const route = useRoute()
const props = defineProps(['sid','cid'])
const quizes = ref(null);
const pages = ref(null);

const selected = ref(route.query.filter ?? "pending");

async function navigateFilter(){
    router.push({
        "path": route.path,
        "query": {
            ...route.query,
            "filter": selected.value,
            "page": 1
        }
    })
}

async function initialFetch(){
    let page = route.query.page ?? 1;
    let per_page = route.query.per_page ?? 5;
    let filter = route.query.filter ?? "pending";
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/?filter=${filter}&page=${page}&per_page=${per_page}`);
    quizes.value = res.data.payload;
    pages.value = res.data.pages;
}

initialFetch()

watch(selected, (newVal,oldVal)=>{
    navigateFilter();
})

</script>

<template>
    <div v-if="quizes" class="d-flex flex-column flex-grow-1 mt-2 align-items-center">
        <form @submit.prevent="" class="d-flex flex-column w-100 align-items-center mt-1">
            <div class="d-flex mb-2">
                <NavButton text="+ Add Quiz" url="quizes/add" color="primary"/>
            </div>
            
            <div class="form-options-div-container">
                <div class="form-options-div">
                    <label for="past">Search past quizes</label>
                    <input type="radio" name="filter" id="past" value="past" v-model="selected">
                    <label for="pending">Search pending quizes</label>
                    <input type="radio" name="filter" id="pending" value="pending" v-model="selected">
                </div>
            </div>
        </form>
        <template v-if="quizes.length > 0">
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
            <PaginationToolBar :num-pages="pages"/>
        </template>
        <ObjectNotFound v-else>
            No results found
        </ObjectNotFound>

    </div>
    <Loader v-else/>
</template>

<style scoped>
#search-button{
    background-color: var(--secondary-color);
    color: var(--light-color);
    border: none;
}

.form-options-div-container{
    display: flex;
    align-items: center;
}

.form-options-div{
    display: flex;
    flex-direction: row;
    gap:1em;    
    padding: 0.5em;
    margin-left:1em;
    margin-right:1em;
}
</style>