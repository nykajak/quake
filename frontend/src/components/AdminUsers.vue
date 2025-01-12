<script setup>
    import { api } from '@/api';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';
    import Pagination from './Pagination.vue';

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
            <div class="user-card-div" v-for="u in users">
                <div class="profile-div">
    
                </div>
    
                <div class="info-div">
                    <h3>{{ u.name }}</h3>
                    <div class="email-div">{{u.email}}</div>
                </div>
            </div>
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

.user-card-div{
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-grow: 1;
    /* border: 1px solid light-dark(var(--dark-color),var(--light-color));
    border-radius: 0.5em;    */
    margin: 1em;    
    padding: 1em;
}

.profile-div{
    display: flex;
    width: 100px;
    height: 100px;
    border-radius: 100%;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    margin-bottom: 1em;
}

.info-div{
    display: flex;
    flex-direction: column;
    text-align: center;
    color: var(--secondary-color);
}

.email-div{
    color: var(--contrast-color);
}
</style>