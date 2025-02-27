<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    const requests = ref(null);

    async function rejectResponse(uid,sid){
        let res = await api.delete(`/admin/enrolled/users/${uid}/subjects/${sid}`);
    }

    async function acceptResponse(uid,sid){
        let res = await api.post(`/admin/enrolled/users/${uid}/subjects/${sid}`);
    }

    async function fetchRequests(){
        let res = await api.get("/admin/enrolled/requests")
        requests.value = res.data.payload;
    }
    fetchRequests()
</script>

<template>
    <div v-if="requests" class="d-flex flex-column flex-grow-1 mt-4 align-items-center">
        <div class="d-flex flex-column align-items-center mb-3" v-for="r in requests">
            <div>
                Username: {{ r.user.name }} 
            </div>
            <div>
                Subject: {{ r.subject.name }}
            </div>

            <div class="d-flex mt-3">
                <button class="accept-button" @click="async () => {
                    await acceptResponse(r.user.id,r.subject.id);
                }">
                    Accept
                </button>
                <button class="reject-button" @click="async () => {
                    await rejectResponse(r.user.id,r.subject.id);
                }">
                    Reject
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.accept-button{
    display: flex;
    border: none;
    background-color: var(--secondary-color);
    color: var(--light-color);
}

.reject-button{
    display: flex;
    border: none;
    background-color: var(--error-color);
    color: var(--light-color);
}
</style>