<script setup>
import UserHeader from './components/UserHeader.vue';
import { RouterView, } from 'vue-router';
</script>

<template>
    <UserHeader/>
    <template v-if="$route.fullPath !== '/user' && $route.fullPath !== '/user/'">
        <RouterView :key="$route.fullPath"/>
    </template>

    <template v-else>
        <div class="d-flex flex-column flex-grow-1 align-items-center mt-3">
            <h3>Welcome back :)</h3>
        </div>
    </template>
</template>

<style scoped>
</style>