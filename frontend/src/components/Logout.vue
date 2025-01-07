<script setup>
import { useRouter,useRoute } from 'vue-router';
import { api } from '@/api';
const router = useRouter()
async function sendReq(){
    
    try{
        let res = await api.get("/");
        return res.data.msg
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
    <div>
        <h3>{{message}}</h3>
        <button @click="sendLogout">Logout</button>
    </div>
</template>

<style scoped>
</style>