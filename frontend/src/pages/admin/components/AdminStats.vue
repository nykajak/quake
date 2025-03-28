<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';
    import Loader from '@/components/Loader.vue';
    import NavButton from '@/components/NavButton.vue';

    const countUsers = ref(null);
    const countSubjects = ref(null);
    const countQuestions = ref(null);
    const countResponses = ref(null);

    async function fetchStats(){
        let res;

        try{
            res = await api.get("/admin/")
        }

        catch(err){
            console.log(err)
        }

        countUsers.value = res.data.count_users
        countSubjects.value = res.data.count_subjects
        countQuestions.value = res.data.count_questions
        countResponses.value = res.data.count_responses
    }

    fetchStats()
</script>

<template>
    <div class="d-flex flex-column pt-3 gap-1 align-items-center justify-content-start w-100">
        <div class="statisticContainer">
            <div class="statisticDiv">
                <h2 class="headerText">
                    User Count!
                </h2>
                <p class="countNumber text-center">
                    <template v-if="countUsers">
                        {{ countUsers }}
                    </template>
                    <Loader v-else/>
                </p>
            </div>
            <div class="statisticDiv">
                <h2 class="headerText">
                    Subject Count!
                </h2>
                <p class="countNumber text-center">
                    <template v-if="countSubjects">
                        {{ countSubjects }}
                    </template>
                    <Loader v-else/>
                </p>
            </div>
            <div class="statisticDiv">
                <h2 class="headerText">
                    Question Count!
                </h2>
                <p class="countNumber text-center">
                    <template v-if="countQuestions">
                        {{ countQuestions }}
                    </template>
                    <Loader v-else/>
                </p>
            </div>

            <div class="statisticDiv">
                <h2 class="headerText">
                    Response Count!
                </h2>
                <p class="countNumber text-center">
                    <template v-if="countResponses">
                        {{ countResponses }}
                    </template>
                    <Loader v-else/>
                </p>
            </div>
            
        </div>
    </div>
</template>

<style scoped>
div{
    padding: 0em;
}

.statisticContainer{
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    width: 100%;
    gap: 0.1em;
    justify-content: space-evenly;
}

.headerText{
    background-color: var(--primary-color);    
    padding-left: 0.4em;
    padding-right: 0.4em;
    padding-bottom: 0.2em;
    color: var(--light-color);
    margin: 0;
}

.countNumber{
    display: flex;
    justify-content: center;
    padding-top: 1em;
    padding-bottom: 1em;
    font-size: 2em;
    margin: 0;
    
}

.statisticDiv{
    border: 10px solid var(--primary-color);
    border-radius: 5px;
}
</style>