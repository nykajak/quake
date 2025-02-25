<script setup>
import { api } from '@/api';
import { defineProps, ref } from 'vue';

import { RouterLink, useRouter } from 'vue-router';
import UserSubjectCard from './components/UserSubjectCard.vue';
import Loader from '@/components/Loader.vue';

const props = defineProps(['sid']);
const router = useRouter();
const subject = ref(null);

async function fetchSubject(){
    try{
        let res = await api.get(`/user/subjects/${props.sid}`);
        subject.value = res.data.payload;
    }
    catch(err){
        console.log(err);
        router.push({
            "path": `/user/subjects`
        })
    }
}

fetchSubject()

</script>

<template>
    <div v-if="subject" class="mt-3">
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
    <Loader v-else/>
</template>

<style scoped>
</style>