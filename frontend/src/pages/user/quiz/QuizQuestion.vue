<script setup>

import { ref } from 'vue';

const props = defineProps(['question']);
let correct = ref(-1);
</script>

<template>
<div v-if="question" class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <div class="question-container">
            <div class="question-no-div">
                <div>
                    Q{{ props.question.id }}
                </div>
            </div>
            <div class="question-statement-div">
                {{ props.question.description }}
            </div>
        </div>
        
        <div class="option-container">
            <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                <button class="option-button" @click="correct = 0">
                    <div :class="{'rounded-div':true, 'selected-option':correct == 0}">
                        A
                    </div>
                    <div class="option-text">
                        {{ props.question.options[0] }}
                    </div>
                </button>
    
                <button class="option-button" @click="correct = 1">
                    <div :class="{'rounded-div':true, 'selected-option':correct == 1}">
                        B
                    </div>
                    <div class="option-text">
                        {{ props.question.options[1] }}
                    </div>
                </button>
    
                <button class="option-button" @click="correct = 2">
                    <div :class="{'rounded-div':true, 'selected-option':correct == 2}">
                        C
                    </div>
                    <div class="option-text">
                        {{ props.question.options[2] }}
                    </div>
                </button>
    
                <button class="option-button" @click="correct = 3">
                    <div :class="{'rounded-div':true, 'selected-option':correct == 3}">
                        D
                    </div>
                    <div class="option-text">
                        {{ props.question.options[3] }}
                    </div>
                </button>
            </div>
            
            <div class="d-flex mt-3 justify-content-center">
                <button id="clear-button" @click="correct = -1">
                    Clear choice
                </button>
            </div>

            <div class="d-flex mt-3 justify-content-between">
                <button class="nav-button">Save and prev</button>
                <button class="nav-button">Save and next</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.nav-button{
    justify-content: center;
    align-items: center;
    padding-left: 0.5em;
    padding-right: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    border: 1px solid var(--light-color);
    background-color: var(--primary-color);
    border-radius: 1em;
}

#clear-button{
    justify-content: center;
    align-items: center;
    padding: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    border: 1px solid var(--light-color);
    background-color: var(--error-color);
    border-radius: 1em;
}

.option-button:has(.selected-option){
    input{
        background-color: green !important;
        border-color: green !important;    
        transition: none;
    }
    background-color: green !important;
}

.selected-option{
    background-color: green !important;
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
    max-width: 25%;
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
}
</style>