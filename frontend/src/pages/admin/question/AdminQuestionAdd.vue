<script setup>

import { ref } from 'vue';
import { api } from '@/api';
import { useRouter } from 'vue-router';

const props = defineProps(['sid','cid'])
const router = useRouter();
const correctOption = ref(-1);
async function createQuestion(e){
    let f = new FormData(e.target);
    let res = await api.post(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions`, f)
    router.push({
        "path": `/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${res.data.payload}`
    })
    return res.data;
}
</script>

<template>
    <div class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <form @submit.prevent="createQuestion">
            <input type="hidden" name="correct" :value="correctOption">
            <div class="question-container">
                <div class="question-no-div">
                    <div>
                        Q
                    </div>
                </div>
                <div class="question-statement-div">
                    <textarea type="text" class="question-input" placeholder="Question Text" name="description"></textarea>
                </div>
            </div>
            
            <div class="option-container">
                <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                    <div class="option-button">
                        <button :class="{'rounded-div':true,'selected-option':correctOption === 0}" @click.prevent="() => {correctOption = 0}">
                            A
                        </button>
                        <div class="option-text">
                            <input type="text" class="option-input" name="options[0]">
                        </div>
                    </div>
        
                    <div class="option-button">
                        <button :class="{'rounded-div':true,'selected-option':correctOption === 1}" @click.prevent="() => {correctOption = 1}">
                            B
                        </button>
                        <div class="option-text">
                            <input type="text" class="option-input" name="options[1]">
                        </div>
                    </div>
        
                    <div class="option-button">
                        <button :class="{'rounded-div':true,'selected-option':correctOption === 2}" @click.prevent="() => {correctOption = 2}">
                            C
                        </button>
                        <div class="option-text">
                            <input type="text" class="option-input" name="options[2]">
                        </div>
                    </div>
        
                    <div class="option-button">
                        <button :class="{'rounded-div':true,'selected-option':correctOption === 3}" @click.prevent="() => {correctOption = 3}">
                            D
                        </button>
                        <div class="option-text">
                            <input type="text" class="option-input" name="options[3]">
                        </div>
                    </div>
                </div>
            </div>
    
            <div class="d-flex justify-content-center mt-3">
                <input type="submit" id="submit-button" value="Add Question">
            </div>
        </form>
    </div>

</template>

<style scoped>

.option-button:has(.selected-option){
    input{
        background-color: green;
        border-color: green;    
        transition: none;
    }
    background-color: green;
}

.selected-option{
    background-color: green !important;
}

#submit-button{
    border: 1px solid var(--light-color);
    color: var(--light-color);
    background-color: var(--tertiary-color);
    padding: 0.5em;
    border-radius: 10px;
}

textarea:focus, input:focus{
    outline: none;
}


.question-input{
    display: flex;
    width: 100%;
    background-color: var(--secondary-color);
    border: 1px solid var(--secondary-color);
    color: var(--light-color);
    min-height: 2em;
}

.question-input::placeholder{
    color: var(--light-color);
    opacity: 60%;
    padding-left: 0.2em;
}

.option-input{
    display: flex;
    width: 100%;
    background-color: var(--secondary-color);
    border: 1px solid var(--secondary-color);
    color: var(--light-color);
    min-height: 2em;
}

.question-container{
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 1px solid var(--light-color);
    padding: 0.33em;
    color: var(--light-color);
    background-color: var(--secondary-color);
}

.question-no-div{
    display: flex;
    flex-direction: row;
    height: 100%;
    margin: 0.33em;
    padding: 0.33em;
    align-self: flex-start;
}

.question-no-div div{
    display: flex;
    border: 1px solid var(--light-color);
    width: 2em;
    height: 2em;
    justify-content: center;
    align-items: center;
    border-radius: 100%;
}

.question-statement-div{
    display: flex;
    justify-content: center;
    flex-grow: 1;
    text-align: center;
}

.option-container{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    margin-top: 2em;
}

.option-text{
    justify-content: center;
    display: flex;
    flex-grow: 1;
}

.option-button{
    max-width: 35%;
    display: flex;
    flex-grow: 1;
    justify-content: center;
    align-items: center;
    padding: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    border: 1px solid var(--light-color);
    background-color: var(--secondary-color);
    border-radius: 1em;
    
    input{
        transition: none;
    }
}

.rounded-div{
    border: 1px solid var(--light-color);
    border-radius: 100%;
    width: 1.5em;
    height: 1.5em;
    display: flex;
    flex-shrink: 0;
    justify-content: center;
    align-items: center;
    margin: 0.33em;
    background-color: var(--secondary-color);
    color: var(--light-color);
}
</style>