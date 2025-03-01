<script setup>
    import { ref, watch } from 'vue';
    import { api } from '@/api';

    const filter = ref("subject");
    const picked = ref(null);
    const values = ref(null);

    watch(filter, (newVal, oldVal) =>{
        console.log(newVal);
        fetchValues()
    })

    async function fetchValues(){
        if (filter.value === "subject"){
            let res = await api.get("/admin/subjects/")
            values.value = res.data.payload
        }
    }

    fetchValues()
</script>

<template>
    <div class="d-flex flew-column flex-grow-1">
        <form @submit.prevent="" class="w-100 d-flex flex-column align-items-center mt-3">
            <div class="d-flex justify-content-center mb-2">
                <div class="d-flex p-2 gap-2">
                    <label for="subject-filter">Filter by Subject</label>
                    <input type="radio" name="filter" value="subject" id="subject-filter" v-model="filter">
                </div>
                <div class="d-flex p-2 gap-2">
                    <label for="chapter-filter">Filter by Chapter</label>
                    <input type="radio" name="filter" value="chapter" id="chapter-filter" v-model="filter">
                </div>
                <div class="d-flex p-2 gap-2">
                    <label for="quiz-filter">Filter by Quiz</label>
                    <input type="radio" name="filter" value="quiz" id="quiz-filter" v-model="filter">
                </div>
                <div class="d-flex p-2 gap-2">
                    <label for="question-filter">Filter by Question</label>
                    <input type="radio" name="filter" value="question" id="question-filter" v-model="filter">
                </div>
            </div>

            <div class="d-flex flex-row gap-2 mb-3">
                <div class="d-flex flex-row align-items-center justify-content-center gap-2">
                    <label class="field-label" for="username">Username </label>
                    <input class="d-flex flex-grow-1" type="text" name="username" placeholder="Ben">
                </div>
                <div class="d-flex flex-row align-items-center justify-content-center gap-2">
                    <label class="field-label" for="pick">{{filter.slice(0,1).toUpperCase() + filter.slice(1)}} </label>
                    <select v-model="picked">
                        <option disabled value="">Please select one</option>
                        <template v-for="val in values">
                            <option :value="val.id">{{val.name}}</option>
                        </template>
                    </select>
                </div>
            </div>
            <div class="d-flex flex-row gap-2">
                <input type="submit" id="submit-button" value="Apply filters">
            </div>
        </form>

        <div>

        </div>
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