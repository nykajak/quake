<script setup>
import AdminHeader from './components/AdminHeader.vue';
import AdminStats from './components/AdminStats.vue';
import AdminInfo from './components/AdminInfo.vue';
    
import { RouterView } from 'vue-router';

import { useRoute } from 'vue-router';
const route = useRoute();
</script>

<template>
    <AdminHeader/>
    <template v-if="$route.fullPath !== '/admin' && $route.fullPath !== '/admin/'">
        <RouterView :key="$route.fullPath"/>
    </template>

    <template v-else>
        <div class="d-flex flex-column flex-grow-1 align-items-center mt-3">
            <AdminStats/>
            <AdminInfo/>
        </div>
    </template>
</template>

<style scoped>
</style>