<script setup>
import { ref } from 'vue';
import { api } from '@/api';

const subjects = ref(null);
const requests = ref(null);

async function fetchSubjects(){
    let res = await api.get(`/user/subjects/all`);
    subjects.value = res.data.payload;
}

async function fetchRequests(){
    let res = await api.get(`/user/enrolled/`);
    requests.value = res.data.payload;
}

Promise.all([fetchSubjects(),fetchRequests()])
</script>

<template>
    <div v-if="subjects" class="d-flex flex-column align-items-center mt-4">
        <h2>
            Send a register request!
        </h2>
        <div class="d-flex flex-column mb-4 align-items-center" v-for="subject in subjects">
            <button class="subject-button" @click="async () =>{
                let res = await api.post(`/user/enrolled/`, {
                    subject_id: subject.id
                }, 
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            );
            Promise.all([fetchSubjects(),fetchRequests()])
            }">
                <h3>
                    {{ subject.name }}
                </h3>
            </button>
            {{ subject.description }}
        </div>
    </div>

    <div v-if="requests" class="d-flex flex-column align-items-center mt-4">
        <h2>
            See pending requests!
        </h2>

        <div v-if="requests.length == 0">
            No pending requests!
        </div>

        <div v-else>
            <div class="d-flex flex-column align-items-center" v-for="subject in requests">
                <h3 class="mb-3">
                    {{ subject.name }}
                </h3>
            </div>
        </div>
    </div>
</template>

<style scoped>
.subject-button{
    background-color: light-dark(var(--light-color),var(--dark-color));
    color: var(--secondary-color);
    border: none;
}
</style>