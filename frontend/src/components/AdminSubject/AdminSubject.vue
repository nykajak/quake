<script setup>
    import { defineProps, ref } from 'vue';
    import { useRouter } from 'vue-router';
    
    import { api } from '@/api';

    import SubjectCard from './SubjectCard.vue';
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
    <div v-if="loading == false && ready == true">
        <SubjectCard :subject="subject" :active="false"/>
    </div>

    <Loader v-else/>
</template>

<style scoped>
</style>