<script setup>
import { defineProps } from 'vue';

const props = defineProps(['subject']);

</script>

<template>
    {{ props.subject.id }}
    <br>
    {{ props.subject.name }}
    <br>
    {{ props.subject.description }}
</template>

<style scoped>
</style>