<script setup>
import { api } from '@/api';
import { defineProps, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import UserCard from '../user/components/UserCard.vue';
import Loader from '@/components/Loader.vue';
import PaginationToolBar from '@/components/PaginationToolBar.vue';
import SearchButton from '@/components/SearchButton.vue';

const props = defineProps(['sid']);

const route = useRoute();
const router = useRouter();

const users = ref(null);
const userName = ref(route.query.q ?? "");
const numPages = ref(null);
const errorMessage = ref(null);

async function fetchUsers(){
    let page = route.query.page ?? 1;
    let per_page = route.query.per_page ?? 5;
    try{
        let res = await api.get(`/admin/enrolled/subjects/${props.sid}?page=${page}&per_page=${per_page}&q=${userName.value}`);
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
    <div v-if="users" class="d-flex flex-column align-items-center mt-3 flex-grow-1">
        <div class="d-flex flex-column flex-grow-1 justify-content-center gap-2 align-items-center w-75">
            <h1>
                Showing all enrolled users
            </h1>
            <div class="d-flex justify-content-center align-items-start w-100">
                <input class="d-flex flex-grow-1 h-100" name="username-query" type="text" v-model="userName" placeholder="Username">
                <SearchButton :query_str="userName">
                    Search
                </SearchButton>
                
            </div>
            <div class="resultContainerDiv">
                <div class="d-flex flex-row flex-grow-1 flex-wrap justify-content-center">
                    <div class="d-flex flex-column align-items-center justify-content-center mb-2" v-for="user in users">
                        <UserCard :user="user" :active="true"/>
                        <button class="remove-button" @click="async () => {
                            let res = await api.delete(`/admin/enrolled/users/${user.id}/subjects/${props.sid}`);
                        }">
                            Remove enrollment?
                        </button>
                    </div>
                </div>
                <PaginationToolBar :num-pages="numPages"/>
            </div>
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

.resultContainerDiv{
    display: flex;
    width: 100%;
    flex-direction: column;
    flex-grow: 1;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    margin-bottom: 0.2em;
}

.remove-button{
    display: flex;
    border: none;
    background-color: var(--error-color);
    color: var(--light-color);
}

#search-button{
    display: flex;
    height: 100%;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    background-color: var(--secondary-color);
    color: var(--light-color);
}
</style>