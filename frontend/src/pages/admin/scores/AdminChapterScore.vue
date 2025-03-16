<script setup>
    import AdminChapterScoreWidget from './AdminChapterScoreWidget.vue';

    const props = defineProps(['uid','sid','cid'])
</script>

<template>
    <AdminChapterScoreWidget :uid="props.uid" :sid="props.sid" :cid="props.cid" />
</template>

<style scoped>
</style>