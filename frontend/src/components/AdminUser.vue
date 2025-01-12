<script setup>
    import { api } from '@/api';
    import { defineProps, ref } from 'vue';
    import UserCard from './UserCard.vue';

    const props = defineProps(['uid']);
    const user = ref(null);
    const loading = ref(false);
    const ready = ref(false);

    async function fetchUsers(){
        loading.value = true;
        let res = await api.get(`/admin/users/${props.uid}`);
        loading.value = false;
        return res.data.payload
    }
    
    fetchUsers().then(data => {
        user.value = data;
        ready.value = true;
    })
</script>

<template>
    <div v-if="loading == false && ready == true">
        <UserCard :user="user" :active="false"/>
    </div>

    <div v-else>
        Loading......
    </div>
</template>

<style scoped>
</style>