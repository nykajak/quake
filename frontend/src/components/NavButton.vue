<script setup>
import { useRouter } from 'vue-router';

    const props = defineProps(['text','url','color'])
    const router = useRouter();
</script>

<template>
    <button :class="['base-button',props.color+'-button'] " @click="router.push({
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


.error-button{
    background-color: var(--error-color);
}

</style>