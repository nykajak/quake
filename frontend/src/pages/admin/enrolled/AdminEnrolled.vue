<script setup>
import { api } from '@/api';
import { defineProps, ref } from 'vue';
import { useRoute } from 'vue-router';

import UserCard from '../user/components/UserCard.vue';
import Loader from '@/components/Loader.vue';
import Pagination from '@/components/Pagination.vue';
import PerPage from '@/components/PerPage.vue';

const props = defineProps(['sid']);

const route = useRoute();

const users = ref(null);
const numPages = ref(null);
const errorMessage = ref(null);

async function fetchUsers(){
    let page = route.query.page ?? 1;
    let per_page = route.query.per_page ?? 5;
    try{
        let res = await api.get(`/admin/enrolled/subjects/${props.sid}?page=${page}&per_page=${per_page}`);
        users.value = res.data.payload.users;
        numPages.value = res.data.pages;
    }
    catch(err){
        if (err.response && err.response.status){
            if(err.response.status == 400){
                errorMessage.value = err.response.data.msg;
            }
            // Page not found error
            else if(err.response.status == 404){
                errorMessage.value = "Page not found!";
            }
            else{
                errorMessage.value = err.data ?? 'Unforeseen error!';
            }
        }
        else{
            errorMessage.value = 'Unforeseen error!';
            console.log(err)
        }
    }
}
fetchUsers()

</script>

<template>
    <div v-if="users" class="mt-3">
        <div class="d-flex justify-content-center gap-2 align-items-center">
            Users per page: <PerPage/>
        </div>
        <div class="d-flex flex-column align-items-center justify-content-center" v-for="user in users">
            <UserCard :user="user" :active="true"/>
            <button id="remove-button" @click="async () => {
                let res = await api.delete(`/admin/enrolled/users/${user.id}/subjects/${props.sid}`);
            }">
                Remove enrollment?
            </button>
        </div>
        <div class="d-flex mt-2 justify-content-center">
            <Pagination :url="route.path" :pages="numPages"/>
        </div>
    </div>

    <Loader v-if="users == null && errorMessage == null"/>

    <div v-if="errorMessage" class="d-flex flex-column flex-grow-1 mt-4 align-items-center ">
        <RouterLink :to="'/admin/subjects/'+props.sid">
            <h2>
                Back to Subject
            </h2>
        </RouterLink>
        <h2>
            {{ errorMessage }}
        </h2>
    </div>
</template>

<style scoped>
#remove-button{
    display: flex;
    border: none;
    background-color: var(--error-color);
    color: var(--light-color);
}
</style>