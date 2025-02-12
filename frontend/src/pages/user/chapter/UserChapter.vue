<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';
    
    const props = defineProps(['sid','cid'])
    const chapter = ref({
        "name": "Chapter"
    });
    const quizes = ref([]);

    async function fetchQuizes(){
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}`);
        console.log(res.data.payload)
        quizes.value = res.data.payload.quizes;
        chapter.value = res.data.payload;
    }
    
    fetchQuizes();
</script>

<template>
    <div class="d-flex flex-column flex-grow-1 mt-3">
        <div class="d-flex flex-column align-items-center">
            <div>
                <h3>
                    {{chapter.subject.name}}
                </h3>
            </div>
            <div>
                <h1>
                    {{chapter.name}}
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
                    <p class="text-center">
                        Start time: {{ quiz.dated.day }}-{{ quiz.dated.month }}-{{ quiz.dated.year }}, at {{ quiz.dated.hour }}:{{ quiz.dated.minute }}
                        <br>
                        Duration: {{quiz.duration}} minutes
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