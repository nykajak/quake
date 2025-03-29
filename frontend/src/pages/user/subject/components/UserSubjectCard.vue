<script setup>
import { defineProps } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps(['subject','active']);

</script>

<template>
    <div class="d-flex flex-column align-items-center text-center">
        <h3 v-if="active == 1">
            <RouterLink :to="`/user/subjects/${props.subject.id}`">
                {{ props.subject.name }}    
            </RouterLink>
        </h3>

        <h3 v-else>{{ props.subject.name }}</h3>
        <p>
            {{ props.subject.description ? props.subject.description : "No description yet!" }}
        </p>
    </div>
</template>

<style scoped>
</style>