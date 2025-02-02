<script setup>
    import { defineProps, ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { RouterLink } from 'vue-router';
    
    import { api } from '@/api';

    import SubjectCard from './components/SubjectCard.vue';
    import ChapterCard from '../chapter/components/ChapterCard.vue';
    import Loader from '@/components/Loader.vue';

    const router = useRouter();
    const props = defineProps(['sid']);
    
    const subject = ref(null);
    const loading = ref(false);
    const ready = ref(false);

    async function fetchSubject(){
        try{
            loading.value = true;
            let res = await api.get(`/admin/subjects/${props.sid}`);
            loading.value = false;
            return res.data.payload
        }

        catch(err){
            loading.value = false;
            router.push({"name":"NotFound"})
            return -1
        }
    }
    
    async function editSubject(e){
        const f = new FormData();
        f.append("name",document.getElementById("edit-title").value)
        f.append("description",document.getElementById("edit-description").innerText)

        let res = await api.put(`/admin/subjects/${props.sid}`,f)
        console.log(res.data)
        return res.data
    }

    fetchSubject().then(data => {
        if (data != -1){
            subject.value = data;
            ready.value = true;
        }
    })

</script>

<template>
    <div v-if="loading == false && ready == true" class="d-flex flex-column flex-grow-1 mt-2">
        <div class="d-flex flex-column justify-content-center align-items-center text-center">
            <input id="edit-title" type="text" :value="subject.name">
            <div id="edit-description" contenteditable="true">
                {{ subject.description }}
            </div>
        </div>

        <div class="d-flex justify-content-center mb-2">
            <input type="submit" class="option-button" id="edit-button" @click="editSubject" value="Confirm Edits?" />
        </div>
        <div class="chapters">
            <h1 class="heading">Chapters</h1>
            <div class="d-flex flex-column align-items-center m-2" v-for="chapter in subject.chapters">
                <ChapterCard :chapter="chapter" :active="1"></ChapterCard>
            </div>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>

#edit-title{
    display: flex;
    text-align: center;
    background-color: light-dark(var(--light-color),var(--dark-color));
    color: var(--secondary-color);
    outline: none;
    border: none;
    font-size: 2.5em;
}

#edit-description{
    font-size: 1.5em;
    margin-bottom: 0.75em;
    outline: none;
}

.option-button{
    display: flex;
    border: none;
    padding: 0.5em;
    color: var(--light-color);
}

#edit-button{
    background-color: var(--error-color);
}

#add-button{
    background-color: var(--tertiary-color);
}

#enroll-button{
    background-color: var(--secondary-color);
}

.chapters{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1em;
    flex-grow: 1;
    border-top: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.heading{
    color: var(--secondary-color);
    font-size: 3em;
}

.chapter-heading{
    font-size: 2.5em;
}
</style>