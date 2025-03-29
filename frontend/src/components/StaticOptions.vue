<!-- 
 Renders a static (non-editable) view of all 4 options
-->
<script setup>
    import StaticOption from './StaticOption.vue';
    const props = defineProps(['question','marked'])
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 mt-3">
        <div class="d-flex flex-row justify-content-center flex-wrap w-100">
            <template v-for="n in 4">
                <StaticOption :optionNo="n - 1" :correctOption="props.question.correct" :optionText="props.question.options[n - 1]" :marked="props.marked"/>
            </template>
        </div>
    </div>
</template>

<style scoped>
</style>