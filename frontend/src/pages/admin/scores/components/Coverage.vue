<script setup>
    
    import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
    import { Doughnut } from 'vue-chartjs'
    ChartJS.register(ArcElement, Tooltip, Legend)

    const color1 = window.getComputedStyle(document.body).getPropertyValue('--tertiary-color');
    const color2 = window.getComputedStyle(document.body).getPropertyValue('--error-color');
    const color3 = window.getComputedStyle(document.body).getPropertyValue('--contrast-color');
    let colors = [color1,color2,color3]
    
    const props = defineProps(['data'])
</script>

<template>
    <div class="d-flex flex-column align-items-center">
        <Doughnut :data="{
            labels: ['attempted','unattempted','unknown'],
            datasets: [
                {
                    backgroundColor: colors,
                    data: props.data
                }
            ]
        }" :options="{
            'responsive': true,
            maintainAspectRatio: true,
            animation: false
        }" />
        <div class="d-flex mt-2">
            <h3>Coverage of questions</h3>
        </div>
    </div>
</template>

<style scoped>
</style>