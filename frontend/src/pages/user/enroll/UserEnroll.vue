<script setup>
import { ref } from 'vue';
import { api } from '@/api';
import { useRouter, useRoute } from 'vue-router';
import SearchButton from '@/components/SearchButton.vue';

const router = useRouter();
const route = useRoute();
const subjects = ref(null);
const requests = ref(null);
const q = ref(route.query.q ?? "");

async function fetchSubjects(){
    let res = await api.get(`/user/subjects/all?q=${q.value}`);
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
        <h2 class="heading">
            Send a register request!
        </h2>
        <div class="d-flex w-75 mb-3">
            <input class="flex flex-grow-1" type="text" v-model="q" placeholder="Subject">
            <SearchButton :query_str="q">
                Search subject
            </SearchButton>
        </div>
        <div class="d-flex flex-column mb-4 align-items-center" v-for="subject in subjects">
            <div class="d-flex align-items-center gap-1">
                <h3>
                    {{ subject.name }}
                </h3>
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
                router.go(0);
                }">
                    Enroll
                </button>
            </div>

            <div class="description">
                {{ subject.description ?? 'No description provided!' }}
            </div>
        </div>
    </div>

    <div v-if="requests" class="d-flex flex-column align-items-center mt-3">
        <h2 class="heading">
            See pending requests!
        </h2>

        <div v-if="requests.length == 0">
            No pending requests!
        </div>

        <div v-else>
            <div class="d-flex flex-column align-items-center mb-3" v-for="subject in requests">
                <h3>
                    {{ subject.name }}
                </h3>
                <div class="description">
                    {{ subject.description ?? 'No description provided!' }}
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.subject-button{
    display: flex;
    background-color: var(--primary-color);
    color: var(--light-color);
    border: none;
    height: 1.5em;
    align-items: center;
}

.heading{
    color: var(--secondary-color);
}

.description{
    color: var(--contrast-color);
}
</style>