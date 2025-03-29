<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';
    import { useRoute, useRouter } from 'vue-router';

    import Loader from '@/components/Loader.vue';
    import PaginationToolBar from '@/components/PaginationToolBar.vue';

    const route = useRoute();
    const router = useRouter();
    const requests = ref(null);
    const errorMessage = ref(null);
    const pages = ref(null);

    async function rejectResponse(uid,sid){
        let res = await api.delete(`/admin/enrolled/users/${uid}/subjects/${sid}`);
        router.go(0);
    }

    async function acceptResponse(uid,sid){
        let res = await api.post(`/admin/enrolled/users/${uid}/subjects/${sid}`);
        router.go(0);
    }

    async function fetchRequests(){
        try{
            let page = route.query.page ?? 1;
            let per_page = route.query.per_page ?? 5;
            console.log(page,per_page)
            let res = await api.get(`/admin/enrolled/requests?page=${page}&per_page=${per_page}`)
            if (res.data.payload.length > 0){
                requests.value = res.data.payload;
                pages.value = res.data.pages;
            }
            else{
                errorMessage.value = "No pending requests!"
            }
        }
        catch(err){
            if (err.response && err.response.status){
                if(err.response.status == 400){
                    errorMessage.value = err.response.data.msg;
                }
                // Page not found error
                else if(err.response.status == 404){
                    errorMessage.value = "Page not found!";
                }
                else{
                    errorMessage.value = err.data ?? 'Unforeseen error!';
                }
            }
            else{
                errorMessage.value = 'Unforeseen error!';
                console.log(err)
            }
        }
    }
    fetchRequests()
</script>

<template>
    <div v-if="requests" class="d-flex flex-column flex-grow-1 mt-4 align-items-center">

        <div v-if="requests.length == 0">
            <h3>
                No requests pending!
            </h3>
        </div>
        <template v-else>
            <h3>
                Viewing enrollment requests!
            </h3>
            <div class="request-div" v-for="r in requests">
                <div class="header-div">
                    <div class="username-div">
                        Username: {{ r.user.name }} 
                    </div>
                    <div class="subject-div">
                        Subject: {{ r.subject.name }}
                    </div>
                </div>
                
                <div class="mt-2">
                    <h4>Confirm action?</h4>
                </div>
                <div class="options-div">
                    <button class="accept-button" @click="async () => {
                        await acceptResponse(r.user.id,r.subject.id);
                    }">
                        Accept Enrollment
                    </button>
                    <button class="reject-button" @click="async () => {
                        await rejectResponse(r.user.id,r.subject.id);
                    }">
                        Reject Enrollment
                    </button>
                </div>
            </div>
            <PaginationToolBar :num-pages="pages"/>
        </template>
    </div>

    <Loader v-if="requests == null && errorMessage == null"/>

    <div v-if="errorMessage" class="d-flex flex-column flex-grow-1 mt-4 align-items-center ">
        <RouterLink :to="'/admin'">
            <h2>
                Back to dashboard
            </h2>
        </RouterLink>
        <h2>
            {{ errorMessage }}
        </h2>
    </div>
</template>

<style scoped>
.header-div div{
    padding: 1em;
    color: var(--light-color);
}

.header-div{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
    background-color: var(--primary-color);
}

.request-div{
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1em;
    padding-bottom: 1em;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.options-div{
    display: flex;
    width: 75%;
    justify-content: space-around;
    margin-top: 0.5em;
}

.options-div button{
    padding: 0.5em;
}

.accept-button{
    display: flex;
    border: none;
    background-color: var(--secondary-color);
    color: var(--light-color);
}

.reject-button{
    display: flex;
    border: none;
    background-color: var(--error-color);
    color: var(--light-color);
}
</style>