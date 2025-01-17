<script setup>
import { defineProps } from 'vue';
import { RouterLink } from 'vue-router';
const props = defineProps(['user','active']);
</script>

<template>
    <div class="">
        <div class="d-flex flex-column align-items-center user-card-div">
            <div class="profile-div">
    
            </div>
    
            <div class="info-div">
                <h1 v-if="active == true">
                    <RouterLink :to="'users/'+user.id">
                        {{ props.user.name }}
                    </RouterLink>
                </h1>
                <h1 v-else>
                    {{ props.user.name }}
                </h1>
                <div class="email-div">{{props.user.email}}</div>
            </div>
        </div>
    </div>
</template>

<style scoped>

.user-card-div{
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
    font-size: 1.5em;
}
</style>