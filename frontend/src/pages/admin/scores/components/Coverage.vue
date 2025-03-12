<script setup>
    
    import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
    import { Doughnut } from 'vue-chartjs'
    ChartJS.register(ArcElement, Tooltip, Legend)
    
    const props = defineProps(['attemptedQuestions','unattemptedQuestions','color1','color2'])
</script>

<template>
    <div v-if="attemptedQuestions + unattemptedQuestions !== 0" class="d-flex flex-column align-items-center">
        <Doughnut :data="{
            labels: ['attempted','unattempted'],
            datasets: [
                {
                    backgroundColor: [color1, color2],
                    data: [attemptedQuestions, unattemptedQuestions]
                }
            ]
        }" :options="{
            'responsive': true,
            maintainAspectRatio: true,
        }" />
        <div class="d-flex mt-2">
            <h3>Coverage of questions</h3>
        </div>
    </div>

    <div v-else>
        No questions yet!
    </div>
</template>

<style scoped>
</style>