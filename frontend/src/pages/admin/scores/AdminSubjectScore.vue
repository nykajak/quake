<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import SubjectCard from '../subject/components/SubjectCard.vue';
    import AdminChapterScoreWidget from './AdminChapterScoreWidget.vue';
    import Accuracy from './components/Accuracy.vue';
    import Coverage from './components/Coverage.vue';

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
                <Accuracy :correct-responses="correctResponses" :wrong-responses="wrongResponses" :color1="color1" :color2="color2"/>
                <Coverage :attempted-questions="attemptedQuestions" :unattempted-questions="unattemptedQuestions" :color1="color1" :color2="color2" />
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