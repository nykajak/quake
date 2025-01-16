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
    const username = ref(route.query.q ?? '');

    async function fetchUsers(){
        try{
            let page = route.query["page"] ?? 1;
            let per_page = route.query["per_page"] ?? 5 ;
            let q = route.query["q"] ?? "";
            loading.value = true;
            let res = await api.get(`/admin/users/?page=${page}&per_page=${per_page}&q=${q}`);
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
        <div class="d-flex flex-row h-100">
            <div class="d-flex flex-column user-sidebar w-25 justify-content-center align-items-center">
                <h3>Querying users</h3>
                <div class="mb-2">
                    <input type="text" v-model="username" placeholder="Username">
                    <button class="query-button" @click="router.push({
                        'path': 'users',
                        'query': {
                            ...route.query,
                            'q': username,
                            'page': 1
                        }
                    })">Submit</button>
                </div>
            </div>
            <div class="d-flex flex-column w-75">
                <div class="d-flex flex-column flex-grow-1 justify-content-center">
                    <div class="results-div">
                        <template v-for="user in users">
                            <UserCard :user="user" :active="true"/>
                        </template>
                    </div>
                </div>
                
                <div class="d-flex justify-content-center">
                    <Pagination :pages="numPages" type="users"/>
                </div>
            </div>
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
    justify-content: center;
}
.user-sidebar{
    border-right: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.query-button{
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    background-color: var(--secondary-color);
    color: var(--light-color);
}

input {
    padding-left: 0.5em;
}
</style>