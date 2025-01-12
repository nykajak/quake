<script setup>

import { defineProps } from 'vue';
const props = defineProps(['intervalStart','intervalLength'])

import { useRouter, useRoute } from 'vue-router';
import { RouterLink } from 'vue-router';
const router = useRouter();
const route = useRoute();

</script>

<template>
    <div class="d-flex flex-row">
        <div class="p-2" v-for="n in intervalLength">
            <button @click="() => {
                router.push({path: '/admin/users', query : {
                'page': intervalStart + n - 1,
            }})
            }" :class="{current:intervalStart + n - 1 == (route.query.page ?? 1)}">
                {{ intervalStart + n - 1 }}
            </button>
        </div>
    </div>
</template>

<style scoped>
.current {
    color: var(--light-color);
    background-color: var(--secondary-color);
}
</style>