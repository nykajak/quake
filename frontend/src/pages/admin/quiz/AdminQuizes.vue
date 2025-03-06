<script setup>
import { ref, watch } from 'vue';
import { api } from '@/api';

import { RouterLink, useRouter, useRoute } from 'vue-router';

const router = useRouter()
const route = useRoute()
const props = defineProps(['sid','cid'])
const quizes = ref([]);
const filter_ = ref("pending");

let filter = route.query.filter ?? "pending";
async function fetchResults(e){
    const f = new FormData(e.target);
    router.push({
        "path": route.path,
        "query": {
            "filter": filter_.value
        }
    })
}

async function initialFetch(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/?filter=${filter_.value}`);
    quizes.value = res.data.payload;
}

watch(filter_, (newValue, oldValue) => {
    initialFetch();
})
initialFetch()

</script>

<template>
    <div class="d-flex flex-column flex-grow-1 mt-2 align-items-center">
        <form @submit.prevent="fetchResults" class="d-flex flex-column w-100 align-items-center mt-1">
            <div class="form-options-div-container">
                <div class="form-options-div">
                    <label for="past">Search past quizes</label>
                    <input type="radio" name="filter" id="past" value="past" v-model="filter_">
                    <label for="pending">Search pending quizes</label>
                    <input type="radio" name="filter" id="pending" value="pending" v-model="filter_">
                </div>
            </div>
        </form>

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