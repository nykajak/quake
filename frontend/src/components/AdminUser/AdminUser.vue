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
        <div class="d-flex flex-column border w-25">
            <UserCard :user="user" :active="false"/>
        </div>

        <div class="d-flex flex-column align-items-center w-75 border pt-3">
            <h2 class="heading">Subjects</h2>
            <div class="d-flex w-100 justify-content-center">
                <div class="d-flex flex-row align-items-center p-3 w-100 justify-content-center border" v-for="subject in user.subjects">
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
    background-color: light-dark(var(--light-color),var(--dark-color));
    border: none;
    font-size: 2em;
}
</style>