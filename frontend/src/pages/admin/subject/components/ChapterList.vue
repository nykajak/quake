<script setup>
    import ChapterCard from '../../chapter/components/ChapterCard.vue';
    
    const props = defineProps(['chapters'])
</script>

<template>
    <div class="chapters">
        <h1 class="heading">Chapters</h1>
        <div class="d-flex flex-column align-items-center m-2" v-for="chapter in props.chapters">
            <ChapterCard :chapter="chapter" :active="1"></ChapterCard>
        </div>
    </div>
</template>

<style>
.chapters{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1em;
    flex-grow: 1;
    border-top: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.heading{
    color: var(--secondary-color);
    font-size: 3em;
}
</style>