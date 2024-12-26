<script setup>
import { api } from '@/api';
import { ref } from 'vue';

async function sendReq(){
    try{
        let res = await api.get("/");
        console.log(res.data)
        return res.data.msg
    }
    catch(err){
        console.log(err)
        return "Something went wrong!"
    }
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
    <h3>{{message}}</h3>
    <button @click="sendLogout">Logout</button>
</template>

<style scoped>
</style>