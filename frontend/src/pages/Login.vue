<script setup>
import { ref } from 'vue';
import { useRouter, RouterLink } from 'vue-router'

import { api } from '@/api';

import Header from '@/components/Header/Header.vue';

const router = useRouter()
const LoginMsg = ref("");
const LoginStatus = ref(0);

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

</script>

<template>
    <Header></Header>
    
    <div class="content">
        <div class="content-container">
            <div class="img-div d-flex">
                
            </div>
            
            <div class="login-div d-flex">
                <form @submit.prevent="validateForm">
                    <div class="form-div form-info-div">
                        <h3 class="text-center">Welcome back!</h3>
                        <p class="text-center">
                            <span class="redirect">Don't have an account yet? <RouterLink class="link" to="/register"><strong> Register </strong></RouterLink></span>
                        </p>
                    </div>
                    <div :class="{'form-div':true, 'form-error-div':LoginStatus === 0 && LoginMsg !== '', 'form-success-div':LoginStatus === 1}">
                        <input type="text" name="username" placeholder="Username" required>
                    </div>
            
                    <div :class="{'form-div':true, 'form-error-div':LoginStatus === 0 && LoginMsg !== '', 'form-success-div':LoginStatus === 1}">
                        <input type="password" name="password" placeholder="Password" required>
                    </div>
                
                    <div v-if="LoginMsg!==''" :class="['form-div',LoginStatus == 0 ? 'error-div' : 'success-div']">
                        {{LoginMsg}}
                    </div>
            
                    <div class="form-div">
                        <button type="submit">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

</template>

<style scoped>

.content{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.content-container {
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    height: 100%;
}

.img-div {
    display: flex;
    height: 100%;
    width: 100%;
    flex-shrink: 1;
    background-image: linear-gradient(to bottom right, var(--primary-color),  var(--secondary-color));
}

.login-div{
    display: flex;
    flex-shrink: 2;
    height: 100%;
    width: 100%;
    justify-content: center;
    align-items: center;
    border-right: 1px solid light-dark(var(--dark-color),var(--light-color));
}

form {
    padding: 10px;
    margin: 2px;
    width: 100%;
    min-width: fit-content;
}

.form-div {
    display: flex;
    margin: 0.75rem;
}

.form-div h3{
    font-size: 3.5em;
    color: var(--secondary-color);
}

.form-div .redirect{
    font-size: 0.9em;
    color: var(--contrast-color);
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

.link {
    color: var(--secondary-color);
}

.link:hover {
    color: var(--primary-color);
}

</style>