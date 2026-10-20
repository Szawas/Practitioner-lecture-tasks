<script setup>
import { computed } from 'vue'
import { Bar, Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler } from 'chart.js'
import { shortRupiah, rupiah } from '../utils/format'
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler)
const props = defineProps({ type: { type: String, required: true }, labels: { type: Array, required: true }, values: { type: Array, required: true } })
const data = computed(() => ({ labels: props.labels, datasets: [{ label: 'Total penjualan', data: props.values, borderColor: '#0f766e', backgroundColor: props.type === 'line' ? 'rgba(15,118,110,0.10)' : '#14b8a6', pointBackgroundColor: '#0f766e', pointRadius: 4, borderWidth: 2.5, tension: 0.35, fill: props.type === 'line', borderRadius: 7, maxBarThickness: 48 }] }))
const options = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ` Penjualan: ${rupiah(ctx.parsed.y)}` } } }, scales: { x: { grid: { display: false }, ticks: { color: '#64748b' } }, y: { beginAtZero: true, grid: { color: '#edf2f5' }, ticks: { color: '#64748b', callback: shortRupiah } } } }
</script>
<template><div class="h-64 w-full" role="img" :aria-label="`${type === 'line' ? 'Grafik tren' : 'Grafik perbandingan'} penjualan; nilai detail tersedia pada tabel transaksi`"><Line v-if="type === 'line'" :data="data" :options="options"/><Bar v-else :data="data" :options="options"/></div></template>
