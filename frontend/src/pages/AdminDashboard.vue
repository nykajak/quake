<script setup>
import Logout from '@/components/Logout.vue';
import { api } from '@/api';
import { ref } from 'vue';


async function fetchUsers(){
    let res = await api.get("/admin/users/")
    return res.data
}

const users = ref("");
fetchUsers().then((data)=>{
    console.log(data.payload)
    users.value = data.payload;
})

</script>

<template>
    HI!!!
    <Logout/>

    <div v-for="u in users">
        {{ u.name }}
    </div>
</template>

<style scoped>
</style>