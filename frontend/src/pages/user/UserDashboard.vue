<script setup>
import { api } from '@/api';
async function fetchUser(){
    let res = await api.get("/user/");
    console.log(res.data)
    return res.data
}
fetchUser().then()
</script>

<template>
    Testing
</template>

<style scoped>
</style>