<script setup>
    import StaticOption from './StaticOption.vue';
    const props = defineProps(['question'])
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 mt-3">
        <div class="d-flex flex-row justify-content-center flex-wrap w-100">
            <template v-for="n in 4">
                <StaticOption :optionNo="n - 1" :correctOption="props.question.correct" :optionText="props.question.options[n - 1]"/>
            </template>
        </div>
    </div>
</template>

<style scoped>
</style>