<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';
    import Message from '@/components/Message.vue';

    const available = ref(false);
    const info_message = ref("");

    async function checkReport(){
        try{
            let res = await api.get("/user/summary/check");
            available.value = true;
        }
        catch(err){
            console.log(err);
        }
    }

    async function requestReport(){
        try{
            let res = await api.get("/user/summary/generate");
            available.value = false;
            info_message.value = "Request successfully sent! Come back after a while to view the results."
        }
        catch(err){
            console.log(err);
        }
    }
    checkReport()
</script>

<template>
    <Message v-if="info_message" :text="info_message" level="info" :hide-function="() => {info_message=''}">
        {{info_message}}
    </Message>
    <div class="d-flex flex-column flex-grow-1">
        <div class="d-flex flex-column align-items-center mt-3" v-if="available">
            <h3>
                Enjoy your report!
            </h3>
            <a href="http://localhost:5000/user/summary/">Download report!</a>
            <button @click="requestReport">
                Generate report!
            </button>
        </div>

        <div class="d-flex flex-column align-items-center mt-3" v-else>
            <h3>
                No report available!
            </h3>
            <button @click="requestReport">
                Generate report!
            </button>
        </div>
    </div>
</template>

<style scoped>
</style>