<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRouter, RouterLink } from 'vue-router'
import Header from '@/components/Header.vue';

const router = useRouter()
async function validateForm(e){
    try{
        let res = await api.post("/register",new FormData(e.target));
        RegisterMsg.value = res.data.msg;
        RegisterStatus.value = 1;
        router.push({"name":"home"})
    }
    catch(err){
        console.log(err)
        RegisterMsg.value = err.response.data.msg;
        RegisterStatus.value = 0;
    }
}

const RegisterMsg = ref("");
const RegisterStatus = ref(0);

</script>

<template>
    <Header></Header>

    <div class="content-container">
        <div class="img-div">
    
        </div>

        <div class="register-div d-flex">
            <form @submit.prevent="validateForm">
                <div class="form-div form-info-div">
                    <h3 class="text-center">Hello there!</h3>
                    <p class="text-center">
                        <span class="redirect">
                            Already have an account? <RouterLink class="link" to="/login"> <strong> Login </strong> </RouterLink>
                        </span>
                    </p>
                </div>
        
                <div :class="{'form-div':true, 'form-error-div':RegisterStatus === 0 && RegisterMsg !== '', 'form-success-div':RegisterStatus === 1}">
                    <input type="text" name="username" placeholder="Username">
                </div>
        
                <div :class="{'form-div':true, 'form-error-div':RegisterStatus === 0 && RegisterMsg !== '', 'form-success-div':RegisterStatus === 1}">
                    <input type="email" name="email" placeholder="Email">
                </div>
        
                <div :class="{'form-div':true, 'form-error-div':RegisterStatus === 0 && RegisterMsg !== '', 'form-success-div':RegisterStatus === 1}">
                    <input type="password" name="password" placeholder="Password">
                </div>
        
                <div :class="{'form-div':true, 'form-error-div':RegisterStatus === 0 && RegisterMsg !== '', 'form-success-div':RegisterStatus === 1}">
                    <input type="password" name="confirm" placeholder="Confirm password">
                </div>
        
                <div v-if="RegisterMsg!==''" :class="['form-div',RegisterStatus == 0 ? 'error-div' : 'success-div']">
                    {{RegisterMsg}}
                </div>
        
        
                <div class="form-div">
                    <button type="submit">Register</button>
                </div>
            </form>
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

.register-div{
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