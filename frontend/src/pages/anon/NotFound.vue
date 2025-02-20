<script setup>
    import {useThemeStore} from "@/stores/theme.js"

    const themeStore = useThemeStore();
    document.body.style.colorScheme = themeStore.theme || "light";

    import { RouterLink } from "vue-router";
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 justify-content-center align-items-center">
        <h4>
            The page you are looking for does not exist :)
        </h4>

        <p>
            Check if the URL has been mispelled!
        </p>

        <RouterLink to="/">
            Return Home
        </RouterLink>
    </div>
</template>

<style scoped>
</style>