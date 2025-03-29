<script setup>
    import { RouterLink, useRoute, useRouter } from 'vue-router';
    import { ref } from 'vue';
    import { api } from '@/api';

    import StaticQuestion from '@/components/StaticQuestion.vue';
    import PaginationToolBar from '@/components/PaginationToolBar.vue';
    import Message from '@/components/Message.vue';

    const props = defineProps(['sid','cid','qid'])
    const router = useRouter();
    const route = useRoute();

    let q = route.query.q ?? ''
    let filter = route.query.filter ?? 'all'
    
    const questions = ref([]);
    const pages = ref(null);
    const errorMessage = ref('');

    async function fetchResults(e){
        const f = new FormData(e.target);
        q = f.get("q")
        filter = f.get("filter")
        router.push({
            "path": route.path,
            "query": {
                ...route.query,
                "q": q,
                "filter": filter,
                "page": 1
            }
        })
    }

    async function initialFetch(){
        let page = route.query.page ?? 1;
        let per_page = route.query.per_page ?? 5;
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions?q=${q}&filter=${filter}&page=${page}&per_page=${per_page}`);
        pages.value = res.data.pages;
        questions.value = res.data.payload;
    }

    async function addQuestion(id){
        const formData = new FormData();
        formData.append('question_id',id);
        try{
            let res = await api.post(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions/add`, formData)
        }
        catch(err){
            errorMessage.value = err.response.data.msg
            return 
        }   
        router.go(0);
    }

    async function removeQuestion(id){
        const formData = new FormData();
        formData.append('question_id',id);
        try{
            let res = await api.post(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions/remove`, formData)
        }
        catch(err){
            errorMessage.value = err.response.data.msg
            return
        }
        router.go(0);
    }

    initialFetch()
</script>

<template>
    <Message v-if='errorMessage' level="danger" :hide-function="()=>{
        errorMessage = ''
    }">
        {{ errorMessage }}
    </Message>
    <div v-if="questions && pages" class="d-flex flex-column flex-grow-1 mt-2 align-items-center">
        <h3 class="text-center">Searching questions for Quiz</h3>
        <form @submit.prevent="fetchResults" class="d-flex flex-column w-100 align-items-center mt-1">
            <div class="form-div">
                <label for="q" class="form-div-label">Search term: </label>
                <input type="text" class="form-div-input" name="q" :value="route.query.q ?? ''">
            </div>
            <div class="form-options-div-container">
                <div class="form-options-div">
                    <label for="added-search">Search all questions</label>
                    <input type="radio" name="filter" id="added-search" value="all" :checked="route.query.filter ? route.query.filter == 'all': true">
                    <label for="added-search">Search present questions</label>
                    <input type="radio" name="filter" id="added-search" value="present" :checked="route.query.filter ? route.query.filter == 'present' : false">
                    <label for="all-search">Search absent questions</label>
                    <input type="radio" name="filter" id="all-search" value="absent" :checked="route.query.filter ? route.query.filter == 'absent' : false">
                </div>
            </div>

            <div class="form-div justify-content-center">
                <input type="submit" value="Search" id="search-button">
            </div>
        </form>

        <div class="results-div mt-2 w-75">
            <div v-for="question in questions" class="d-flex">
                <div class="d-flex flex-grow-1">
                    <RouterLink class="w-100" :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                        <StaticQuestion :description="question.description"/>
                    </RouterLink>
                </div>
                <div>
                    <button id="add-button" class="manage-button" v-if="route.query.filter == 'absent' || ((route.query.filter ? route.query.filter == 'all': true) && question.present == false)" @click="()=>addQuestion(question.id)">+</button>
                    <button id="remove-button" class="manage-button" v-if="route.query.filter == 'present' || ((route.query.filter ? route.query.filter == 'all': true) && question.present == true)" @click="()=>removeQuestion(question.id)">x</button>
                </div>
            </div>
        </div>
        <PaginationToolBar :num-pages = "pages"/>
    </div>

</template>

<style scoped>

#add-button{
    height: 100%;
    background-color: var(--primary-color);
}

#remove-button{
    height: 100%;
    background-color: var(--error-color);
}

.manage-button{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 1.5em;
    height: 1.5em;
    border: none;
    color: var(--light-color);
}

.results-div{
    display: flex;
    flex-direction: column;
    gap:0.5em;
}

.question-decorator{
    display: flex;
    width: 1.5em;
    height: 100%;
    justify-content: center;
    align-items: center;
    background-color: var(--primary-color);
    color: var(--light-color);  
}

.question-div{
    display: flex;
    width: 40em;
    padding: 0.5em;
    gap:0.5em;  
}

#search-button{
    background-color: var(--secondary-color);
    color: var(--light-color);
    border: none;
}

.form-options-div-container{
    display: flex;
    align-items: center;
}

.form-div{
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 60%;
    gap:1em;    
    padding: 0.5em;
}

.form-div-input{
    display: flex;
    flex-grow: 1;
}

.form-options-div{
    display: flex;
    flex-direction: row;
    gap:1em;    
    padding: 0.5em;
    margin-left:1em;
    margin-right:1em;
}
</style>