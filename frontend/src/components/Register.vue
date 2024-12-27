<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRouter } from 'vue-router'

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
    <form @submit.prevent="validateForm">
        <div class="form-div form-info-div">
            <h3>Hello there!</h3>
            <p>
                Register to start learning now!
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