<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';
    import { RouterLink } from 'vue-router';
    import NavButton from '@/components/NavButton.vue';

    const props = defineProps(['sid','cid','qid'])
    const quiz = ref(null);
    const active = ref(null);
    const accuracy = ref(null);
    const attempted = ref(null);

    async function fetchQuiz() {
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}`);
        quiz.value = res.data.payload
        active.value = res.data.active;
        if (res.data.count){
            accuracy.value = [res.data.correct, res.data.count]
        }
        if(res.data.attempted){
            attempted.value = res.data.attempted;
            console.log(attempted.value)
        }
    }
    fetchQuiz()
</script>

<template>
    <div v-if="quiz" class="d-flex flex-column flex-grow-1 align-items-center mt-3">
        <div class="d-flex flex-column align-items-center">
            <h1>
                {{quiz.description}}
            </h1>
            <p class="text-center">
                Start time: {{ quiz.dated.minute }}:{{ quiz.dated.hour }}, on {{ quiz.dated.day }}/{{ quiz.dated.month }}/{{ quiz.dated.year }}
                <br>
                Duration: {{ quiz.duration }} minutes
            </p>
        </div>

        <div class="d-flex justify-content-center" v-if="quiz">
            <div class="d-flex flex-column align-items-center" v-if="active === null">
                <h3>Quiz status: Expired</h3>
                <template v-if="attempted === null">
                    {{accuracy[0]}} questions correct out of {{accuracy[1]}}
                    <div class="mt-2">
                        <NavButton :color="'primary'" :text="`View responses!`" :url="`${props.qid}/responses`"/>
                    </div>
                </template>
                <template v-else>
                    Quiz not attempted!
                </template>
            </div>
            
            <div class="d-flex flex-column align-items-center" v-else-if="active === false">
                <h3>Quiz status: Pending</h3>
                <NavButton :active="false" :color="'primary'" :text="`Quiz yet to start!`" :url="`${props.qid}/questions/1`"/>
            </div>
            
            <div class="d-flex flex-column align-items-center" v-else-if="active === true">
                <NavButton :color="'primary'" :text="`Start quiz now!`" :url="`${props.qid}/questions/1`"/>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>
