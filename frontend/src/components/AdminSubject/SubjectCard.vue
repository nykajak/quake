<script setup>
    import { defineProps } from 'vue';
    import { RouterLink } from 'vue-router';
    const props = defineProps(['subject','active'])
</script>

<template>
    <div class="d-flex flex-column justify-content-center align-items-center text-center">
        <h3 v-if="active == true">
                <RouterLink :to="'subjects/'+subject.id">
                    {{ props.subject.name }}
                </RouterLink>
        </h3>
        <h3 v-else>
            {{ props.subject.name }}
        </h3>
        <p v-if="props.subject.description">
            {{ props.subject.description }}
        </p>
        <p v-else>
            No description provided!
        </p>
    </div>
</template>

<style scoped>
</style>