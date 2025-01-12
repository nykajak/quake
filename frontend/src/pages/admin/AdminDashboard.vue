<script setup>
import AdminHeader from '@/components/AdminHeader.vue';
import { RouterView } from 'vue-router';
</script>

<template>
    <AdminHeader/>
    <RouterView :key="$route.fullPath"/>
</template>

<style scoped>
</style>