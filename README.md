# 🧬 Algoritma Genetika — Knapsack Problem

### Praktikum Kecerdasan Buatan | Pertemuan 10

## 📦 Data Barang & Kapasitas Gudang

| Barang  | Keuntungan | Ukuran |
| ------- | ---------- | ------ |
| Barang1 | 10         | 5      |
| Barang2 | 40         | 4      |
| Barang3 | 30         | 6      |
| Barang4 | 50         | 3      |
| Barang5 | 35         | 7      |

**Ukuran Maksimal Gudang: 15**

---

## 🗂️ Struktur File

```
📁 Proyek/
├── main.py               # Program utama GA (tanpa GUI)
├── gui.py                # Program utama GA dengan GUI Tkinter
├── InisiasiPopulasi.py   # Fungsi inisialisasi populasi awal
├── EvaluasiFitness.py    # Fungsi evaluasi / hitung fitness
├── selection.py          # Fungsi seleksi (RWS & Tournament)
├── crossover.py          # Fungsi crossover (One Point, Two Point, Uniform)
├── mutation.py           # Fungsi mutasi (Swap, Inversion, Uniform)
└── README.md             # Dokumentasi ini
```

---

## ⚙️ Cara Instalasi & Menjalankan

### 1. Dependensi

```bash
pip install matplotlib
```

### 2. Menjalankan Versi Terminal (tanpa GUI)

```bash
python main.py
```

### 3. Menjalankan Versi GUI (Tkinter)

```bash
python gui.py
```

---

## 🖥️ Panduan Penggunaan GUI

### Panel Kiri — Input & Hasil

| Bagian           | Keterangan                                                            |
| ---------------- | --------------------------------------------------------------------- |
| 📦 Data Barang   | Menampilkan daftar barang, keuntungan, ukuran, dan kapasitas gudang   |
| ⚙️ Parameter GA  | Atur parameter sebelum menjalankan GA                                 |
| ▶ Jalankan GA    | Tombol untuk memulai proses GA                                        |
| 🗑 Reset         | Membersihkan grafik, log, dan hasil                                   |
| Progress Bar     | Menunjukkan kemajuan proses per generasi                              |
| 🏆 Hasil Terbaik | Menampilkan keuntungan maksimal, ukuran terpakai, dan barang terpilih |

### Panel Kanan — Visualisasi

| Bagian          | Keterangan                                                                     |
| --------------- | ------------------------------------------------------------------------------ |
| 📈 Grafik       | Menampilkan perkembangan fitness (tertinggi, terendah, rata-rata) per generasi |
| 📋 Log Generasi | Mencatat nilai fitness tiap 5 generasi secara real-time                        |

### Parameter yang Dapat Diatur

| Parameter       | Default | Keterangan                           |
| --------------- | ------- | ------------------------------------ |
| Jumlah Generasi | 50      | Banyaknya iterasi evolusi (1–500)    |
| Ukuran Populasi | 20      | Jumlah individu per generasi (2–200) |
| Prob. Crossover | 0.8     | Peluang crossover terjadi (0–1)      |
| Prob. Mutasi    | 0.1     | Peluang mutasi terjadi (0–1)         |

---

## 🔬 Penjelasan Algoritma Genetika

### Representasi Kromosom

Kromosom direpresentasikan sebagai **binary string** sepanjang jumlah barang:

```
[ 0, 1, 0, 1, 1 ]
  B1  B2  B3  B4  B5
```

- `1` = barang dipilih untuk masuk gudang
- `0` = barang tidak dipilih

### 1. Inisialisasi Populasi

Populasi awal dibangkitkan secara **acak**. Setiap individu memiliki kromosom biner yang mewakili kombinasi barang yang dipilih.

### 2. Evaluasi Fitness

Fungsi fitness menghitung **total keuntungan** dari barang yang dipilih:

- Jika total ukuran ≤ kapasitas gudang → fitness = total keuntungan
- Jika total ukuran > kapasitas gudang → fitness = **0** (penalti)

### 3. Seleksi — Roulette Wheel Selection (RWS)

Setiap individu mendapat **peluang terpilih** sebanding dengan nilai fitnessnya:

```
P(individu_i) = fitness_i / total_fitness
```

Individu dengan fitness lebih tinggi lebih berpeluang terpilih sebagai parent.

### 4. Crossover — Uniform Crossover

Dua parent menghasilkan dua anak dengan **mask acak** per-gen:

- Jika mask = `0` → anak1 ambil dari parent1, anak2 dari parent2
- Jika mask = `1` → anak1 ambil dari parent2, anak2 dari parent1

```
Parent1 : [1, 0, 1, 1, 0]
Parent2 : [0, 1, 0, 0, 1]
Mask    : [0, 1, 0, 1, 1]
Anak1   : [1, 1, 1, 0, 1]
Anak2   : [0, 0, 0, 1, 0]
```

### 5. Mutasi — Inversion Mutation

Memilih dua titik acak, lalu **membalik urutan gen** di antara kedua titik tersebut:

```
Sebelum : [1, 0, | 1, 1, 0 |]
Sesudah : [1, 0, | 0, 1, 1 |]
```

Mutasi menjaga keberagaman populasi dan membantu keluar dari solusi lokal optimal.

### 6. Pembentukan Populasi Baru

Anak-anak yang dihasilkan dari crossover dan mutasi menggantikan populasi lama. Proses ini diulang hingga jumlah generasi tercapai.

---
