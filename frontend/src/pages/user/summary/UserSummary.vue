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
            <h1>
                Enjoy your report!
            </h1>
        </div>

        <div class="d-flex flex-column align-items-center mt-3" v-else>
            <h1>
                No report available!
            </h1>
        </div>

        <div class="d-flex justify-content-center m-2">
            <a v-if="available" id="fetch-button" :href="api.defaults.baseURL + 'user/summary/'" @click="(e)=>{
                if (!available){
                    e.preventDefault();
                }
            }">
                Download report!
            </a>
            <button id="generate-button" @click="requestReport">
                Generate new report!
            </button>
        </div>

    </div>
</template>

<style scoped>
#fetch-button{
    padding: 0.5em;
    background-color: var(--primary-color);
    color: var(--light-color);
    border: none;
    text-decoration: none;
}

#generate-button{
    padding: 0.5em;
    background-color: var(--secondary-color);
    color: var(--light-color);
    border: none;
}
</style>