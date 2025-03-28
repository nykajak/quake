<!-- Renders a button that navigates to another page! -->
<script setup>
import { useRouter } from 'vue-router';
    // Note: Replace props.text with slot based rendering
    const props = defineProps(['text','url','color','active'])
    const router = useRouter();
</script>

<template>
    <button :disabled="active === false" :class="['base-button',props.color+'-button'] " @click="router.push({
        'path': `${props.url}`
    })">
        {{ props.text }}
    </button>
</template>

<style scoped>
.base-button{
    display: flex;
    border: none;
    padding: 0.5em;
    color: var(--light-color);
}

.primary-button{
    background-color: var(--primary-color);
}

.secondary-button{
    background-color: var(--secondary-color);
}

.tertiary-button{
    background-color: var(--tertiary-color);
}

.error-button{
    background-color: var(--error-color);
}

</style>