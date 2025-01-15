<script setup>
    import { defineProps, ref } from 'vue';
    import { useRouter } from 'vue-router';
    
    import { api } from '@/api';

    import UserCard from './UserCard.vue';
    import Loader from '../Utility/Loader.vue';

    const router = useRouter();
    const props = defineProps(['uid']);
    
    const user = ref(null);
    const loading = ref(false);
    const ready = ref(false);

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
    <div v-if="loading == false && ready == true" class="d-flex flex-column flex-grow-1">
        <UserCard :user="user" :active="false"/>
        <div class="d-flex flex-column align-items-center mt-3 flex-grow-1">
            <h2>Subjects</h2>
            <div class="d-flex flex-column align-items-center" v-for="subject in user.subjects">
                <h6>{{ subject.name }}</h6>
            </div>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>
</style>