<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  components: { Bar },
  props: ['chartData'],
  data() {
    return {
      chartOptions: {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: { display: true, text: 'Seat Availability' }
        }
      }
    }
  }
}
</script>
