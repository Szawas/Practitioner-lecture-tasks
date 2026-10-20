export const rupiah = value => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(value)
export const shortRupiah = value => value >= 1e9 ? `Rp${(value / 1e9).toFixed(1)} M` : value >= 1e6 ? `Rp${(value / 1e6).toFixed(1)} jt` : value >= 1e3 ? `Rp${(value / 1e3).toFixed(0)} rb` : rupiah(value)
export const dateLabel = value => new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${value}T00:00:00Z`))
export const monthLabel = value => new Intl.DateTimeFormat('id-ID', { month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${value}-01T00:00:00Z`))
