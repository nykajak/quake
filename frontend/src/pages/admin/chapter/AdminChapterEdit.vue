<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

import Loader from '@/components/Loader.vue';

const props = defineProps(['sid','cid']);
const router = useRouter();
const chapter = ref(null);
const errorMessage = ref(null);

async function fetchChapter(){
    try{
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}`)
        chapter.value = res.data.payload
    }
    catch(err){
        if (err.response && err.response.status){
            // Chapter not found error
            if(err.response.status == 404){
                errorMessage.value = 'No such chapter!';
            }
            else{
                errorMessage.value = 'Unforeseen error!';
                console.log(err.response);
            }
        }
        else{
            errorMessage.value = 'Unforeseen error!';
            console.log(err)
        }
    }
}

async function editChapter(){
    const f = new FormData();
    f.append("name",document.getElementById("edit-name").value)
    f.append("description",document.getElementById("edit-description").innerText)

    let res = await api.put(`/admin/subjects/${props.sid}/chapters/${props.cid}`,f)
    router.push({
        "path": `/admin/subjects/${props.sid}/chapters/${props.cid}`
    })
    return res.data
}

fetchChapter()

</script>

<template>
    <div v-if="chapter" class="d-flex flex-column flex-grow-1 mt-2">
        <div class="d-flex flex-column justify-content-center align-items-center text-center">
            <input id="edit-name" type="text" :value="chapter.name">
            <div contenteditable="true" id="edit-description" type="text">
                {{ chapter.description }}
            </div>

            <input id="submit-button" type="submit" @click="editChapter" value="Confirm Edits?">
        </div>
    </div>

    <Loader v-if="chapter == null && errorMessage == null"/>

    <div v-if="errorMessage" class="d-flex flex-column flex-grow-1 mt-4 align-items-center ">
        <RouterLink :to="'/admin/subjects/'+props.sid">
            <h2>
                Back to Subject
            </h2>
        </RouterLink>
        <h2>
            {{ errorMessage }}
        </h2>
    </div>
</template>

<style scoped>
#submit-button{
    display: flex;
    background-color: var(--secondary-color);
    border: none;
    color: var(--light-color);
    padding: 0.33em;
}

#edit-name{
    display: flex;
    text-align: center;
    background-color: light-dark(var(--light-color),var(--dark-color));
    color: var(--secondary-color);
    outline: none;
    border: none;
    font-size: 2.5em;
    width: 100%;
}

#edit-description{
    font-size: 1.5em;
    margin-bottom: 0.75em;
    outline: none;
    width: 100%;
}
</style>