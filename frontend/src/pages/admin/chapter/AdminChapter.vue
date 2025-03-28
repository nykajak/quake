<script setup>
import { ref, defineProps } from 'vue';
import { RouterLink } from 'vue-router';

import { api } from '@/api';

import ChapterCard from './components/ChapterCard.vue';

import Loader from '@/components/Loader.vue';
import NavButton from '@/components/NavButton.vue';
import DeleteButton from '@/components/DeleteButton.vue';

const props = defineProps(['sid','cid']);

const chapter = ref(null);
const errorMessage = ref(null);

async function fetchChapter(){
    try{
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}`)
        chapter.value = res.data.payload
    }
    catch(err){
        if (err.response && err.response.status){
            // Chapter not found error
            if(err.response.status == 404){
                errorMessage.value = 'No such chapter!';
            }
            else{
                errorMessage.value = 'Unforeseen error!';
                console.log(err.response);
            }
        }
        else{
            errorMessage.value = 'Unforeseen error!';
            console.log(err)
        }
    }
}

fetchChapter()

</script>

<template>
    <div v-if="chapter" class="d-flex flex-column flex-grow-1 mt-2">
        <div class="d-flex flex-row justify-content-center">
            <RouterLink :to="'/admin/subjects/'+chapter.subject.id">
                <h2>{{ chapter.subject.name }}</h2>
            </RouterLink>
        </div>
        <ChapterCard :chapter="chapter" :active="0"/>

        <div class="d-flex flex-row justify-content-center">
            <NavButton text="Manage questions" :url="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions`" color="primary"/>
            <NavButton text="Manage quizes" :url="`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes`" color="secondary"/>
            <NavButton text="Edit chapter" :url="`/admin/subjects/${props.sid}/chapters/${props.cid}/edit`" color="tertiary"/>
            <DeleteButton :redirect="`/admin/subjects/${props.sid}`" :url="`/admin/subjects/${props.sid}/chapters/${props.cid}`" color="error">
                Delete chapter
            </DeleteButton>
        </div>
    </div>

    <Loader v-if="chapter == null && errorMessage == null"/>

    <div v-if="errorMessage" class="d-flex flex-column flex-grow-1 mt-4 align-items-center ">
        <RouterLink :to="'/admin/subjects/'+props.sid">
            <h2>
                Back to Subject
            </h2>
        </RouterLink>
        <h2>
            {{ errorMessage }}
        </h2>
    </div>
</template>

<style scoped>

</style>