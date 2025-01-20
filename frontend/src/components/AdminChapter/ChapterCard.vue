<script setup>
import { defineProps } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps(['chapter','active'])

</script>

<template>
    <h1 v-if="active == 0" class="chapter-heading">{{ chapter.name }}</h1>
    <h1 v-else class="chapter-heading"><RouterLink :to="'/admin/subjects/'+chapter.subject.id+'/chapter/'+chapter.id">{{ chapter.name }}</RouterLink></h1>

    <p class="description">
        {{ chapter.description ?? "No description given!" }}
    </p>
</template>

<style scoped>
.chapter-heading{
    font-size: 2.5em;
}
.description{
    font-size: 1.25em;
}
</style>