<script setup>
    import { api } from '@/api';
    import { defineProps, ref } from 'vue';

    const props = defineProps(['uid']);
    const user = ref([]);
    const loading = ref(false);

    async function fetchUsers(){
        loading.value = true;
        let res = await api.get(`/admin/users/${props.uid}`);
        loading.value = false;
        return res.data.payload
    }

    fetchUsers().then(data => {
        console.log(data);
        user.value = data;
    })
</script>

<template>
    <div v-if="loading == false">
        <div class="user-card-div">
            <div class="profile-div">

            </div>

            <div class="info-div">
                <h3>{{ user.name }}</h3>
                <div class="email-div">{{user.email}}</div>
            </div>
        </div>
    </div>

    <div v-else>
        Loading......
    </div>
</template>

<style scoped>
.results-div{
    margin-top: 3em;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}

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