<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRouter,useRoute } from 'vue-router';
import Header from './Header.vue';

const router = useRouter()
const route = useRoute()
async function sendReq(){
    
    try{
        let res = await api.get("/");
        return res.data.msg
    }
    catch(err){
        console.log(err)
        return "Something went wrong!"
    }
}

async function sendLogout(){
    let res = await api.post("/logout");
    router.push({"name":"login"})
}

const message = ref("")
sendReq().then(data => {
    message.value = data;
})

const page = ref(0);

</script>

<template>
    <Header></Header>
    <div class="content">
        <div class="jumbotron jumbotron-fluid">
            <div class="container-fluid marketing text-center">
                <h1 class="display-1">Quake</h1>
                <p class="lead">
                    Your one stop solution for all your quizzing needs!
                </p>

                <div class="slideshow">
                    <div class="slideshow-control-div">
                        <button class="slideshow-control" @click="page=(page+2)%3">&lt;</button>
                    </div>
                    
                    <div v-if="page==0" class="slideshow-item">
                        <div class="slideshow-header">
                            <div class="slideshow-symbol">
                                <h3>?</h3>
                            </div>
                            <div class="slideshow-question">
                                <h3>Question 1</h3>
                            </div>
                        </div>
                        <div class="slideshow-answer">
                            <p>
                                Answer to question 1 given here!
                            </p>
                        </div>
                    </div>
                    
                    <div v-else-if="page==1" class="slideshow-item">
                        <div class="slideshow-header">
                            <div class="slideshow-symbol">
                                <h3>?</h3>
                            </div>
                            <div class="slideshow-question">
                                <h3>Question 2</h3>
                            </div>
                        </div>
                        <div class="slideshow-answer">
                            <p>
                                Answer to question 2 given here!
                            </p>
                        </div>
                    </div>
                    
                    <div v-else-if="page==2" class="slideshow-item">
                        <div class="slideshow-header">
                            <div class="slideshow-symbol">
                                <h3>?</h3>
                            </div>
                            <div class="slideshow-question">
                                <h3>Question 3</h3>
                            </div>
                        </div>
                        <div class="slideshow-answer">
                            <p>
                                Answer to question 3 given here!
                            </p>
                        </div>
                    </div>
                    
                    <div class="slideshow-control-div">
                        <button class="slideshow-control" @click="page=(page+1)%3">&gt;</button>
                    </div>
                </div>
            </div>
        </div>
        <h3>{{message}}</h3>
        <button @click="sendLogout">Logout</button>
    </div>
</template>

<style scoped>
.content{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.slideshow{
    width: 40%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: stretch;
}

.slideshow-control{
    display: flex;
    height: 100%;
    align-items: center;
}

.slideshow-item{
    width: 100%;
    justify-content: center;
    align-items: center;
}

.slideshow-header{
    display: flex;
    flex-direction: row;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.slideshow-symbol{
    flex-grow: 1;
}

.slideshow-question{
    flex-grow: 5;
    background-color: light-dark(var(--light-color),var(--secondary-color));
}

.slideshow-answer{
    display: flex;
    flex-direction: column;
}

.marketing {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1em;
    background-image: linear-gradient(to bottom right,  light-dark( var(--primary-color),var(--dark-color)),  light-dark( var(--secondary-color),var(--contrast-color)));
}
</style>