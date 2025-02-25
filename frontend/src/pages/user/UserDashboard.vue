<script setup>

import { ref } from 'vue';
import { RouterView } from 'vue-router';

import UserHeader from './components/UserHeader.vue';
import Loader from '@/components/Loader.vue';

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
                <h3>Welcome back {{ user.name }}!</h3>
            </div>
        </template>
    </template>

    <Loader v-else/>
</template>

<style scoped>
</style>