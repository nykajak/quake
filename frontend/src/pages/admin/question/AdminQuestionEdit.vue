<script setup>
import { api } from '@/api';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import EditableOption from './components/EditableOption.vue';
import EditableQuestion from './components/EditableQuestion.vue';

const props = defineProps(['sid','cid','qid'])
const router = useRouter()

async function fetchQuestion(){
    let res = await api.get(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}`)
    return res.data.payload;
}

const qid = ref("")
const question = ref("");
const options = ref([])
const correctOption = ref(-1);

fetchQuestion().then((data)=>{
    question.value = data.description;
    options.value = data.options;
    correctOption.value = data.correct;
    qid.value = data.id;
})

async function editQuestion(e){
    const entries = new FormData(e.target);
    entries.append("description",document.getElementById("question-statement").innerText)
    entries.append("correct",entries.get("correct"))

    let res = await api.put(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}`,entries);
    router.push({
        "path": `/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${props.qid}`
    })
    return res.data
}
</script>

<template>
    <div v-if="question" class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <form @submit.prevent="editQuestion">
            <input type="hidden" name="correct" :value="correctOption">
            <EditableQuestion :description="question" :index="qid"/>
            
            <div class="option-container">
                <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                    <template v-for="n in 4">
                        <EditableOption :default="options[n - 1]" :option="n - 1" :correct-option="correctOption" :set-correct-option="(x)=>{
                            correctOption = x;
                        }"/>
                    </template>
                </div>
            </div>
    
            <div class="d-flex justify-content-center mt-3">
                <input type="submit" id="submit-button" value="Confirm Edit?">
            </div>
        </form>
    </div>

</template>

<style scoped>

#submit-button{
    border: 1px solid var(--light-color);
    color: var(--light-color);
    background-color: var(--tertiary-color);
    padding: 0.5em;
    border-radius: 10px;
}

.option-container{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    margin-top: 2em;
}

</style>