<script setup>
    import { RouterLink } from 'vue-router';
    import { ref } from 'vue';
    import { api } from '@/api';

    const props = defineProps(['sid','cid','qid'])
    
    const questions = ref([]);

    async function fetchResults(e){
        const f = new FormData(e.target);
        const q = f.get("q")
        const filter = f.get("filter")

        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions?q=${q}&filter=${filter}`);
        questions.value = res.data.payload;
    }

    async function initialFetch(){
        let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions`);
        questions.value = res.data.payload;
    }

    initialFetch()
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 mt-2 align-items-center">
        <h3 class="text-center">Searching questions for Quiz</h3>
        <form @submit.prevent="fetchResults" class="d-flex flex-column w-100 align-items-center mt-1">
            <div class="form-div">
                <label for="q" class="form-div-label">Search term: </label>
                <input type="text" class="form-div-input" name="q">
            </div>
            <div class="form-options-div-container">
                <div class="form-options-div">
                    <label for="added-search">Search all questions</label>
                    <input type="radio" name="filter" id="added-search" value="all" checked>
                    <label for="added-search">Search present questions</label>
                    <input type="radio" name="filter" id="added-search" value="present">
                    <label for="all-search">Search absent questions</label>
                    <input type="radio" name="filter" id="all-search" value="absent">
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
                        {{ question.description.length < 90 ? question.description : question.description.slice(0,85) + "..." }}
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>

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