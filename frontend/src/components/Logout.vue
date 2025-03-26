<!-- Renders a button which logouts the current user! -->
<script setup>
import { useRouter } from 'vue-router';
import { api } from '@/api';

const router = useRouter()
async function sendLogout(){
    await api.post("/logout");
    router.push({"name":"login"})
}

</script>

<template>
    <div class="d-flex align-items-center">
        <button class="logout-button" @click="sendLogout">Sign out</button>
    </div>
</template>

<style scoped>
.logout-button {
    height: fit-content;
    border-radius: 0.5em;
    border: 1px solid light-dark(var(--dark-color), var(--light-color));
    background-color:var(--secondary-color);
    color: var(--light-color);
}
</style>