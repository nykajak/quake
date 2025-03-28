<script setup>
    
    import Accuracy from './components/Accuracy.vue'
    import Coverage from './components/Coverage.vue'

    import ChapterCard from '../chapter/components/ChapterCard.vue'

    import { ref } from 'vue'
    import { api } from '@/api'

    const props = defineProps(['uid','sid','cid','active'])

    const correctResponses = ref(null);
    const wrongResponses = ref(null);
    const unknownResponses = ref(10);

    const attemptedQuestions = ref(null);
    const unattemptedQuestions = ref(null);
    const unknownQuestions = ref(10);

    const chapter = ref(null);
    const errorMessage = ref(null);

    async function fetchChapter(){
        try{
            let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}`)
            chapter.value = res.data.payload
        }
        catch(err){
            if (err.response && err.response.status){
                // Chapter not found error
                if(err.response.status == 404){
                    errorMessage.value = 'No such chapter!';
                }
                else{
                    errorMessage.value = 'Unforeseen error!';
                    console.log(err.response);
                }
            }
            else{
                errorMessage.value = 'Unforeseen error!';
                console.log(err)
            }
        }
    }


    async function fetchChapterStats(){
        try{
            let res;
            res = await api.get(`/admin/scores/users/${props.uid}/subjects/${props.sid}/chapters/${props.cid}`)
            correctResponses.value = res.data.correct_count
            wrongResponses.value = res.data.response_count - res.data.correct_count

            if (correctResponses.value + wrongResponses.value > 0){
                unknownResponses.value = 0;
            }

            attemptedQuestions.value = res.data.seen_count
            unattemptedQuestions.value = res.data.question_count - res.data.seen_count

            if (attemptedQuestions.value + unattemptedQuestions.value > 0){
                unknownQuestions.value = 0;
            }
        }
        catch(err){
            console.log(err);
        }
    }

    Promise.all([fetchChapter(),fetchChapterStats()])

</script>

<template>
    <div class="d-flex flex-column w-100 justify-content-between align-items-center">
        <ChapterCard v-if="chapter" :chapter="chapter"/>
        <template v-else>
            <ChapterCard :chapter="{
                'id': 0,
                'name':'Loading...  ',
            }"/>
        </template>

        <div class="d-flex w-75 justify-content-between">
            <Accuracy :data="[correctResponses,wrongResponses,unknownResponses]"/>
            <Coverage :data="[attemptedQuestions,unattemptedQuestions,unknownQuestions]"/>
        </div>
    </div>
</template>

<style scoped>
</style>