<script setup>
    import { useRoute } from 'vue-router';
    import Pagination from './Pagination.vue';
    import PerPage from './PerPage.vue';

    const props = defineProps(['numPages'])
    const route = useRoute();
</script>

<template>
    <div class="d-flex justify-content-center gap-2">
        <div>
            <Pagination :pages="numPages" :url="route.fullPath"/>
        </div>
        <PerPage/>
    </div>
</template>

<style scoped>
</style>