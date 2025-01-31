<script setup>
import { api } from '@/api';
import { defineProps, ref } from 'vue';

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
    <template v-if="subject">
        <UserSubjectCard :subject="subject"/>
    </template>
</template>

<style scoped>
</style>