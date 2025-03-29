<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import NavButton from '@/components/NavButton.vue';
    import Loader from '@/components/Loader.vue';
    import { useRouter } from 'vue-router';

    const router = useRouter()
    const props = defineProps(['sid','cid','qid'])
    const quiz = ref(null);
    const status = ref("pending");

    const correct_count = ref(null);
    const response_count = ref(null);
    const question_count = ref(null);

    async function fetchQuiz() {
        let res;
        try{
            res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.qid}`);
        }
        catch(err){
            router.push({
                "path": `/user/subjects/${props.sid}/chapters/${props.cid}`
            });
            return
        }
        quiz.value = res.data.payload
        
        let active = res.data.active;
        if (active == true){
            status.value = "ongoing";
        }
        
        if (res.data.correct_count != null && res.data.response_count != null && res.data.question_count != null){
            correct_count.value = res.data.correct_count
            response_count.value = res.data.response_count
            question_count.value = res.data.question_count
            status.value = "past";
        }
    }
    fetchQuiz()
</script>

<template>
    <div v-if="quiz" class="d-flex flex-column flex-grow-1 align-items-center mt-3 w-100">
        <div class="d-flex flex-column align-items-center">
            <h1 class="headingText">
                {{quiz.description}}
            </h1>
            <p class="descriptionText text-center">
                Start time: {{ quiz.dated.hour }}:{{ quiz.dated.minute }}, on {{ quiz.dated.day }}/{{ quiz.dated.month }}/{{ quiz.dated.year }}
                <br>
                Duration: {{ quiz.duration }} minutes
            </p>
        </div>

        <div class="d-flex justify-content-center w-100" v-if="quiz">
            <div class="d-flex flex-column align-items-center w-100" v-if="status === 'past'">
                <h3 class="expiredStatus">Quiz status: Expired</h3>
                <div class="statsContainer">
                    <div class="statsElement">
                        <h4>
                            Total questions
                        </h4>
                        <p>
                            {{ question_count }}
                        </p>
                    </div>
                    <div class="statsElement">
                        <h4>
                            Attempted questions
                        </h4>
                        <p>
                            {{ response_count }}
                        </p>
                    </div>
                    <div class="statsElement">
                        <h4>
                            Correct questions
                        </h4>
                        <p>
                            {{ correct_count }}
                        </p>
                    </div>
                </div>
                <div class="mt-2">
                    <NavButton :color="'primary'" :text="`View responses!`" :url="`${props.qid}/responses/1`"/>
                </div>
            </div>
            
            <div class="d-flex flex-column align-items-center" v-else-if="status === 'pending'">
                <h3 class="pendingStatus">Quiz status: Pending</h3>
            </div>
            
            <div class="d-flex flex-column align-items-center" v-else-if="status === 'ongoing'">
                <h3 class="liveStatus">Quiz status: Live</h3>
                <NavButton :color="'primary'" :text="`Start quiz now!`" :url="`${props.qid}/questions/1`"/>
            </div>
        </div>
    </div>

    <Loader v-else/>
</template>

<style scoped>
.statsContainer{
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    width: 75%;
    margin-bottom: 2em;
}

.statsElement{
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 5px;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.statsElement h4{
    padding: 1em;
    border-radius: 5px;
    background-color: var(--primary-color);
    color: var(--light-color);
}

.statsElement p{
    font-size: 2em;
}

.expiredStatus{
    color: var(--error-color);
}

.pendingStatus{
    color: var(--tertiary-color);
}

.liveStatus{
    color: var(--secondary-color);
}

.headingText{
    color: var(--primary-color);
}

.descriptionText{
    color: var(--contrast-color);
}
</style>
