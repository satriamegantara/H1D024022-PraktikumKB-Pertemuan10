import random
import matplotlib.pyplot as plt

# Mengimpor fungsi-fungsi dari file lain
from InisiasiPopulasi import inisialisasi_populasi
from EvaluasiFitness import hitung_fitness
from selection import roulette_wheel_selection
from crossover import uniform_crossover
from mutation import inversion_mutation

# Data barang: (nama, keuntungan, ukuran)
# Sesuai tugas Pertemuan 10
# ============================================================
barang = [
    ("Barang1", 10, 5),
    ("Barang2", 40, 4),
    ("Barang3", 30, 6),
    ("Barang4", 50, 3),
    ("Barang5", 35, 7),
]

# ============================================================
# Metode berdasarkan NIM berakhiran 22:
#   Digit pertama = 2 -> Seleksi : RWS (Roulette Wheel Selection)
#   Digit kedua   = 2 -> Crossover: Uniform Crossover
#   2 + 2 = 4         -> Mutasi  : Inversion Mutation
# ============================================================

def run_ga(jumlah_generasi, jumlah_populasi, prob_crossover, prob_mutasi, kapasitas_gudang):
    # Menentukan jumlah gen berdasarkan jumlah barang
    jumlah_gen = len(barang)

    # Inisialisasi populasi awal
    populasi = inisialisasi_populasi(jumlah_populasi, jumlah_gen)

    # List untuk menyimpan nilai fitness per generasi
    best_fitness_list = []
    worst_fitness_list = []
    avg_fitness_list = []
    all_fitness = []

    # Variabel untuk menyimpan individu terbaik secara keseluruhan
    best_individu = None
    best_fitness_overall = 0

    # Proses evolusi selama jumlah generasi yang ditentukan
    for generasi in range(jumlah_generasi):
        # Evaluasi fitness populasi saat ini
        fitness_populasi = [hitung_fitness(individu, barang, kapasitas_gudang) for individu in populasi]

        # Catat statistik fitness generasi ini
        best_fitness  = max(fitness_populasi)
        worst_fitness = min(fitness_populasi)
        avg_fitness   = sum(fitness_populasi) / len(fitness_populasi)
        best_fitness_list.append(best_fitness)
        worst_fitness_list.append(worst_fitness)
        avg_fitness_list.append(avg_fitness)
        all_fitness.append(fitness_populasi.copy())

        # Simpan individu terbaik secara keseluruhan
        if best_fitness > best_fitness_overall:
            best_fitness_overall = best_fitness
            index_best = fitness_populasi.index(best_fitness)
            best_individu = populasi[index_best][:]

        new_populasi = []
        used_indices = []

        # Membentuk populasi baru
        while len(new_populasi) < jumlah_populasi:
            # --- SELEKSI: Roulette Wheel Selection ---
            parent1, idx1 = roulette_wheel_selection(populasi, fitness_populasi)
            used_indices.append(idx1)

            # Pastikan parent2 berbeda dari parent1
            available_indices = [i for i in range(len(populasi)) if i not in used_indices]
            if not available_indices:
                used_indices = [idx1]
                available_indices = [i for i in range(len(populasi)) if i != idx1]

            parent2, rel_idx = roulette_wheel_selection(
                [populasi[i] for i in available_indices],
                [fitness_populasi[i] for i in available_indices]
            )
            used_indices.append(available_indices[rel_idx])

            # --- CROSSOVER: Uniform Crossover ---
            if random.random() < prob_crossover:
                anak1, anak2 = uniform_crossover(parent1, parent2)
            else:
                anak1, anak2 = parent1[:], parent2[:]

            # --- MUTASI: Inversion Mutation ---
            if random.random() < prob_mutasi:
                anak1 = inversion_mutation(anak1)
            if random.random() < prob_mutasi:
                anak2 = inversion_mutation(anak2)

            new_populasi.extend([anak1, anak2])

        # Potong populasi baru sesuai ukuran
        populasi = new_populasi[:jumlah_populasi]

    # ============================================================
    # Tampilkan grafik perkembangan fitness
    # ============================================================
    plt.figure(figsize=(12, 7))

    # Scatter semua nilai fitness tiap generasi (transparan)
    for i in range(jumlah_generasi):
        x = [i + 1] * len(all_fitness[i])
        y = all_fitness[i]
        plt.scatter(x, y, color='gray', alpha=0.1)

    plt.plot(range(1, jumlah_generasi + 1), best_fitness_list,  color='blue',   label='Fitness Tertinggi')
    plt.plot(range(1, jumlah_generasi + 1), worst_fitness_list, color='orange',  label='Fitness Terendah')
    plt.plot(range(1, jumlah_generasi + 1), avg_fitness_list,   color='red',    label='Fitness Rata-rata')

    plt.title('Perkembangan Nilai Fitness - Knapsack Problem\n'
              '(Seleksi: RWS | Crossover: Uniform | Mutasi: Inversion)')
    plt.xlabel('Generasi')
    plt.ylabel('Nilai Fitness (Keuntungan)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # ============================================================
    # Tampilkan hasil solusi terbaik
    # ============================================================
    selected_items  = [barang[i][0] for i in range(len(best_individu)) if best_individu[i] == 1]
    selected_profit = hitung_fitness(best_individu, barang, kapasitas_gudang)
    selected_size   = sum(barang[i][2] for i in range(len(best_individu)) if best_individu[i] == 1)

    print("=" * 45)
    print("         HASIL ALGORITMA GENETIKA")
    print("=" * 45)
    print(f"Metode Seleksi  : Roulette Wheel Selection")
    print(f"Metode Crossover: Uniform Crossover")
    print(f"Metode Mutasi   : Inversion Mutation")
    print("-" * 45)
    print(f"Keuntungan Maksimal : {selected_profit}")
    print(f"Total Ukuran Dipakai: {selected_size} / {kapasitas_gudang}")
    print("Barang yang Dibeli  :")
    for item in selected_items:
        idx = next(i for i, b in enumerate(barang) if b[0] == item)
        print(f"  - {item} (Keuntungan: {barang[idx][1]}, Ukuran: {barang[idx][2]})")
    print("=" * 45)


# ============================================================
# Jalankan GA
# ============================================================
run_ga(
    jumlah_generasi=50,
    jumlah_populasi=20,
    prob_crossover=0.8,
    prob_mutasi=0.1,
    kapasitas_gudang=15
)