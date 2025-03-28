<script setup>
    import StaticOptions from '@/components/StaticOptions.vue';
    import StaticQuestion from '@/components/StaticQuestion.vue';
    const props = defineProps(['question'])

</script>

<template>
    <StaticQuestion :index="props.question.id" :description="props.question.description" />
    <StaticOptions :question="props.question"/>
</template>

<style scoped>

</style>