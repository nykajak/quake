<script setup>

import { ref } from 'vue';
import { RouterView } from 'vue-router';

import UserHeader from './components/UserHeader.vue';
import Loader from '@/components/Loader.vue';
import UserCard from '../admin/user/components/UserCard.vue';
import NavButton from '@/components/NavButton.vue';

import { api } from '@/api';

const user = ref(null);

async function fetchUser(){
    try{
        let res = await api.get("/user/");
        user.value = res.data.payload;
    }
    catch(err){
        console.log(err);
    }
}

fetchUser();

</script>

<template>
    <UserHeader/>

    <template v-if="user">
        <template v-if="$route.fullPath !== '/user' && $route.fullPath !== '/user/'">
            <RouterView :key="$route.fullPath"/>
        </template>
    
        <template v-else>
            <div class="d-flex flex-column flex-grow-1 align-items-center mt-3">
                <UserCard :user="user"/>
                <h3>Welcome back!</h3>
                <br>
                <div class="d-flex">
                    <NavButton url="/user/subjects" text="Get Started!" color="primary"/>
                    <NavButton url="/user/summary" text="Summary page" color="secondary"/>
                </div>
            </div>
        </template>
    </template>

    <Loader v-else/>
</template>

<style scoped>
</style>