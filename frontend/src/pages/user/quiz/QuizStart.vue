<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import NavButton from '@/components/NavButton.vue';
    import Loader from '@/components/Loader.vue';

    const props = defineProps(['sid','cid','qid'])
    const quiz = ref(null);
    const status = ref("pending");

    const correct_count = ref(null);
    const response_count = ref(null);
    const question_count = ref(null);

    async function fetchQuiz() {
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}`);
        quiz.value = res.data.payload
        
        let active = res.data.active;
        if (active == true){
            status.value = "ongoing";
        }
        
        if (res.data.correct_count && res.data.response_count && res.data.question_count){
            correct_count.value = res.data.correct_count
            response_count.value = res.data.response_count
            question_count.value = res.data.question_count
            status.value = "past";
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
            <div class="d-flex flex-column align-items-center" v-if="status === 'past'">
                <h3>Quiz status: Expired</h3>
                <div>
                        Total questions: {{ question_count }}
                </div>
                <div>
                    Attempted questions: {{ response_count }}
                </div>
                <div>
                    Correct questions: {{ correct_count }}
                </div>
                <div class="mt-2">
                    <NavButton :color="'primary'" :text="`View responses!`" :url="`${props.qid}/responses/1`"/>
                </div>
            </div>
            
            <div class="d-flex flex-column align-items-center" v-else-if="status === 'pending'">
                <h3>Quiz status: Pending</h3>
                <NavButton :active="false" :color="'primary'" :text="`Quiz yet to start!`" :url="`${props.qid}/questions/1`"/>
            </div>
            
            <div class="d-flex flex-column align-items-center" v-else-if="status === 'ongoing'">
                <NavButton :color="'primary'" :text="`Start quiz now!`" :url="`${props.qid}/questions/1`"/>
            </div>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>
</style>
