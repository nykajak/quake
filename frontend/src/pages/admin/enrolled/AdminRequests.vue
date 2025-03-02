<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import Loader from '@/components/Loader.vue';

    const requests = ref(null);
    const errorMessage = ref(null);

    async function rejectResponse(uid,sid){
        let res = await api.delete(`/admin/enrolled/users/${uid}/subjects/${sid}`);
    }

    async function acceptResponse(uid,sid){
        let res = await api.post(`/admin/enrolled/users/${uid}/subjects/${sid}`);
    }

    async function fetchRequests(){
        try{
            let res = await api.get("/admin/enrolled/requests")
            if (res.data.payload.length > 0){
                requests.value = res.data.payload;
            }
            else{
                errorMessage.value = "No pending requests!"
            }
        }
        catch(err){
            if (err.response && err.response.status){
                if(err.response.status == 400){
                    errorMessage.value = err.response.data.msg;
                }
                // Page not found error
                else if(err.response.status == 404){
                    errorMessage.value = "Page not found!";
                }
                else{
                    errorMessage.value = err.data ?? 'Unforeseen error!';
                }
            }
            else{
                errorMessage.value = 'Unforeseen error!';
                console.log(err)
            }
        }
    }
    fetchRequests()
</script>

<template>
    <div v-if="requests" class="d-flex flex-column flex-grow-1 mt-4 align-items-center">

        <div v-if="requests.length == 0">
            <h3>
                No requests pending!
            </h3>
        </div>

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

    <Loader v-if="requests == null && errorMessage == null"/>

    <div v-if="errorMessage" class="d-flex flex-column flex-grow-1 mt-4 align-items-center ">
        <RouterLink :to="'/admin'">
            <h2>
                Back to dashboard
            </h2>
        </RouterLink>
        <h2>
            {{ errorMessage }}
        </h2>
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