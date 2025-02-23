<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

import Loader from '@/components/Loader.vue';
import { RouterLink } from 'vue-router';

const router = useRouter();
const props = defineProps(['sid','cid']);
const loading = ref(false);
const ready = ref(false);
const chapter = ref(null);

async function fetchChapter(){
    try{
        loading.value = true;
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}`)
        loading.value = false;
        return res.data.payload
    }
    catch(err){
        console.log(err);
        loading.value = false;
        router.push({"name":"NotFound"})
        return -1
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

fetchChapter().then(data => {
    if (data != -1){
        chapter.value = data;
        ready.value = true;
    }
})

</script>

<template>
    <div v-if="loading == false && ready == true" class="d-flex flex-column flex-grow-1 mt-2">
        <div class="d-flex flex-column justify-content-center align-items-center text-center">
            <input id="edit-name" type="text" :value="chapter.name">
            <div contenteditable="true" id="edit-description" type="text">
                {{ chapter.description }}
            </div>

            <input id="submit-button" type="submit" @click="editChapter" value="Confirm Edits?">
        </div>
    </div>
    <Loader v-else/>
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