<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import Loader from '@/components/Loader.vue';
    import { RouterLink } from 'vue-router';
    
    const props = defineProps(['sid','cid'])
    const chapter = ref({
        "name": "Chapter"
    });
    const quizes = ref([]);

    async function fetchQuizes(){
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}`);
        quizes.value = res.data.payload.quizes;
        chapter.value = res.data.payload;
    }
    
    fetchQuizes();
</script>

<template>
    <div v-if="chapter && chapter.subject" class="d-flex flex-column flex-grow-1 mt-3">
        <div class="d-flex flex-column align-items-center">
            <div>
                <h3>
                    <RouterLink :to="`/user/subjects/${props.sid}`">
                        {{chapter.subject.name}}
                    </RouterLink>
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
                        <RouterLink :to="`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${quiz.id}`">
                            {{quiz.description}}
                        </RouterLink>
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

    <Loader v-else/>
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