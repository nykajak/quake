<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';
    
    const props = defineProps(['sid','cid'])
    const quizes = ref([]);

    async function fetchQuizes(){
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes`);
        quizes.value = res.data.payload;
    }
    
    fetchQuizes();
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 mt-3">
        <div class="d-flex flex-column align-items-center">
            <div>
                <h3>
                    Linear Algebra
                </h3>
            </div>
            <div>
                <h1>
                    Logic Gates
                </h1>
            </div>
        </div>
        <div class="results-div">
            <div class="result-obj" v-for="quiz in quizes">
                <div>
                    <h4>
                        {{quiz.description}}
                    </h4>
                </div>
                <div class="d-flex flex-column align-items-center">
                    <p>
                        Start time: {{quiz.dated}}
                        <br>
                        Duration: {{quiz.duration}}
                    </p>    
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.result-obj{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5em;
}

.results-div{
    display: flex;
    flex-direction: column;
    margin-top:2em;
    gap:1em;
}

</style>