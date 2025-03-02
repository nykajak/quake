<script setup>
    const props = defineProps(['index', 'description'])
</script>

<template>
    <div class="question-no-div">
        <div>
            Q{{ props.index }}
        </div>
    </div>
    <div class="question-statement-div">
        {{ props.description }}
    </div>
</template>

<style scoped>
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

</style>