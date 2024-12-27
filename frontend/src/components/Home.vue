<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRoute } from 'vue-router';


async function sendReq(){
    let route = useRoute();

    try{
        let res = await api.get("/admin/users",{params : {
            "page":route.query["page"],
            "per_page":route.query["per_page"],
        }});
        console.log(res.data)
        return res.data.payload[0]["name"]
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