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

</script>

<template>
    <div class="d-flex align-items-center">
        <select v-model="selected" class="dropdown-style">
            <option>1</option>
            <option>3</option>
            <option>5</option>
            <option>10</option>
        </select>
    </div>
</template>

<style scoped>
    .dropdown-style{
        width: 100%;
        padding: 0.2em;
        height: 2em;
        text-align: center;
    }
</style>