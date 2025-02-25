<script setup>
    import { ref } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    
    import { api } from '@/api';
    
    import UserCard from './components/UserCard.vue';
    import Pagination from '@/components/Pagination.vue';
    import Loader from '@/components/Loader.vue';
    import PerPage from '@/components/PerPage.vue';

    const route = useRoute();
    const router = useRouter();

    const users = ref(null); // Stores the result of the search for users
    const numPages = ref(null); // Stores the number of pages found
    const username = ref(route.query.q ?? ''); // Stores the query string (starting chars of user)
    const errorMessage = ref(""); // Stores an error message if any

    async function fetchUsers(){
        try{
            // Current values from url or defaults (should be sensible defaults)
            let page = route.query["page"] ?? 1;
            let per_page = route.query["per_page"] ?? 5 ;
            let q = route.query["q"] ?? "";

            // API request made
            let res = await api.get(`/admin/users/?page=${page}&per_page=${per_page}&q=${q}`);
            numPages.value = res.data.pages
            users.value = res.data.payload
            errorMessage.value = ""
        }

        catch(err){
            // Validation error for page and per_page attributes
            if (err.status == 400){
                errorMessage.value = err.response.data.msg;
            }
            // Validation error for page not found
            else if (err.status == 404){
                errorMessage.value = err.response.data.msg;
            }
            else{
                console.log(err);
            }
        }
    }

    fetchUsers();
</script>

<template>
    <div v-if="users || errorMessage" class="d-flex flex-column flex-grow-1">
        <div class="d-flex flex-grow-1 flex-column align-items-center">

            <!-- Display the search bar -->
            <div class="d-flex flex-column user-sidebar w-25 justify-content-start align-items-center text-center">
                <h3>Querying users</h3>
                <div class="d-flex mb-2">
                    <PerPage/>
                    <input type="text" v-model="username" placeholder="Username">
                    <button class="query-button" @click="router.push({
                        'path': 'users',
                        'query': {
                            ...route.query,
                            'q': username,
                            'page': 1
                        }
                    })">Submit</button>
                </div>
            </div>

            <!-- Display search results -->
            <div v-if="users !== null && users.length > 0" class="d-flex flex-column w-75">
                <div class="d-flex flex-column flex-grow-1 justify-content-center">
                    <div class="results-div">
                        <template v-for="user in users">
                            <UserCard :user="user" :active="true"/>
                        </template>
                    </div>
                </div>
                
                <div class="d-flex justify-content-center">
                    <Pagination :pages="numPages" type="users"/>
                </div>
            </div>

            <div v-else-if="users !== null && users.length == 0" class="error-div">
                No users found!
            </div>

            <!-- Error message displaying div -->
            <div v-else class="error-div">
                {{ errorMessage }}
            </div>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>

.error-div{
    display: flex;
    flex-direction: column;
    margin-top: 2rem;
    font-size: 2rem;
}

.results-div{
    margin-top: 3em;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
}
.user-sidebar{
    margin-top: 1em;
}

.query-button{
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    background-color: var(--secondary-color);
    color: var(--light-color);
}

input {
    padding-left: 0.5em;
}
</style>