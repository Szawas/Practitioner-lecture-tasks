<script setup>
import { computed, ref } from 'vue'
import { LayoutDashboard, TrendingUp, ShoppingBag, Package, Download, RotateCcw, Search, ChartNoAxesCombined, Info } from 'lucide-vue-next'
import SalesChart from './components/SalesChart.vue'
import { transactions, categories, monthOptions } from './data/transactions'
import { rupiah, shortRupiah, dateLabel, monthLabel } from './utils/format'
const month = ref('all')
const category = ref('all')
const search = ref('')
const filtered = computed(() => transactions.filter(t => (month.value === 'all' || t.date.startsWith(month.value)) && (category.value === 'all' || t.category === category.value) && (!search.value.trim() || `${t.id} ${t.product}`.toLowerCase().includes(search.value.trim().toLowerCase()))))
const total = computed(() => filtered.value.reduce((sum, t) => sum + t.total, 0))
const units = computed(() => filtered.value.reduce((sum, t) => sum + t.qty, 0))
const bestProduct = computed(() => {
  if (!filtered.value.length) return '—'
  const sums = {}
  filtered.value.forEach(t => { sums[t.product] = (sums[t.product] || 0) + t.qty })
  return Object.entries(sums).sort((a, b) => b[1] - a[1])[0][0]
})
const monthly = computed(() => monthOptions.map(m => filtered.value.filter(t => t.date.startsWith(m)).reduce((sum, t) => sum + t.total, 0)))
const byCategory = computed(() => categories.map(c => filtered.value.filter(t => t.category === c).reduce((sum, t) => sum + t.total, 0)))
const rows = computed(() => [...filtered.value].sort((a, b) => b.date.localeCompare(a.date) || b.id.localeCompare(a.id)))
function reset() { month.value = 'all'; category.value = 'all'; search.value = '' }
function downloadCSV() {
  const header = ['ID', 'Tanggal', 'Produk', 'Kategori', 'Jumlah', 'Harga Satuan', 'Total']
  const escape = value => `"${String(value).replaceAll('"', '""')}"`
  const content = [header, ...rows.value.map(t => [t.id, t.date, t.product, t.category, t.qty, t.price, t.total])].map(line => line.map(escape).join(',')).join('\r\n')
  const blob = new Blob(['\uFEFF' + content], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a'); link.href = url; link.download = 'sales-insight-transaksi.csv'; link.click()
  URL.revokeObjectURL(url)
}
</script>
<template>
  <div class="min-h-screen">
    <header class="bg-white border-b border-slate-200">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 py-4 flex items-center justify-between gap-4">
        <div class="flex items-center gap-3"><div class="bg-teal-700 text-white p-2.5 rounded-xl"><ChartNoAxesCombined :size="22"/></div><div><p class="font-extrabold tracking-tight text-slate-900">Sales Insight</p><p class="text-xs text-slate-500">Dashboard analisis penjualan</p></div></div>
        <span class="hidden sm:inline-flex items-center gap-2 text-xs text-teal-800 bg-teal-50 px-3 py-2 rounded-full"><span class="w-2 h-2 bg-teal-500 rounded-full"></span>Data simulasi 2026</span>
      </div>
    </header>
    <main class="mx-auto max-w-7xl px-4 sm:px-6 py-8 space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-3"><div><p class="text-xs uppercase tracking-widest text-teal-700 font-bold mb-2">Overview</p><h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900">Ringkasan Penjualan</h1><p class="text-sm text-slate-500 mt-2">Pantau performa penjualan dan temukan pola dari data transaksi.</p></div><button type="button" @click="downloadCSV" :disabled="!rows.length" class="inline-flex items-center justify-center gap-2 bg-teal-700 hover:bg-teal-800 disabled:opacity-50 text-white rounded-xl px-4 py-2.5 text-sm font-semibold transition"><Download :size="17"/> Unduh CSV</button></div>
      <section class="panel p-5" aria-label="Filter data"><div class="flex flex-wrap justify-between items-center gap-3 mb-4"><h2 class="font-bold text-slate-800">Filter Data</h2><button type="button" @click="reset" class="text-sm font-semibold text-teal-700 hover:underline inline-flex gap-1.5 items-center"><RotateCcw :size="15"/> Reset filter</button></div><div class="grid grid-cols-1 md:grid-cols-3 gap-4"><label class="text-xs font-semibold text-slate-600">Bulan<select v-model="month" class="field mt-2"><option value="all">Semua bulan</option><option v-for="m in monthOptions" :key="m" :value="m">{{ monthLabel(m) }}</option></select></label><label class="text-xs font-semibold text-slate-600">Kategori<select v-model="category" class="field mt-2"><option value="all">Semua kategori</option><option v-for="c in categories" :key="c" :value="c">{{ c }}</option></select></label><label class="text-xs font-semibold text-slate-600">Cari transaksi<div class="relative mt-2"><Search :size="16" class="absolute left-3 top-3 text-slate-400"/><input v-model="search" class="field pl-9" type="search" placeholder="ID atau nama produk"/></div></label></div><p class="text-xs text-slate-500 mt-3" role="status">Menampilkan {{ filtered.length }} dari {{ transactions.length }} transaksi.</p></section>
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" aria-label="Statistik penjualan"><article class="metric"><div class="flex justify-between"><span class="text-sm text-slate-500">Total Penjualan</span><TrendingUp class="text-teal-600" :size="19"/></div><p class="text-xl font-extrabold mt-3 text-slate-900">{{ shortRupiah(total) }}</p><p class="text-xs text-slate-500 mt-2" :title="rupiah(total)">{{ rupiah(total) }}</p></article><article class="metric"><div class="flex justify-between"><span class="text-sm text-slate-500">Jumlah Transaksi</span><ShoppingBag class="text-teal-600" :size="19"/></div><p class="text-2xl font-extrabold mt-3 text-slate-900">{{ filtered.length }}</p><p class="text-xs text-slate-500 mt-2">Transaksi sesuai filter</p></article><article class="metric"><div class="flex justify-between"><span class="text-sm text-slate-500">Produk Terjual</span><Package class="text-teal-600" :size="19"/></div><p class="text-2xl font-extrabold mt-3 text-slate-900">{{ units }}</p><p class="text-xs text-slate-500 mt-2">Total unit produk</p></article><article class="metric"><div class="flex justify-between"><span class="text-sm text-slate-500">Produk Terlaris</span><LayoutDashboard class="text-teal-600" :size="19"/></div><p class="text-xl font-extrabold mt-3 text-slate-900">{{ bestProduct }}</p><p class="text-xs text-slate-500 mt-2">Berdasarkan jumlah unit</p></article></section>
      <section class="grid grid-cols-1 lg:grid-cols-2 gap-5" aria-label="Visualisasi penjualan"><article class="panel p-5"><h2 class="font-bold text-slate-800">Tren Penjualan</h2><p class="text-xs text-slate-500 mt-1 mb-5">Total pendapatan per bulan</p><SalesChart type="line" :labels="monthOptions.map(monthLabel)" :values="monthly"/></article><article class="panel p-5"><h2 class="font-bold text-slate-800">Penjualan per Kategori</h2><p class="text-xs text-slate-500 mt-1 mb-5">Perbandingan total pendapatan</p><SalesChart type="bar" :labels="categories" :values="byCategory"/></article></section>
      <section class="panel overflow-hidden" aria-label="Tabel transaksi"><div class="p-5 flex flex-wrap justify-between gap-2 items-center"><div><h2 class="font-bold text-slate-800">Detail Transaksi</h2><p class="text-xs text-slate-500 mt-1">Data mengikuti filter yang dipilih</p></div><span class="text-xs text-slate-500">{{ rows.length }} baris</span></div><div class="overflow-x-auto"><table class="w-full text-left text-sm"><thead class="bg-slate-50 text-slate-600 text-xs uppercase"><tr><th class="px-5 py-3">ID</th><th class="px-5 py-3">Tanggal</th><th class="px-5 py-3">Produk</th><th class="px-5 py-3">Kategori</th><th class="px-5 py-3 text-right">Qty</th><th class="px-5 py-3 text-right">Total</th></tr></thead><tbody><tr v-for="t in rows" :key="t.id" class="border-t border-slate-100 hover:bg-teal-50/40"><td class="px-5 py-3 font-medium text-slate-700">{{ t.id }}</td><td class="px-5 py-3 text-slate-600">{{ dateLabel(t.date) }}</td><td class="px-5 py-3">{{ t.product }}</td><td class="px-5 py-3 text-slate-600">{{ t.category }}</td><td class="px-5 py-3 text-right">{{ t.qty }}</td><td class="px-5 py-3 text-right font-semibold">{{ rupiah(t.total) }}</td></tr><tr v-if="!rows.length"><td colspan="6" class="text-center px-5 py-12 text-slate-500">Tidak ada transaksi yang cocok. Coba ubah atau reset filter.</td></tr></tbody></table></div></section>
      <div class="flex gap-2 text-xs text-slate-500 items-start"><Info :size="16" class="shrink-0 text-teal-700"/><p>Seluruh transaksi adalah data simulasi untuk pembelajaran Human-Computer Interaction dan Data Visualization. Grafik serta statistik berubah sesuai filter.</p></div>
    </main><footer class="text-center text-xs text-slate-400 py-6 border-t border-slate-200">Sales Insight • Practitioner Lecture Series — Sesi 05</footer>
  </div>
</template>
