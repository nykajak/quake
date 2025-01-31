<script setup>
import { api } from '@/api';
import { defineProps, ref } from 'vue';
import { useRouter } from 'vue-router';

import UserCard from '../user/components/UserCard.vue';
import Loader from '@/components/Loader.vue';

const props = defineProps(['sid']);

const router = useRouter();
const loading = ref(false);
const ready = ref(false);
const users = ref([]);

async function fetchUsers(){
    try{
        loading.value = true;
        let res = await api.get(`/admin/subjects/${props.sid}/enrolled`);
        loading.value = false;
        return res.data.payload
    }
    catch(err){
        loading.value = false;
        router.push({"name":"NotFound"})
        return -1
    }
}

fetchUsers().then(data => {
    if (data != -1){
        users.value = data.users;
        ready.value = true;
    }
})


</script>

<template>
    <div v-if="loading == 0 && ready == 1">
        <template v-for="user in users">
            <UserCard :user="user" :active="true"/>
        </template>
    </div>

    <Loader v-else/>
</template>

<style scoped>
</style>