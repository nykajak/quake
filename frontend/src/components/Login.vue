<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()
async function validateForm(e){
    try{
        let res = await api.post("/login",new FormData(e.target));
        LoginMsg.value = res.data.msg;
        LoginStatus.value = 1;
        router.push({"name":"home"})
    }
    catch(err){
        LoginMsg.value = err.response.data.msg;
        LoginStatus.value = 0;
    }
}

const LoginMsg = ref("");
const LoginStatus = ref(0);

</script>

<template>
    <form @submit.prevent="validateForm">
        <div class="form-div form-info-div">
            <h3 class="text-center">Welcome back!</h3>
            <p class="text-center">
                Login with your credentials to continue your learning journey.
                <br>
                Don't have an account yet? <RouterLink to="/register"> Register </RouterLink>
            </p>
        </div>
        <div :class="{'form-div':true, 'form-error-div':LoginStatus === 0 && LoginMsg !== '', 'form-success-div':LoginStatus === 1}">
            <input type="text" name="username" placeholder="Username">
        </div>

        <div :class="{'form-div':true, 'form-error-div':LoginStatus === 0 && LoginMsg !== '', 'form-success-div':LoginStatus === 1}">
            <input type="password" name="password" placeholder="Password">
        </div>
    
        <div v-if="LoginMsg!==''" :class="['form-div',LoginStatus == 0 ? 'error-div' : 'success-div']">
            {{LoginMsg}}
        </div>

        <div class="form-div">
            <button type="submit">Login</button>
        </div>
    </form>
</template>

<style scoped>
form {
    padding: 10px;
    margin: 2px;
    border: 2px solid light-dark(var(--dark-color),var(--light-color));
    width: 75%;
}

.form-div {
    display: flex;
    margin: 0.75rem;
}

.form-error-div{
    border: 1px solid var(--error-color);
}

.form-success-div{
    border: 1px solid var(--tertiary-color);
}


.error-div{
    color: var(--error-color);
}

.success-div{
    color: var(--tertiary-color);
}


.form-info-div {
    flex-direction: column;
}

.form-div input {
    display: flex;
    flex-grow: 1;
    height: 2.5em;
    padding-left: 0.5em;
}

.form-div input:focus::placeholder{
    opacity: 0;
}

.form-div button {
    display: flex;
    width: 100%;
    height: 2em;
    justify-content: center;
    align-items: center;
    background-color: var(--secondary-color);
    color: var(--light-color);
    border: none;
}


</style>