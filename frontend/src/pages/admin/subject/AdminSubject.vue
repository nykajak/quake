<script setup>
    import { defineProps, ref } from 'vue';

    import { api } from '@/api';
    
    import SubjectCard from './components/SubjectCard.vue';
    import ChapterList from './components/ChapterList.vue';
    
    import NavButton from '@/components/NavButton.vue';
    import DeleteButton from '@/components/DeleteButton.vue';
    import Loader from '@/components/Loader.vue';
    import ObjectNotFound from '@/components/ObjectNotFound.vue';

    const props = defineProps(['sid']);
    
    const subject = ref(null);
    const errorMessage = ref('');

    async function fetchSubject(){
        let res;
        try{
            res = await api.get(`/admin/subjects/${props.sid}`);
        }

        catch(err){
            errorMessage.value = err.response.data.msg
            subject.value = true;
            return 
        }
        subject.value = res.data.payload
    }
    
    fetchSubject()
</script>

<template>
    <div v-if="subject" class="d-flex flex-column flex-grow-1 mt-2">
        <template v-if="errorMessage == ''">
            <SubjectCard :subject="subject" :active="false"/>
            <div class="d-flex justify-content-center mb-2">
                <NavButton text="See enrolled" :url="`/admin/subjects/${subject.id}/enrolled`" color="primary"/>
                <NavButton text="Add chapter" :url="`/admin/subjects/${subject.id}/chapters/add`" color="secondary"/>
                <NavButton text="Edit subject" :url="`/admin/subjects/${subject.id}/edit`" color="tertiary"/>
                <DeleteButton :redirect="`/admin/subjects/`" :url="`/admin/subjects/${props.sid}`" color="error">
                    Delete subject
                </DeleteButton>
            </div>
            <ChapterList :chapters="subject.chapters"/>
        </template>

        <ObjectNotFound v-else>
            Subject not found!
        </ObjectNotFound>
    </div>

    <Loader v-else/>
</template>

<style scoped>
</style>