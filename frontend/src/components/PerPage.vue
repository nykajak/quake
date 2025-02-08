<script setup>

import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const route = useRoute();
const router = useRouter();
const selected = ref(route.query.per_page ?? 5);

watch(selected, (old,_new) => {
    router.push({
        "path": route.path,
        "query": {
            ...route.query,
            "page": 1,
            "per_page": old
        }
    })
})

console.log(route.query)
</script>

<template>
    <div class="d-flex">
        <select v-model="selected" class="w-100 p-1">
            <option>1</option>
            <option>3</option>
            <option>5</option>
            <option>10</option>
        </select>
    </div>
</template>

<style scoped>
</style>