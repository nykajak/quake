<script setup>
    import { RouterLink, useRoute, useRouter } from 'vue-router';
    import { ref } from 'vue';
    import { api } from '@/api';

    const props = defineProps(['sid','cid','qid'])
    const router = useRouter();
    const route = useRoute();

    let q = route.query.q ?? ''
    let filter = route.query.filter ?? 'all'

    const questions = ref([]);

    async function fetchResults(e){
        const f = new FormData(e.target);
        q = f.get("q")
        filter = f.get("filter")
        router.push({
            "path": route.path,
            "query": {
                "q": q,
                "filter": filter
            }
        })
    }

    async function initialFetch(){
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions?q=${q}&filter=${filter}`);
        questions.value = res.data.payload;
    }

    async function addQuestion(id){
        const formData = new FormData();
        formData.append('question_id',id);
        let res = await api.post(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions/add`, formData)
    }

    async function removeQuestion(id){
        const formData = new FormData();
        formData.append('question_id',id);
        let res = await api.post(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions/remove`, formData)
    }

    initialFetch()
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 mt-2 align-items-center">
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

        <div class="results-div mt-2">
            <div v-for="question in questions" class="question-div">
                <div class="question-decorator">
                    Q
                </div>
                <div class="d-flex flex-grow-1">
                    <RouterLink :to="`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${question.id}`">
                        {{ question.description.length < 80 ? question.description : question.description.slice(0,75) + "..." }}
                    </RouterLink>
                </div>
                <div>
                    <button id="add-button" class="manage-button" v-if="route.query.filter == 'absent' || ((route.query.filter ? route.query.filter == 'all': true) && question.present == false)" @click="()=>addQuestion(question.id)">+</button>
                    
                    <button id="remove-button" class="manage-button" v-if="route.query.filter == 'present' || ((route.query.filter ? route.query.filter == 'all': true) && question.present == true)" @click="()=>removeQuestion(question.id)">x</button>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>

#add-button{
    background-color: var(--secondary-color);
}

#remove-button{
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
    height: 1.5em;
    justify-content: center;
    background-color: var(--secondary-color);
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