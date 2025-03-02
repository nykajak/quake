<script setup>
    const props = defineProps(['description','index'])
</script>

<template>
    <div class="question-no-div">
        <div>
            Q{{ index }}
        </div>
    </div>
    <div class="question-statement-div">
        <div id="question-statement" contenteditable="true">
            {{description}}
        </div>
    </div>
</template>

<style scoped>
#question-statement{
    display: flex;
    flex-wrap: wrap;
    outline: none;
}

.question-statement-div{
    display: flex;
    justify-content: center;
    flex-grow: 1;
    text-align: center;
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

</style>