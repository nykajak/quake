<script setup>
import { ref } from 'vue';
import { api } from '@/api';

const subjects = ref(null);
const reload = ref(0);

async function fetchSubjects(){
    let res = await api.get(`/user/subjects/all`);
    subjects.value = res.data.payload;
}

fetchSubjects()
</script>

<template>
    <div v-if="subjects" class="d-flex flex-column align-items-center mt-4">
        <h2>
            Send a register request!
        </h2>
        <div>
            
        </div>
        <div class="d-flex flex-column mb-4 align-items-center" v-for="subject in subjects">
            <button class="subject-button" @click="async () =>{
                let res = await api.post(`/user/enroll`, {
                    subject_id: subject.id
                }, 
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            );
            fetchSubjects();
            }">
                <h3>
                    {{ subject.name }}
                </h3>
            </button>
            {{ subject.description }}
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