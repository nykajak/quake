<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRouter,useRoute } from 'vue-router';
import Header from './Header.vue';

const router = useRouter()
const route = useRoute()
async function sendReq(){

    try{
        let res = await api.get("/admin/users/Nykaj");
        console.log(res.data)
        return res.data.payload
    }
    catch(err){
        console.log(err)
        return "Something went wrong!"
    }
}

async function sendLogout(){
    let res = await api.post("/logout");
    router.push({"name":"login"})
}

const message = ref("")
sendReq().then(data => {
    message.value = data;
})

</script>

<template>
    <Header></Header>
    <h3>{{message}}</h3>
    <button @click="sendLogout">Logout</button>
</template>

<style scoped>
</style>