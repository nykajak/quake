<script setup>
    import { ref } from 'vue';
    const props = defineProps(['option', 'correctOption','setCorrectOption', 'default'])
    const currentVal = ref(props.default)
    const mapping = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
    }
</script>

<template>
    <div class="option-button">
        <button :class="{'rounded-div':true,'selected-option':props.correctOption === props.option}" @click.prevent="() => {
            props.setCorrectOption(props.option)
        }">
            {{ mapping[props.option] }}
        </button>
        <div class="option-text">
            <input type="text" class="option-input" :name="`options[${props.option}]`" v-model="currentVal">
        </div>
    </div>
</template>

<style scoped>

input:focus{
    outline: none;
}


.option-button:has(.selected-option){
    input{
        background-color: green;
        border-color: green;    
        transition: none;
    }
    background-color: green;
}

.option-text{
    justify-content: center;
    display: flex;
    flex-grow: 1;
}

.option-input{
    display: flex;
    width: 100%;
    background-color: var(--secondary-color);
    border: 1px solid var(--secondary-color);
    color: var(--light-color);
    min-height: 2em;
    text-align: center;
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

.selected-option{
    background-color: green !important;
}

.option-text{
    justify-content: center;
    text-align: center;
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

</style>