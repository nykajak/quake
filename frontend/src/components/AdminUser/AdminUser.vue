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
    <div v-if="loading == false && ready == true" class="d-flex flex-row flex-grow-1 mt-4">
        <div class="d-flex flex-column border w-25">
            <UserCard :user="user" :active="false" class="border"/>
        </div>

        <div class="d-flex flex-column align-items-center w-75 border">
            <h2>Subjects</h2>
            <div class="d-flex w-100">
                <div class="d-flex flex-row align-items-center w-100 border p-3" v-for="subject in user.subjects">
                    <div class="d-flex justify-content-center flex-grow-1">
                        <h5>{{ subject.name }}</h5>
                    </div>
                    <div class="d-flex h-100">
                        <button>v</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>
</style>