<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import SubjectCard from '../subject/components/SubjectCard.vue';
    import ChapterCard from '../chapter/components/ChapterCard.vue';
    import Accuracy from './components/Accuracy.vue';
    import Coverage from './components/Coverage.vue';
    import NavButton from '@/components/NavButton.vue';

    const props = defineProps(['uid','sid'])
    const subject = ref(null);

    const correctResponses = ref(null);
    const wrongResponses = ref(null);
    const unknownResponses = ref(10);

    const attemptedQuestions = ref(null);
    const unattemptedQuestions = ref(null);
    const unknownQuestions = ref(10);

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

    Promise.all([fetchSubject(),fetchStats()])

</script>

<template>
    <SubjectCard v-if="subject" :subject="subject" :active="true"/>
    <template v-else>
        <SubjectCard :subject="{
            'id': 0,
            'name':'Loading...  ',
        }"/>
    </template>

    <div class="d-flex align-items-center justify-content-center w-100 mt-4">
        <div class="d-flex justify-content-around w-75">
            <Accuracy :data="[correctResponses,wrongResponses,unknownResponses]"/>
            <Coverage :data="[attemptedQuestions,unattemptedQuestions,unknownQuestions]"/>
        </div>
    </div>

    <div v-if="subject && subject.chapters" class="chapters">
        <div class="d-flex flex-column align-items-center mb-3 w-100" v-for="chapter in subject.chapters">
            <ChapterCard :chapter="chapter"/>
            <NavButton color="primary" text="View Score" :url="`${props.sid}/chapters/${chapter.id}`" />
        </div>
    </div>
    
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