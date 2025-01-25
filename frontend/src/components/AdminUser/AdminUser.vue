<script setup>
    import { defineProps, ref } from 'vue';
    import { useRouter } from 'vue-router';
    
    import { api } from '@/api';

    import UserCard from './UserCard.vue';
    import Loader from '../Utility/Loader.vue';

    const router = useRouter();
    const props = defineProps(['uid']);
    
    const user = ref(null);
    const loading = ref(false);
    const ready = ref(false);

    async function fetchUsers(){
        try{
            loading.value = true;
            let res = await api.get(`/admin/users/${props.uid}`);
            loading.value = false;
            return res.data.payload
        }

        catch(err){
            loading.value = false;
            router.push({"name":"NotFound"})
            return -1
        }
    }
    
    fetchUsers().then(data => {
        if (data != -1){
            user.value = data;
            ready.value = true;
        }
    })
</script>

<template>
    <div v-if="loading == false && ready == true" class="d-flex flex-row flex-grow-1 mt-4">
        <div class="user-card">
            <UserCard :user="user" :active="false"/>
        </div>

        <div class="user-info">
            <h2 class="heading">Subjects</h2>
            <div class="d-flex flex-column w-100 align-items-center">
                <div class="subject-info" v-for="subject in user.subjects">
                    <div>
                        <h5 class="subject-heading">{{ subject.name }}</h5>
                    </div>
                    <div>
                        <h5>
                            <button class="dropdown">	
                                &#9656;
                            </button>
                        </h5>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>
.user-card{
    display: flex;
    flex-direction: column;
    min-width: 25%;
    border-top: 1px solid light-dark(var(--dark-color),var(--light-color));
    border-right: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.subject-info{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: 1em;
    width: 90%;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.user-info{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 75%;
    padding-top: 1em;
    border-top: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.subject-heading{
    font-size: 2em;
    padding-right: 0.3em;
}
.heading{
    color: var(--secondary-color);
}
.dropdown{
    display: flex;
    color: var(--secondary-color);
    background-color: rgba(1,1,1,0);
    border: none;
    font-size: 2em;
}
</style>