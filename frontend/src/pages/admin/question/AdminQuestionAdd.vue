<script setup>

import { ref } from 'vue';
import { api } from '@/api';
import { useRouter } from 'vue-router';

import EditableOption from './components/EditableOption.vue';
import EditableQuestion from './components/EditableQuestion.vue';

const props = defineProps(['sid','cid'])
const router = useRouter();

const correctOption = ref(-1);

async function createQuestion(e){
    let f = new FormData(e.target);
    f.append("description",document.getElementById("question-statement").innerText)
    let res = await api.post(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/`, f)
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
                <EditableQuestion description=""/>
            </div>
            
            <div class="option-container">
                <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                    <template v-for="n in 4">
                        <EditableOption default="" :option="n - 1" :correct-option="correctOption" :set-correct-option="(x)=>{
                            correctOption = x;
                        }"/>
                    </template>
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