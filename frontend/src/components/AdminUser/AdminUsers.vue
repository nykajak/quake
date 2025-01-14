<script setup>
    import { ref } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    
    import { api } from '@/api';
    
    import Pagination from '../Utility/Pagination.vue';
    import UserCard from './UserCard.vue';
    import Loader from '../Utility/Loader.vue';

    const route = useRoute();
    const router = useRouter();

    const users = ref([]);
    const numPages = ref(0);
    const loading = ref(false);
    const ready = ref(false);

    async function fetchUsers(){
        try{
            let page = route.query["page"] ?? 1;
            let per_page = route.query["per_page"] ?? 5 ;
            loading.value = true;
            let res = await api.get(`/admin/users/?page=${page}&per_page=${per_page}`);
            numPages.value = res.data.pages
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
            users.value = data;
            ready.value = true;
        }
    })
</script>

<template>
    <div v-if="loading == false" class="d-flex flex-column flex-grow-1">
        <div class="d-flex flex-column flex-grow-1">
            <div class="results-div">
                <template v-for="user in users">
                    <UserCard :user="user" :active="true"/>
                </template>
            </div>
        </div>
        
        <div class="d-flex justify-content-center">
            <Pagination :interval-start="1" :interval-length="numPages" type="users"/>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>
.results-div{
    margin-top: 3em;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}
</style>