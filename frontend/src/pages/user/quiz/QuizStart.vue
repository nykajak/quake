<script setup>
    import { RouterLink } from 'vue-router';
    const props = defineProps(['sid','cid','qid'])
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 align-items-center justify-content-center">
        <h3>
            <RouterLink :to="`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}/questions/1`">
                Start quiz now!
            </RouterLink>
        </h3>
    </div>
</template>

<style scoped>
</style>
