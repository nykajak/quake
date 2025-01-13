<script setup>
    import { ref } from 'vue';
    import { useRoute, useRouter } from 'vue-router';

    import { api } from '@/api';

    import Pagination from '../Utility/Pagination.vue';
    import SubjectCard from './SubjectCard.vue';
    import Loader from '../Utility/Loader.vue';

    const route = useRoute();
    const router = useRouter();
    
    const subjects = ref([]);
    const loading = ref(false);
    const ready = ref(false);

    async function fetchSubjects(){
        try{
            let page = route.query["page"] ?? 1;
            let per_page = route.query["per_page"] ?? 5 ;
            loading.value = true;
            let res = await api.get(`/admin/subjects/?page=${page}&per_page=${per_page}`);
            loading.value = false;
            return res.data.payload;
        }

        catch(err){
            loading.value = false;
            router.push({"name":"NotFound"})
            return -1
        }
    }

    fetchSubjects().then(data => {
        if (data != -1){
            subjects.value = data;
            ready.value = true;
        }
    })

</script>

<template>
    <div v-if="loading == false">
        <div class="results-div">
            <template v-for="subject in subjects">
                <SubjectCard :subject="subject" :active="true"/>
            </template>
        </div>
    
        <Pagination :interval-start="1" :interval-length="6" type="subjects"/>
    </div>

    <Loader v-else/>
</template>

<style scoped>
.results-div{
    margin-top: 3em;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
}
</style>