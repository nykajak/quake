<script setup>
    import { api } from '@/api';
    import { ref } from 'vue';

    import { useRoute, useRouter } from 'vue-router';
    
    import QuizQuestion from './QuizQuestion.vue';
    import QuizNavigation from './QuizNavigation.vue';
    import Loader from '@/components/Loader.vue';

    const props = defineProps(['sid','cid','quiz_id','question_id'])
    const route = useRoute();
    const router = useRouter();


    function formatTime(time){
        if (time > 0){
            return `${Math.floor(time / 60)}  minutes and ${time % 60} seconds left!`;
        }
        else{
            return `You are out of time!`
        }
    }

    let questions = ref([]);
    let time = ref(null);

    async function fetchQuestions(){

        try{
            let res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`);
            questions.value = res.data.payload.map((x)=>{
                let y = {...x, 'sid':props.sid, 'cid':props.cid, 'quiz_id':props.quiz_id}
                return y;
            });
            time.value = res.data.time
        }
        catch(err){
            console.log(err);
            router.push({
                "path": `/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`
            })
        }
        
    }

    fetchQuestions().then((data)=>{
        time.value = data.res.time;
    })

    let interval_id = setInterval(() => {
        time.value -= 1;
        if (time.value <= 0){
            clearInterval(interval_id);
            router.push({
                "path": `/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`
            })
        }
    },1000)
</script>

<template>
    <template v-if="time && questions && questions[props.question_id - 1]">
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