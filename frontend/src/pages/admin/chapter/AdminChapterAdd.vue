<script setup>
import { useRouter } from 'vue-router';

import { api } from '@/api';

const router = useRouter();
const props = defineProps(['sid'])

async function validateForm(e){
    try {
        let res = await api.post(`/admin/subjects/${props.sid}/chapters/`, new FormData(e.target))
        router.push({"path":`/admin/subjects/${props.sid}/chapters/${res.data.payload.id}`})
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
                        Add Chapter
                    </h3>
                </div>
            <form @submit.prevent="validateForm" class="w-100">
                <div class="form-div">
                    <input type="text" name="name" placeholder="Title" required>
                </div>
    
                <div class="form-div">
                    <input type="text" name="description" placeholder="Description">
                </div>
    
                <div class="form-div">
                    <input type="submit" id="form-submit-button">
                </div>
                
            </form>
        </div>
    </div>
</template>

<style scoped>
</style>