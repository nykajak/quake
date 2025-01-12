<script setup>
    import { api } from '@/api';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    import Pagination from './Pagination.vue';
    import { useRouter } from 'vue-router';

    import { RouterLink } from 'vue-router';
    import UserCard from './UserCard.vue';

    const route = useRoute();
    const router = useRouter();

    const users = ref([]);
    const loading = ref(false);
    const ready = ref(false);

    async function fetchUsers(){
        try{
            let page = route.query["page"] ?? 1;
            let per_page = route.query["per_page"] ?? 5 ;
            loading.value = true;
            let res = await api.get(`/admin/users/?page=${page}&per_page=${per_page}`);
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