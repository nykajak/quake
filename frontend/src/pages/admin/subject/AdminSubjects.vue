<script setup>
    import { ref } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    import { RouterLink } from 'vue-router';

    import { api } from '@/api';

    import PaginationToolBar from '@/components/PaginationToolBar.vue';
    import Loader from '@/components/Loader.vue';
    import SubjectCard from './components/SubjectCard.vue';

    const route = useRoute();
    const router = useRouter();
    
    const subjects = ref([]);
    const numPages = ref(0);
    const loading = ref(false);
    const ready = ref(false);
    const subjectname = ref(route.query.q ?? '');

    async function fetchSubjects(){
        try{
            let page = route.query["page"] ?? 1;
            let per_page = route.query["per_page"] ?? 5 ;
            let q = route.query["q"] ?? "";
            loading.value = true;
            let res = await api.get(`/admin/subjects/?page=${page}&per_page=${per_page}&q=${q}`);
            loading.value = false;
            numPages.value = res.data.pages
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
    <div v-if="loading == false" class="d-flex flex-column flex-grow-1">
        <div class="d-flex flex-column align-items-center flex-grow-1">
            <div class="subject-sidebar d-flex flex-column text-center justify-content-center align-items-center w-75">
                <div class="d-flex gap-2">
                    <h3 id="heading-info">
                        Querying subjects
                    </h3>
                </div>
                <div class="d-flex w-100 mb-2">
                    <button id="add_button" @click="router.push({
                        path: '/admin/subjects/add'
                    })">+</button>
                    <input class="d-flex flex-grow-1" type="text" v-model="subjectname" placeholder="Subject">
                    <button class="query-button" @click="router.push({
                        'path': 'subjects',
                        'query': {
                            ...route.query,
                            'q': subjectname,
                            'page': 1
                        }
                    })">Search subjects</button>
                </div>
            </div>
            <div class="result-container-div">
                <div class="d-flex flex-column flex-grow-1 justify-content-center">
                    <div class="results-div">
                        <div v-for="subject in subjects" class="pl-2 pr-2 mb-2">
                            <SubjectCard :subject="subject" :active="true"/>
                        </div>
                    </div>
                </div>
                <PaginationToolBar :num-pages="numPages"/>
            </div>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>
.result-container-div{
    display: flex;
    flex-grow: 1;
    flex-direction: column;
    width: 75%;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
}

#heading-info{
    font-size: 3em;
    color: var(--secondary-color);
    padding-bottom: 0.3em;
}

#add_button{
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    color: var(--light-color);
    background-color: var(--tertiary-color);
    padding-left: 0.7em;
    padding-right: 0.7em;
}

.results-div{
    margin-top: 3em;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
}

.subject-sidebar{
    margin-top: 1em;
}

.query-button{
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    background-color: var(--secondary-color);
    color: var(--light-color);
}

input {
    padding-left: 0.5em;
}
</style>