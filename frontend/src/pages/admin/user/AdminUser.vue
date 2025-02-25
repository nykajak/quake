<script setup>
    import { defineProps, ref } from 'vue';
    import { useRouter } from 'vue-router';
    
    import { api } from '@/api';

    import UserCard from './components/UserCard.vue';
    import Loader from '@/components/Loader.vue';

    const props = defineProps(['uid']);
    
    const user = ref(null);
    const errorMessage = ref("")

    async function fetchUsers(){
        try{
            let res = await api.get(`/admin/users/${props.uid}`);
            user.value = res.data.payload;
        }

        catch(err){
            // Validation error for user not found
            if (err.status == 404){
                errorMessage.value = err.response.data.msg;
            }
            else{
                console.log(err);
            }
        }
    }
    
    fetchUsers()
</script>

<template>
    <div v-if="user || errorMessage" class="d-flex flex-row flex-grow-1 mt-4">
        <template v-if="user">
            <!-- Display the user details -->
            <div class="user-card">
                <UserCard :user="user" :active="false"/>
            </div>
            
            <!-- Display the user subject details -->
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
        </template>

        <div v-else class="error-div">
            {{ errorMessage }}
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>

.error-div{
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-top: 2rem;
    font-size: 2rem;
    width: 100%;
}

.user-card{
    display: flex;
    flex-direction: column;
    min-width: max(25%,fit-content);
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
    border-bottom: 1px solid light-dark(var(--dark-color),var(--light-color));
    border-top: 1px solid light-dark(var(--dark-color),var(--light-color));
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