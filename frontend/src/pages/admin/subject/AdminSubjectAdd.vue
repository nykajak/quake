<script setup>

import { api } from '@/api';
import { useRouter } from 'vue-router';

const router = useRouter();

async function validateForm(e){
    try {
        let res = await api.post("/admin/subjects/", new FormData(e.target))
        router.push({"path":`/admin/subjects/${res.data.payload.id}`})
        return;
    }
    catch(err){
        console.log(err);
    }
}
</script>

<template>
    <div class="d-flex flex-row flex-grow-1 justify-content-center pt-5">
        <div class="d-flex flex-column align-items-center w-75">
            <div class="form-div justify-content-center">
                    <h3 class="form-header">
                        Add Subject
                    </h3>
                </div>
            <form @submit.prevent="validateForm" class="w-100">
                <input type="hidden">
                <div class="form-div">
                    <input type="text" name="name" placeholder="Title" required>
                </div>
    
                <div class="form-div">
                    <input type="text" name="description" placeholder="Description">
                </div>
    
                <div class="form-div">
                    <input type="number" name="credits" placeholder="Credits" required>
                </div>
    
                <div class="form-div">
                    <input type="submit" id="form-submit-button">
                </div>
                
            </form>
        </div>
    </div>
</template>

<style scoped>
.form-header{
    color: var(--secondary-color)
}

#form-submit-button{
    border: 1px solid var(--light-color);
    background-color: var(--secondary-color);
    color: var(--light-color);
}

.form-div {
    display: flex;
    margin: 0.75rem;
}

.form-div input {
    display: flex;
    flex-grow: 1;
    height: 2.5em;
    padding-left: 0.5em;
}
</style>