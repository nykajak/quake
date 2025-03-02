<script setup>
    import { ref, watch } from 'vue';
    import { api } from '@/api';

    const filter = ref(null);
    const question_description = ref(null);
    const hidden = ref(true);

    const subject = ref(null);
    const chapter = ref(null);
    const quiz = ref(null);
    const question = ref(null);

    const subjectValues = ref(null);
    const chapterValues = ref(null);
    const quizValues = ref(null);
    const questionValues = ref(null);

    async function fetchSubjectValues(){
        let res = await api.get("/admin/subjects/")
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

    if (subject.value == null){
        fetchSubjectValues()
    }

    watch(subject, (newVal, oldVal)=>{
        fetchChapterValues();
        chapter.value = null
        questionValues.value = null;
        quizValues.value = null;
        question.value = null;
        quiz.value = null;
    })

    watch(chapter, (newVal, oldVal)=>{
        fetchQuestionValues();
        fetchQuizValues();
        question.value = null;
        quiz.value = null;
    })

</script>

<template>
    <div class="d-flex flew-column flex-grow-1">
        <form @submit.prevent="" class="w-100 d-flex flex-column align-items-center mt-3">
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
                    <div class="d-flex flex-column">
                        <div class="dropdown" @click="hidden=!hidden">
                            <input id="dropdown-input" type="text" readonly v-model="question_description">
                        </div>
                        <div class="dropdown-options" v-show="hidden == false && questionValues">
                            <div class="d-flex flex-column">
                                <template v-for="val in questionValues">
                                    <button class="dropdown-button" @click="question=val.id;question_description=val.description;hidden=true">{{val.description}}</button>
                                </template>
                            </div>
                        </div>
                    </div>
                </div> 
            </div>

            <div class="d-flex flex-row gap-2">
                <input type="submit" id="submit-button" value="Apply filters">
            </div>
        </form>
    </div>
</template>

<style scoped>

#dropdown-input{
    display: flex;
    width: 30em;
}

.dropdown{
    display: flex;
    flex-direction: row;
    gap: 1em;
    anchor-name: --dropdown;
}

.dropdown-options{
    position: absolute;
    position-anchor: --dropdown;
    position-area: bottom center;
    overflow-y: auto;
    height: 5em;
    width: 100%;
    border: 1px solid light-dark(var(--dark-color), var(--light-color));
}

.dropdown-button{
    background-color: light-dark(var(--light-color),var(--dark-color));
    border: none;
}

.dropdown-button:hover{
    background-color: var(--secondary-color);
}

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