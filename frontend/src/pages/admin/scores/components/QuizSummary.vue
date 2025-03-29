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
    <Doughnut :data="{
        labels: ['correct','incorrect','not attempted'],
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
    <div class="d-flex justify-content-center mt-2">
        <h3 v-if="props.data[2] < 1000">Attempt summary</h3>
        <h3 v-if="props.data[2] >= 1000">Quiz empty</h3>
    </div>
</template>

<style scoped>
</style>