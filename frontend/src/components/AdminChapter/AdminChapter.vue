<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

import Loader from '../Utility/Loader.vue';
import ChapterCard from './ChapterCard.vue';

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
        <ChapterCard :chapter="chapter" :active="0"/>
    </div>
    <Loader v-else/>
</template>

<style scoped>
</style>