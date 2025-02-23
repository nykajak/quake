<script setup>
    import { api } from '@/api';
    import { onUpdated, ref } from 'vue';

    import { useRoute, useRouter } from 'vue-router';
    import { useTimer } from '@/timer';
    
    import QuizQuestion from './QuizQuestion.vue';
    import QuizNavigation from './QuizNavigation.vue';
    import Loader from '@/components/Loader.vue';

    const props = defineProps(['sid','cid','quiz_id','question_id'])
    const route = useRoute();
    const router = useRouter();

    let {time} = useTimer(300);

    function formatTime(time){
        if (time > 0){
            return `${Math.floor(time / 60)}  minutes and ${time % 60} seconds left!`;
        }
        else{
            return `You are out of time!`
        }
    }

    let questions = ref([]);

    async function fetchQuestions(){
        let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`);
        
        // let dated = res.data.quiz.dated;
        // let startDate = new Date(dated.year, dated.month, dated.day, dated.hour, dated.minute)
        // let endDate = new Date(startDate);
        // endDate.setMinutes(startDate.getMinutes() + res.data.quiz.duration);
        // let current = new Date();

        // console.log(current.getTime())
        // console.log(startDate.getTime())
        // console.log(endDate.getTime())
        // if (){
        //     console.log("Can attempt!")
        // }
        // else if (current.getTime() < startDate.getTime()){
        //     console.log("Has not started")
        // }
        // else{
        //     console.log("Quiz expired")
        // }

        questions.value = res.data.payload.map((x)=>{
            let y = {...x, 'sid':props.sid, 'cid':props.cid, 'quiz_id':props.quiz_id}
            return y;
        });
    }

    fetchQuestions()

    onUpdated(() =>{
        if (time.value <= 0){
            router.push({
                "path": `/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`
            })
        }
    })
</script>

<template>
    <template v-if="questions && questions[props.question_id - 1]">
        <div class="d-flex justify-content-end p-2">
            {{formatTime(time)}}
        </div>
        <QuizQuestion :question="questions[props.question_id - 1]" :index="props.question_id" :length="questions.length"/>
        <QuizNavigation :length="questions.length"/>
    </template>
    <Loader v-else/>
</template>

<style scoped>
</style>