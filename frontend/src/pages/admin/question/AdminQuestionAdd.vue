<script setup>

import { ref } from 'vue';
import { api } from '@/api';
import { useRouter } from 'vue-router';

import EditableOption from './components/EditableOption.vue';
import EditableQuestion from './components/EditableQuestion.vue';

const props = defineProps(['sid','cid'])
const router = useRouter();

const correctOption = ref(-1);

async function createQuestion(e){
    let f = new FormData(e.target);
    f.append("description",document.getElementById("question-statement").innerText)
    let res = await api.post(`/admin/subjects/${props.sid}/chapters/${props.cid}/questions/`, f)
    router.push({
        "path": `/admin/subjects/${props.sid}/chapters/${props.cid}/questions/${res.data.payload}`
    })
    return res.data;
}
</script>

<template>
    <div class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <form @submit.prevent="createQuestion">
            <input type="hidden" name="correct" :value="correctOption">
            <EditableQuestion description=""/>
            
            <div class="option-container">
                <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                    <template v-for="n in 4">
                        <EditableOption default="" :option="n - 1" :correct-option="correctOption" :set-correct-option="(x)=>{
                            correctOption = x;
                        }"/>
                    </template>
                </div>
            </div>
    
            <div class="d-flex justify-content-center mt-3">
                <input type="submit" id="submit-button" value="Add Question">
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