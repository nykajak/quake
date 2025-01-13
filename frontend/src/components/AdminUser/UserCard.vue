<script setup>
import { defineProps } from 'vue';
import { RouterLink } from 'vue-router';
const props = defineProps(['user','active']);
</script>

<template>
    <div class="user-card-div">
        <div class="profile-div">

        </div>

        <div class="info-div">
            <h3 v-if="active == true">
                <RouterLink :to="'users/'+user.id">
                    {{ props.user.name }}
                </RouterLink>
            </h3>
            <h3 v-else>
                {{ props.user.name }}
            </h3>
            <div class="email-div">{{props.user.email}}</div>
        </div>
    </div>
</template>

<style scoped>

.user-card-div{
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-grow: 1;
    /* border: 1px solid light-dark(var(--dark-color),var(--light-color));
    border-radius: 0.5em;    */
    margin: 1em;    
    padding: 1em;
}

.profile-div{
    display: flex;
    width: 100px;
    height: 100px;
    border-radius: 100%;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    margin-bottom: 1em;
}

.info-div{
    display: flex;
    flex-direction: column;
    text-align: center;
    color: var(--secondary-color);
}

.email-div{
    color: var(--contrast-color);
}
</style>