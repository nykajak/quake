<script setup>
    import StaticQuestion from './StaticQuestion.vue';
    import StaticOptions from './StaticOptions.vue';

    const props = defineProps(['response'])

</script>

<template>
    <div class="mt-4 mb-4">
        <StaticQuestion :description="props.response.question.description"/>
        <StaticOptions :question="props.response.question"/>
    </div>
</template>

<style scoped>
</style>
