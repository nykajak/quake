<script setup>
    import { api } from '@/api';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    import Pagination from './Pagination.vue';

    import { RouterLink } from 'vue-router';
    import UserCard from './UserCard.vue';

    const route = useRoute();
    const users = ref([]);
    const loading = ref(false);

    async function fetchUsers(){
        let page = route.query["page"] ?? 1;
        let per_page = route.query["per_page"] ?? 5 ;
        loading.value = true;
        let res = await api.get(`/admin/users/?page=${page}&per_page=${per_page}`);
        loading.value = false;
        return res.data.payload
    }

    fetchUsers().then(data => {
        console.log(data);
        users.value = data;
    })
</script>

<template>
    <div v-if="loading == false">
        <div class="results-div">
            <template v-for="user in users">
                <UserCard :user="user" :active="true"/>
            </template>
        </div>
    
        <Pagination :interval-start="1" :interval-length="2"/>
    </div>

    <div v-else>
        Loading......
    </div>
</template>

<style scoped>
.results-div{
    margin-top: 3em;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}
</style>