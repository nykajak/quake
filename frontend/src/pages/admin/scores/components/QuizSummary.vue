<script setup>
    
    import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
    import { Doughnut } from 'vue-chartjs'
    ChartJS.register(ArcElement, Tooltip, Legend)
    
    const props = defineProps(['correctResponses','wrongResponses','unattemptedQuestions','color1','color2','color3'])
</script>

<template>
    <div v-if="!(props.correctResponses + props.wrongResponses + props.unattemptedQuestions == 0)" class="d-flex flex-column align-items-center">
        <Doughnut :data="{
            labels: ['correct','incorrect','not attempted'],
            datasets: [
                {
                    backgroundColor: [props.color1, props.color2, props.color3],
                    data: [props.correctResponses, props.wrongResponses,props.unattemptedQuestions]
                }
            ]
        }" :options="{
            'responsive': true,
            maintainAspectRatio: true,
        }" />
        <div class="d-flex mt-2">
            <h3>Attempt summary</h3>
        </div>
    </div>

    <div v-else class="d-flex w-50 justify-content-between">
        No questions yet!
    </div>
</template>

<style scoped>
</style>