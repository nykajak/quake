<script setup>
    import { defineProps } from 'vue';
    import { RouterLink } from 'vue-router';
    const props = defineProps(['subject','active'])
</script>

<template>
    <div class="d-flex flex-column justify-content-center align-items-center text-center">
        <h1 v-if="active == true">
                <RouterLink :to="'subjects/'+subject.id">
                    {{ props.subject.name }}
                </RouterLink>
        </h1>
        <h1 v-else>
            {{ props.subject.name }}
        </h1>
        <p v-if="props.subject.description">
            {{ props.subject.description }}
        </p>
        <p v-else>
            No description provided!
        </p>
    </div>
</template>

<style scoped>
h1{
    color: var(--secondary-color);
}
p{
    font-size: 1.5em;
}
</style>