<script setup>
    import { useRouter, useRoute } from 'vue-router';
    
    const props = defineProps(['query_str'])
    const router = useRouter();
    const route = useRoute();
</script>

<template>
    <button class="query-button" @click="router.push({
        'path': 'subjects',
        'query': {
            ...route.query,
            'q': props.query_str,
            'page': 1
        }
    })">
        <slot></slot>
    </button>
</template>

<style scoped>
.query-button{
    border: none;
    background-color: var(--secondary-color);
    color: var(--light-color);
    padding: 0.5em;
}
</style>