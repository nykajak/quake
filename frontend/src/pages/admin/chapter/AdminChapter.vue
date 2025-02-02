<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

import Loader from '@/components/Loader.vue';
import ChapterCard from './components/ChapterCard.vue';
import { RouterLink } from 'vue-router';

const router = useRouter();
const props = defineProps(['sid','cid']);
const loading = ref(false);
const ready = ref(false);
const chapter = ref(null);

async function fetchChapter(){
    try{
        loading.value = true;
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}`)
        loading.value = false;
        return res.data.payload
    }
    catch(err){
        console.log(err);
        loading.value = false;
        router.push({"name":"NotFound"})
        return -1
    }
}

fetchChapter().then(data => {
    if (data != -1){
        chapter.value = data;
        ready.value = true;
    }
})

</script>

<template>
    <div v-if="loading == false && ready == true" class="d-flex flex-column flex-grow-1 mt-2">
        <div class="d-flex flex-row justify-content-center">
            <RouterLink :to="'/admin/subjects/'+chapter.subject.id">
                <h2>{{ chapter.subject.name }}</h2>
            </RouterLink>
        </div>
        <ChapterCard :chapter="chapter" :active="0"/>

        <div class="d-flex flex-row justify-content-center">
            <button class="option-button" id="edit-button" @click="router.push({
                path:`/admin/subjects/${props.sid}/chapters/${props.cid}/edit`
            })">
                Edit chapter
            </button>
        </div>
    </div>
    <Loader v-else/>
</template>

<style scoped>
.option-button{
    display: flex;
    border: none;
    padding: 0.5em;
    color: var(--light-color);
}

#edit-button{
    background-color: var(--error-color);
}
</style>