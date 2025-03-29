<script setup>
import { defineProps } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps(['chapter','active'])
</script>

<template>
    <div class="d-flex flex-column justify-content-center align-items-center text-center">
        <h1 v-if="!props.active" class="chapter-heading">{{ props.chapter.name }}</h1>
        <h1 v-else class="chapter-heading"><RouterLink :to="'/admin/subjects/'+props.chapter.subject.id+'/chapters/'+props.chapter.id">{{ props.chapter.name }}</RouterLink></h1>
    
        <p class="description">
            {{ props.chapter.description ?? "No description given!" }}
        </p>
    </div>
</template>

<style scoped>
.chapter-heading{
    font-size: 2.5em;
}
.description{
    font-size: 1.25em;
}
</style>