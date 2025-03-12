<script setup>
    
    import ChapterCard from '../chapter/components/ChapterCard.vue'
    import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
    import { Doughnut } from 'vue-chartjs'

    import { ref } from 'vue'
    import { api } from '@/api'

    const props = defineProps(['uid','sid','cid'])
    
    ChartJS.register(ArcElement, Tooltip, Legend)

    const correctResponses = ref(null);
    const wrongResponses = ref(null);

    const attemptedQuestions = ref(null);
    const unattemptedQuestions = ref(null);

    const color1 = window.getComputedStyle(document.body).getPropertyValue('--tertiary-color');
    const color2 = window.getComputedStyle(document.body).getPropertyValue('--error-color');

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
            correctResponses.value = res.data.correct
            wrongResponses.value = res.data.count - res.data.correct
            console.log(res.data)

            res = await api.get(`/admin/scores/users/${props.uid}/subjects/${props.sid}/chapters/${props.cid}/coverage`)
            attemptedQuestions.value = res.data.attempted
            unattemptedQuestions.value = res.data.count - res.data.attempted
            console.log(res.data)
        }
        catch(err){
            console.log(err);
        }
    }

    fetchChapter()
    fetchChapterStats()

</script>

<template>
    <div v-if="chapter" class="d-flex flex-column w-100 justify-content-between align-items-center p-5">
        <h2 class="d-flex flex-grow-1 mb-3">
            {{chapter.name}}
        </h2>
        <div class="d-flex w-50 justify-content-between">
            <div v-if="!(correctResponses + wrongResponses == 0)" class="d-flex flex-column align-items-center">
                <Doughnut :data="{
                    labels: ['correct','incorrect'],
                    datasets: [
                        {
                            backgroundColor: [color1, color2],
                            data: [correctResponses, wrongResponses]
                        }
                    ]
                }" :options="{
                    'responsive': true,
                    maintainAspectRatio: true,
                }" />
                <div class="d-flex mt-2">
                    <h3>Attempt summary</h3>
                </div>
            </div>

            <div class="d-flex w-50 justify-content-between" v-else>
                No Responses yet!
            </div>
    
            <div v-if="!(attemptedQuestions + unattemptedQuestions == 0)" class="d-flex flex-column align-items-center">
                <Doughnut :data="{
                    labels: ['attempted','unattempted'],
                    datasets: [
                        {
                            backgroundColor: [color1, color2],
                            data: [attemptedQuestions, unattemptedQuestions]
                        }
                    ]
                }" :options="{
                    'responsive': true,
                    maintainAspectRatio: true,
                }" />
                <div class="d-flex mt-2">
                    <h3>Coverage of questions</h3>
                </div>
            </div>

            <div v-else>
                No questions yet!
            </div>
    
        </div>
    </div>
</template>

<style scoped>
</style>