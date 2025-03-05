<script setup>
    const props = defineProps(['optionNo', 'correctOption', 'optionText', 'clickable', 'marked'])
    const mapping = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
    }
</script>

<template>
    <div v-if="clickable == null" class="option-button">
        <div :class="{'rounded-div':true, 'marked-option':props.marked == props.optionNo,'selected-option':props.correctOption == props.optionNo}">
            {{ mapping[props.optionNo] }}
        </div>
        <div class="option-text">
            {{ props.optionText }}
        </div>
    </div>

    <button v-if="clickable" class="option-button" @click="props.clickable(props.optionNo)">
        <div :class="{'rounded-div':true, 'selected-option':props.correctOption == props.optionNo}">
            {{ mapping[props.optionNo] }}
        </div>
        <div class="option-text">
            {{ props.optionText }}
        </div>
    </button>
</template>

<style scoped>
.option-button:has(.selected-option){
    input{
        background-color: green !important;
        border-color: green !important;    
        transition: none;
    }
    background-color: green !important;
}

.marked-option{
    background-color: red !important;
}

.selected-option{
    background-color: green !important;
}

.option-button:has(.marked-option):not(:has(.selected-option)){
    input{
        background-color: red !important;
        background-color: red !important;  
        transition: none;
    }
    background-color: red !important;
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