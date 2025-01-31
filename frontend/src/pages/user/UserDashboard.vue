<script setup>
import UserHeader from './components/UserHeader.vue';
import { RouterView } from 'vue-router';
</script>

<template>
    <UserHeader/>
    <RouterView :key="$route.fullPath"/>
</template>

<style scoped>
</style>