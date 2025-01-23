<script setup>
import UserHeader from '@/components/Header/UserHeader.vue';
import { RouterView } from 'vue-router';
</script>

<template>
    <UserHeader/>
    <RouterView :key="$route.fullPath"/>
</template>

<style scoped>
</style>