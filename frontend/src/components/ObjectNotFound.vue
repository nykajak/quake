<script setup>
    
</script>

<template>
    <div id="not-found-div">
        <h1>
            <slot></slot>
        </h1>
    </div>
</template>

<style scoped>
#not-found-div{
    display: flex;
    justify-content: center;
    color: var(--secondary-color);
}
</style>