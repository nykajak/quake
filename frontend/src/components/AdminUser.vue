<script setup>
    import { api } from '@/api';
    import { defineProps, ref } from 'vue';
    import UserCard from './UserCard.vue';
    import { useRouter } from 'vue-router';

    const props = defineProps(['uid']);
    const user = ref(null);
    const loading = ref(false);
    const ready = ref(false);

    const router = useRouter();

    async function fetchUsers(){
        try{
            loading.value = true;
            let res = await api.get(`/admin/users/${props.uid}`);
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
            user.value = data;
            ready.value = true;
        }
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