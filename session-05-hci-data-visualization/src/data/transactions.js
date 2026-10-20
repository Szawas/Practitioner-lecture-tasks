// Dataset simulasi deterministik: bukan data penjualan nyata.
const products = [
  { name: 'Laptop', category: 'Elektronik', price: 7200000 },
  { name: 'Headset', category: 'Elektronik', price: 380000 },
  { name: 'Mouse', category: 'Elektronik', price: 175000 },
  { name: 'Kursi Kerja', category: 'Furnitur', price: 1450000 },
  { name: 'Meja Belajar', category: 'Furnitur', price: 950000 },
  { name: 'Buku Catatan', category: 'Alat Tulis', price: 35000 },
  { name: 'Pulpen', category: 'Alat Tulis', price: 18000 },
  { name: 'Botol Minum', category: 'Aksesori', price: 115000 },
  { name: 'Tas', category: 'Aksesori', price: 285000 }
]
const months = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06']
export const transactions = months.flatMap((month, mi) =>
  Array.from({ length: 20 }, (_, j) => {
    const product = products[(j * 7 + mi * 3) % products.length]
    const qty = 1 + ((j + mi * 2) % 4)
    const day = String(1 + ((j * 3 + mi) % 28)).padStart(2, '0')
    return { id: `TRX-${String(mi * 20 + j + 1).padStart(3, '0')}`, date: `${month}-${day}`, product: product.name, category: product.category, qty, price: product.price, total: qty * product.price }
  })
)
export const monthOptions = months
export const categories = [...new Set(products.map(p => p.category))]
