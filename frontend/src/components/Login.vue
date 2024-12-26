<script setup>
import { api } from '@/api';
import { useRouter } from 'vue-router'

const router = useRouter()
async function validateForm(e){
    try{
        let res = await api.post("/login",new FormData(e.target));
        console.log(res.data.msg);
    }
    catch(err){
        console.log(err);
    }
}

</script>

<template>
    <form @submit.prevent="validateForm">
        <div>
            <label for="username">Username: </label>
            <input type="text" name="username">
        </div>

        <div>
            <label for="password">Password: </label>
            <input type="password" name="password">
        </div>

        <button type="submit" class="btn btn-primary">Login</button>
    </form>
</template>

<style scoped>
</style>