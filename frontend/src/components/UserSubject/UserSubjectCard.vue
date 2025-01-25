<script setup>
import { defineProps } from 'vue';

const props = defineProps(['subject']);

</script>

<template>
    <div class="d-flex flex-column align-items-center">
        <h3>{{ props.subject.name }}</h3>
        <p>
            {{ props.subject.description }}
        </p>
    </div>
</template>

<style scoped>
</style>