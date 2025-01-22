<script setup>

import { api } from '@/api';

async function validateForm(e){
    try {
        let res = await api.post("/admin/subjects/", new FormData(e.target))
        console.log(res);
        return res;
    }
    catch(err){
        console.log(err);
    }
}
</script>

<template>
    <div class="d-flex flex-row flex-grow-1 justify-content-center pt-5">
        <div class="d-flex flex-column align-items-center w-50">
            <div class="form-div justify-content-center">
                    <h3>
                        Add Subject
                    </h3>
                </div>
            <form @submit.prevent="validateForm" class="w-100">
                <input type="hidden">
                <div class="form-div">
                    <input type="text" name="name" placeholder="Title">
                </div>
    
                <div class="form-div">
                    <input type="text" name="description" placeholder="Description">
                </div>
    
                <div class="form-div">
                    <input type="number" name="credits" placeholder="Credits">
                </div>
    
                <div class="form-div">
                    <input type="submit">
                </div>
                
            </form>
        </div>
    </div>
</template>

<style scoped>
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