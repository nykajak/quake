<script setup>
    import { ref, watch } from 'vue';
    import { api } from '@/api';

    import DropDown from './components/DropDown.vue';

    const filter = ref(null);
    const question_description = ref(null);
    const hidden = ref(true);

    const user = ref(null)
    const subject = ref(null);
    const chapter = ref(null);
    const quiz = ref(null);
    const question = ref(null);

    const userValues = ref(null);
    const subjectValues = ref(null);
    const chapterValues = ref(null);
    const quizValues = ref(null);
    const questionValues = ref(null);

    async function fetchUserValues(){
        let res = await api.get("/admin/users/?filter=all")
        userValues.value = res.data.payload
    }

    async function fetchSubjectValues(){
        let res = await api.get("/admin/subjects/?filter=all")
        subjectValues.value = res.data.payload
    }

    async function fetchChapterValues(){
        let res = await api.get(`/admin/subjects/${subject.value}`)
        chapterValues.value = res.data.payload.chapters
    }

    async function fetchQuizValues(){
        let res = await api.get(`/admin/subjects/${subject.value}/chapters/${chapter.value}/quizes/?filter=all`)
        quizValues.value = res.data.payload
    }

    async function fetchQuestionValues(){
        let res = await api.get(`/admin/subjects/${subject.value}/chapters/${chapter.value}/questions/?filter=all`)
        questionValues.value = res.data.payload.questions
    }

    if (subjectValues.value == null){
        fetchSubjectValues();
    }

    // if (userValues.value == null){
    //     fetchUserValues();
    // }

    watch(subject, (newVal, oldVal)=>{
        fetchChapterValues();
        chapter.value = null
        questionValues.value = null;
        quizValues.value = null;
        question.value = null;
        quiz.value = null;
        question_description.value = null;
    })

    watch(chapter, (newVal, oldVal)=>{
        fetchQuestionValues();
        fetchQuizValues();
        question.value = null;
        quiz.value = null;
        question_description.value = null;
    })

    function handleForm(e){
        let f = new FormData(e.target)
        // if (e.get("filter") == "question"){
        //     f.append("question_id",question);
        // }
        // else{
        //     f.append("quiz_id",quiz);
        // }
    }

</script>

<template>
    <div class="d-flex flew-column flex-grow-1">
        <form @submit.prevent="handleForm" class="w-100 d-flex flex-column align-items-center mt-3">
            <div class="d-flex flex-row gap-2 mb-3 flex-wrap justify-content-center">
                <div class="d-flex flex-row align-items-center justify-content-center gap-2">
                    <label class="field-label" for="username">Username </label>
                    <input class="d-flex flex-grow-1" type="text" name="username" placeholder="Ben">
                </div>

                <!-- Subject selection -->
                <div class="d-flex flex-row align-items-center justify-content-center gap-2">
                    <label class="field-label" for="pick">Subject </label>
                    <select v-model="subject">
                        <option disabled value="">Please select one</option>
                        <template v-for="val in subjectValues">
                            <option :value="val.id">{{val.name}}</option>
                        </template>
                    </select>
                </div>

                <!-- Chapter selection -->
                <div class="d-flex flex-row align-items-center justify-content-center gap-2">
                    <label class="field-label" for="pick">Chapter </label>
                    <select v-model="chapter">
                        <option disabled value="">Please select one</option>
                        <template v-for="val in chapterValues">
                            <option :value="val.id">{{val.name}}</option>
                        </template>
                    </select>
                </div>
            </div>
            
            <div class="d-flex flex-row gap-2 mb-3 flex-wrap justify-content-center">
                <div class="d-flex gap-2 align-items-center">
                    <label for="question_filter">Filter by Question</label>
                    <input type="radio" name="filter" id="question_filter" v-model="filter" value="question">
                </div>
                <div class="d-flex gap-2 align-items-center">
                    <label for="quiz_filter">Filter by Quiz</label>
                    <input type="radio" name="filter" id="quiz_filter" v-model="filter" value="quiz">
                </div>
            </div>

            <div class="d-flex flex-row gap-2 mb-3 flex-wrap justify-content-center">
                <!-- Quiz selection -->
               <div v-if="filter == `quiz`" class="d-flex flex-row align-items-center justify-content-center gap-2">
                    <label class="field-label" for="pick">Quiz </label>
                
                    <select v-model="quiz">
                        <option disabled value="">Please select one</option>
                        <template v-for="val in quizValues">
                            <option :value="val.id">{{val.description}}</option>
                        </template>
                    </select>
                </div>

                <!-- Question selection -->
                <div v-if="filter == `question`" class="d-flex flex-row align-items-center justify-content-center gap-2">
                    Question: 
                    <DropDown type="question" :values="questionValues" current="" :setVal="(x)=>{
                        question = x;
                    }"/>
                </div> 
            </div>

            <div class="d-flex flex-row gap-2">
                <input type="submit" id="submit-button" value="Apply filters">
            </div>
        </form>
    </div>
</template>

<style scoped>

#submit-button{
    background-color: var(--secondary-color);
    color: var(--light-color);
    border: none;
    padding-left: 0.5em;
    padding-right: 0.5em;
}

input::placeholder{
    padding-left: 0.3em;
}
</style>