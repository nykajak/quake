<script setup>
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';

import {useThemeStore} from "@/stores/theme.js"

import Logout from '../Utility/Logout.vue';
import ToggleDark from '../Utility/ToggleDark.vue';

const themeStore = useThemeStore();
onMounted(() => {
    document.body.style.colorScheme = themeStore.theme || "light dark";
})

function toggle(){
    themeStore.toggle()
    document.body.style.colorScheme = themeStore.theme || "light dark";
}

</script>

<template>
    <div class="header-container">
        <div class="header-inner-div" id="logo-div">
            <h3 class="header-text">Quake</h3>
        </div>

        <div class="header-inner-div" id="link-div">
            <div class="nav-div">
                <RouterLink class="nav-link" to="/admin"><strong>Overview</strong></RouterLink>
            </div>
            <div class="nav-div">
                <RouterLink class="nav-link" to="/admin/users"><strong>Users</strong></RouterLink>
            </div>
            <div class="nav-div">
                <RouterLink class="nav-link" to="/admin/subjects"><strong>Subjects</strong></RouterLink>
            </div>
        </div>

        <div class="header-inner-div" id="utility-div">
            <button class="btn btn-default" @click="toggle()">
                <ToggleDark/>
            </button>
            <Logout/>
        </div>
    </div>
</template>

<style scoped>

.header-text {
    color: var(--secondary-color)
}

.header-container {
    display: flex;
    flex-direction: row;
    border-bottom: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.header-inner-div {
    display: flex;
    padding: 0.25em;
}

#link-div {
    flex-grow: 2;
    justify-content: end;
    align-items: center;
}

#logo-div {
    flex-grow: 5;
    min-width: fit-content;
}


.nav-div{
    display: flex;
    flex-grow: 1;
    justify-content: center;
    align-items: center;
}

.nav-link {
    color: var(--secondary-color);
}

.nav-link:hover {
    color: var(--primary-color);
}

</style>