<script setup>
    
    import { ref } from 'vue';
    import { api } from '@/api';
    import { useRouter } from 'vue-router';

    import StaticQuestion from '@/components/StaticQuestion.vue';
    import StaticOption from '@/components/StaticOption.vue';
    import QuizNavigation from '../quiz/components/QuizNavigation.vue';

    const router = useRouter()

    const props = defineProps(['sid','cid','quiz_id','question_id'])
    const marked = ref(null);
    const question = ref(null);
    const pages = ref(null);

    async function fetchQuestion(){
        let res;
        try{
            res = await api.get(`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}/questions/${props.question_id}`);
        }
        catch(err){
            router.push({
                "path": `/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`
            })
        }

        marked.value = res.data.payload;
        question.value = res.data.question;
        pages.value = res.data.num;
        if (res.data.time > 0){
            router.push({
                "path": `/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}`
            })
        }
    }
    fetchQuestion()
</script>

<template>
    <div v-if="question" class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <div class="question-container">
            <div v-if="marked == -1">
                Not attempted!
            </div>
            <StaticQuestion :index="props.question_id" :description="question.description"/>
        </div>

        <div class="option-container">
            <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                <template v-for="n in 4">
                    <StaticOption :marked="marked" :optionNo="n-1" :correctOption="question.correct" :option-text="question.options[n-1]" />
                </template>
            </div>
        </div>
    </div>

    <QuizNavigation :length="pages" :beforeSubmit="()=>{}" :current="props.question_id" :url="`/user/subjects/${props.sid}/chapters/${props.cid}/quizes/${props.quiz_id}/responses`"/>
</template>

<style scoped>
</style>