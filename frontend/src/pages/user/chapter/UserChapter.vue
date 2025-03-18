<script setup>
    import { ref, watch } from 'vue';
    import { api } from '@/api';
    import { RouterLink, useRouter,useRoute } from 'vue-router';

    import Loader from '@/components/Loader.vue';
    import Pagination from '@/components/Pagination.vue';
    import PerPage from '@/components/PerPage.vue';
    
    const router = useRouter();
    const route = useRoute();
    const props = defineProps(['sid','cid'])
    const chapter = ref({
        "name": "Chapter"
    });
    const quizes = ref([]);
    const pages = ref(null);
    const filter = ref(route.query.filter ?? 'pending')

    async function fetchQuizes(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 3;
        try{
            let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}?filter=${filter.value}&page=${page}&per_page=${per_page}`);
            quizes.value = res.data.quizes;
            chapter.value = res.data.payload;
            pages.value = res.data.pages;
        }
        catch(err){
            console.log(err);
            router.go(-1);
        }
    }
    
    fetchQuizes();

    watch(filter,(newVal,oldVal) =>{
        router.push({
            "to": route.fullPath,
            "query": {
                "filter" : filter.value,
                "page": 1
            }
        })
    })
</script>

<template>
    <div v-if="chapter && chapter.subject" class="d-flex flex-column flex-grow-1 mt-3">
        <div class="d-flex flex-column align-items-center">
            <div>
                <h3>
                    <RouterLink :to="`/user/subjects/${props.sid}`">
                        {{chapter.subject.name}}
                    </RouterLink>
                </h3>
            </div>
            <div>
                <h1>
                    {{chapter.name}}
                </h1>
            </div>
        </div>

        <div class="d-flex w-100 justify-content-center gap-2">
            Past: <input type="radio" v-model="filter" value="past">
            Pending: <input type="radio" v-model="filter" value="pending">
        </div>
        <div class="d-flex w-100 align-items-center justify-content-center mb-2 gap-1 mt-2">
            Quizes per page: <PerPage/>
        </div>

        <div class="results-div">
            <div class="result-obj" v-for="quiz in quizes">
                <div>
                    <h4>
                        <RouterLink :to="`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${quiz.id}`">
                            {{quiz.description ?? 'No description given!'}}
                        </RouterLink>
                    </h4>
                </div>
                <div class="d-flex flex-column align-items-center">
                    <p class="text-center">
                        Start time: {{ quiz.dated.day }}-{{ quiz.dated.month }}-{{ quiz.dated.year }}, at {{ quiz.dated.hour }}:{{ quiz.dated.minute }}
                        <br>
                        Duration: {{quiz.duration}} minutes
                    </p>
                </div>
            </div>
            <Pagination :url="route.fullPath" :pages="pages"/>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>
.result-obj{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5em;
}

.results-div{
    display: flex;
    flex-direction: column;
    margin-top:1em;
    gap:1em;
}

</style>