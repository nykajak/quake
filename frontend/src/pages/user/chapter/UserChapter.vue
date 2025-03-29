<script setup>
    import { ref, watch } from 'vue';
    import { api } from '@/api';
    import { RouterLink, useRouter,useRoute } from 'vue-router';

    import Loader from '@/components/Loader.vue';
    import PaginationToolBar from '@/components/PaginationToolBar.vue';
    import SearchButton from '@/components/SearchButton.vue';
    
    const props = defineProps(['sid','cid'])
    const router = useRouter();
    const route = useRoute();
    
    const chapter = ref(null);
    const pages = ref(null);
    const quizes = ref(null);
    const filter = ref(route.query.filter ?? 'pending')
    const query_str = ref(route.query.q ?? "")

    async function search(){
        router.push({
            'path' : route.fullPath,
            'query': {
                ...route.query,
                'page' : 1,
                'q': query_str.value
            }
        })
    }

    async function fetchQuizes(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 5;
        let q = route.query.q ?? "";
        try{
            let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}?filter=${filter.value}&page=${page}&per_page=${per_page}&q=${q}`);
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
    <div v-if="chapter && chapter.subject" class="d-flex align-items-center flex-column flex-grow-1 mt-3">
        <div class="d-flex flex-column align-items-center text-center">
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
                <p class="descriptionDiv text-center">
                    {{chapter.description ?? 'No description provided!'}}
                </p>
            </div>
        </div>

        <div class="d-flex w-100 justify-content-center gap-2 mt-2">
            <h4>
                Showing all {{ filter }} quizes
            </h4>
        </div>

        <div class="d-flex w-100 justify-content-center gap-2 mt-2">
            Past: <input type="radio" v-model="filter" value="past">
            Pending: <input type="radio" v-model="filter" value="pending">
        </div>

        <div class="d-flex justify-content-center align-items-center mt-2 w-75">
            <input class="d-flex flex-grow-1 h-100" type="text" v-model="query_str" placeholder="Description">
            <SearchButton :query_str="query_str">
                Search by description
            </SearchButton>
        </div>

        <div class="results-div">
            <div v-if="quizes !== null && quizes.length > 0" class="result-obj" v-for="quiz in quizes">
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

            <div class="result-obj" v-else-if="quizes !== null && quizes.length === 0">
                No quizes matching requirements found!
            </div>

            <div v-else class="result-obj">
                Quiz fetching logic error!
            </div>
        </div>
        <PaginationToolBar :num-pages="pages"/>
    </div>

    <Loader v-else/>
</template>

<style scoped>
.descriptionDiv{
    color: var(--contrast-color);
}

.result-obj{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5em;
}

.results-div{
    display: flex;
    flex-direction: column;
    flex-grow:1;
    margin-top:1em;
    gap:1em;
}

</style>