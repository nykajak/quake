<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import SubjectCard from '../subject/components/SubjectCard.vue';
    import AdminChapterScoreWidget from './AdminChapterScoreWidget.vue';
    import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
    import { Doughnut } from 'vue-chartjs'

    ChartJS.register(ArcElement, Tooltip, Legend)

    const props = defineProps(['uid','sid'])
    const subject = ref(null);

    const correctResponses = ref(null);
    const wrongResponses = ref(null);

    const attemptedQuestions = ref(null);
    const unattemptedQuestions = ref(null);

    const color1 = window.getComputedStyle(document.body).getPropertyValue('--tertiary-color');
    const color2 = window.getComputedStyle(document.body).getPropertyValue('--error-color');

    async function fetchSubject(){
        try{
            let res = await api.get(`/admin/subjects/${props.sid}`);
            subject.value = res.data.payload;
        }

        catch(err){
            console.log(err);
            return -1
        }
    }

    async function fetchStats(){
        try{
            let res;
            res = await api.get(`/admin/scores/users/${props.uid}/subjects/${props.sid}`)
            correctResponses.value = res.data.correct
            wrongResponses.value = res.data.count - res.data.correct
            console.log(res.data)

            res = await api.get(`/admin/scores/users/${props.uid}/subjects/${props.sid}/coverage`)
            attemptedQuestions.value = res.data.attempted
            unattemptedQuestions.value = res.data.count - res.data.attempted
            console.log(res.data)
        }
        catch(err){
            console.log(err);
        }
    }
    
    fetchSubject();
    fetchStats();
</script>

<template>
    <template v-if="subject">
        <SubjectCard :subject="subject" :active="true"/>

        <div class="d-flex align-items-center justify-content-center w-100 mt-4">
            <div class="d-flex justify-content-around w-75">
                <div v-if="correctResponses + wrongResponses !== 0" class="d-flex flex-column align-items-center">
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

                <div v-else>
                    No responses yet!
                </div>
    
                <div v-if="attemptedQuestions + unattemptedQuestions !== 0" class="d-flex flex-column align-items-center">
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

        <div v-if="subject.chapters" class="chapters">
            <div class="d-flex flex-column align-items-start m-2 w-100" v-for="chapter in subject.chapters">
                <AdminChapterScoreWidget :key="chapter.id" :uid='props.uid' :sid='props.sid' :cid='chapter.id'/>
            </div>
        </div>
    
    </template>
</template>

<style scoped>
.chapters{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1em;
    margin-top: 1.5em;
    flex-grow: 1;
    border-top: 1px solid light-dark(var(--dark-color),var(--light-color));
}
</style>