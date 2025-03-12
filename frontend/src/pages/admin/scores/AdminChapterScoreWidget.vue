<script setup>
    
    import Accuracy from './components/Accuracy.vue'
    import Coverage from './components/Coverage.vue'

    import { RouterLink } from 'vue-router'

    import { ref } from 'vue'
    import { api } from '@/api'

    const props = defineProps(['uid','sid','cid'])

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
            <RouterLink :to="`${props.sid}/chapters/${chapter.id}`">
                {{chapter.name}}
            </RouterLink>
        </h2>
        <div class="d-flex w-50 justify-content-between">
            <Accuracy :correct-responses="correctResponses" :wrong-responses="wrongResponses" :color1="color1" :color2="color2"/>
            <Coverage :attempted-questions="attemptedQuestions" :unattempted-questions="unattemptedQuestions" :color1="color1" :color2="color2" />
        </div>
    </div>
</template>

<style scoped>
</style>