<script setup>
    import { RouterLink } from 'vue-router';

    const props = defineProps(['sid','cid','qid'])
    
    const questions = [
        {
            "description": "What is 1 + 1?",
            "id": 1,
        },
        {
            "description": "What is 54 + 54?",
            "id": 2,
        },
        {
            "description": "What is 23 + 11?",
            "id": 3,
        }
    ]
    async function fetchResults(e){
        const f = new FormData(e.target);
        for (let e of f.entries()){
            console.log(e);
        }
    }
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
                    <label for="description-search">Search by description</label>
                    <input type="radio" name="type" id="description-search" value="description" checked>
                    <label for="option-search">Search by option</label>
                    <input type="radio" name="type" id="option-search" value="option">
                </div>
    
                <div class="form-options-div">
                    <label for="added-search">Search added only</label>
                    <input type="radio" name="space" id="added-search" value="description" checked>
                    <label for="all-search">Search not added</label>
                    <input type="radio" name="space" id="all-search" value="option">
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