<script setup>
    
    import Accuracy from './components/Accuracy.vue'
    import Coverage from './components/Coverage.vue'

    import { RouterLink } from 'vue-router'
    import Loader from '@/components/Loader.vue'

    import { ref } from 'vue'
    import { api } from '@/api'

    const props = defineProps(['uid','sid','cid','active'])

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
            correctResponses.value = res.data.correct_count
            wrongResponses.value = res.data.response_count - res.data.correct_count
            attemptedQuestions.value = res.data.seen_count
            unattemptedQuestions.value = res.data.question_count - res.data.seen_count
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
            <RouterLink v-if="props.active" :to="`${props.sid}/chapters/${chapter.id}`">
                {{chapter.name}}
            </RouterLink>

            <template v-else>
                {{chapter.name}}
            </template>
        </h2>
        <div class="d-flex w-75 justify-content-between">
            <Accuracy :correct-responses="correctResponses" :wrong-responses="wrongResponses" :color1="color1" :color2="color2"/>
            <Coverage :attempted-questions="attemptedQuestions" :unattempted-questions="unattemptedQuestions" :color1="color1" :color2="color2" />
        </div>
    </div>
<Loader v-else/>
</template>

<style scoped>
</style>