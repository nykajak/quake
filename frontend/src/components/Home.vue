<script setup>
import { api } from '@/api';
import { ref } from 'vue';

async function sendReq(){
    let res = await api.get("/all");
    console.log(res)
    return res.data.payload[0]
}

async function sendLogout(){
    let res = await api.post("/logout");
}

const message = ref("")
sendReq().then(data => {
    message.value = data;
})

</script>

<template>
    <h3>Home {{message}} !</h3>
    <button @click="sendLogout">Logout</button>
</template>

<style scoped>
</style>