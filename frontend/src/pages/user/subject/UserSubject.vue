<script setup>
import { api } from '@/api';
import { defineProps, ref } from 'vue';

import { RouterLink } from 'vue-router';
import UserSubjectCard from './components/UserSubjectCard.vue';

const props = defineProps(['sid']);
const subject = ref(null);

async function fetchSubject(){
    let res = await api.get(`/user/subjects/${props.sid}`);
    return res.data.payload
}

fetchSubject().then((data)=>{
    subject.value = data;
})

</script>

<template>
    <div class="mt-3">
        <template v-if="subject">
            <UserSubjectCard :subject="subject"/>
        </template>

        <div class="d-flex flex-column align-items-center" v-for="chapter in subject.chapters">
            <h3>
                <RouterLink :to="`/user/subjects/${props.sid}/chapters/${chapter.id}`">
                    {{ chapter.name }}
                </RouterLink>
            </h3>
            <p>
                {{ chapter.description ? chapter.description : "No description yet!" }}
            </p>
        </div>
    </div>
</template>

<style scoped>
</style>