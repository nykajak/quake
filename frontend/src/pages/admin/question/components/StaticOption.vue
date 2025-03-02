<script setup>
    const props = defineProps(['optionNo', 'correctOption', 'optionText'])
    const mapping = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
    }
</script>

<template>
    <div class="option-button">
        <div :class="{'rounded-div':true, 'selected-option':props.correctOption == props.optionNo}">
            {{ mapping[props.optionNo] }}
        </div>
        <div class="option-text">
            {{ props.optionText }}
        </div>
    </div>
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

.selected-option{
    background-color: green !important;
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