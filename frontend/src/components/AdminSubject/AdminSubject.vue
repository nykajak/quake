<script setup>
    import { defineProps, ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { RouterLink } from 'vue-router';
    
    import { api } from '@/api';

    import SubjectCard from './SubjectCard.vue';
    import ChapterCard from '../AdminChapter/ChapterCard.vue';
    import Loader from '../Utility/Loader.vue';

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
    
    fetchSubject().then(data => {
        if (data != -1){
            subject.value = data;
            ready.value = true;
        }
    })
</script>

<template>
    <div v-if="loading == false && ready == true" class="d-flex flex-column flex-grow-1 mt-2">
        <div class="d-flex flex-column align-items-center">
            <RouterLink :to="`/admin/subjects/${subject.id}/chapters/add`">Add Chapter</RouterLink>
        </div>
        <SubjectCard :subject="subject" :active="false"/>
        <div class="d-flex justify-content-center">
            <RouterLink :to="'/admin/subjects/'+subject.id+'/enrolled'">See Enrolled</RouterLink>
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