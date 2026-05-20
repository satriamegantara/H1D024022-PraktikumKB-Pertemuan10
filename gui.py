import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

# Mengimpor fungsi-fungsi dari file lain
from InisiasiPopulasi import inisialisasi_populasi
from EvaluasiFitness import hitung_fitness
from selection import roulette_wheel_selection
from crossover import uniform_crossover
from mutation import inversion_mutation

# Data barang: (nama, keuntungan, ukuran)
barang = [
    ("Barang1", 10, 5),
    ("Barang2", 40, 4),
    ("Barang3", 30, 6),
    ("Barang4", 50, 3),
    ("Barang5", 35, 7),
]
KAPASITAS_GUDANG = 15

# Warna tema
BG_DARK     = "#1e1e2e"
BG_PANEL    = "#2a2a3e"
BG_CARD     = "#313150"
ACCENT      = "#7c6af7"
ACCENT2     = "#50fa7b"
TEXT_LIGHT  = "#cdd6f4"
TEXT_DIM    = "#6c7086"
RED_C       = "#f38ba8"
YELLOW_C    = "#f9e2af"
GREEN_C     = "#a6e3a1"
BLUE_C      = "#89b4fa"


def run_ga(jumlah_generasi, jumlah_populasi, prob_crossover, prob_mutasi,
           kapasitas_gudang, callback_generasi=None):
    """
    Menjalankan Algoritma Genetika dan mengembalikan hasil serta data plotting.
    callback_generasi(gen, best, worst, avg) dipanggil tiap generasi (opsional).
    """
    jumlah_gen = len(barang)
    populasi = inisialisasi_populasi(jumlah_populasi, jumlah_gen)

    best_fitness_list  = []
    worst_fitness_list = []
    avg_fitness_list   = []
    all_fitness        = []

    best_individu       = None
    best_fitness_overall = 0

    for generasi in range(jumlah_generasi):
        fitness_populasi = [hitung_fitness(ind, barang, kapasitas_gudang) for ind in populasi]

        best_f  = max(fitness_populasi)
        worst_f = min(fitness_populasi)
        avg_f   = sum(fitness_populasi) / len(fitness_populasi)

        best_fitness_list.append(best_f)
        worst_fitness_list.append(worst_f)
        avg_fitness_list.append(avg_f)
        all_fitness.append(fitness_populasi.copy())

        if best_f > best_fitness_overall:
            best_fitness_overall = best_f
            idx_best = fitness_populasi.index(best_f)
            best_individu = populasi[idx_best][:]

        if callback_generasi:
            callback_generasi(generasi + 1, best_f, worst_f, avg_f)

        new_populasi = []
        used_indices = []

        while len(new_populasi) < jumlah_populasi:
            # Seleksi: RWS
            parent1, idx1 = roulette_wheel_selection(populasi, fitness_populasi)
            used_indices.append(idx1)

            available_indices = [i for i in range(len(populasi)) if i not in used_indices]
            if not available_indices:
                used_indices = [idx1]
                available_indices = [i for i in range(len(populasi)) if i != idx1]

            parent2, rel_idx = roulette_wheel_selection(
                [populasi[i] for i in available_indices],
                [fitness_populasi[i] for i in available_indices]
            )
            used_indices.append(available_indices[rel_idx])

            # Crossover: Uniform
            if random.random() < prob_crossover:
                anak1, anak2 = uniform_crossover(parent1, parent2)
            else:
                anak1, anak2 = parent1[:], parent2[:]

            # Mutasi: Inversion
            if random.random() < prob_mutasi:
                anak1 = inversion_mutation(anak1)
            if random.random() < prob_mutasi:
                anak2 = inversion_mutation(anak2)

            new_populasi.extend([anak1, anak2])

        populasi = new_populasi[:jumlah_populasi]

    return best_individu, best_fitness_overall, best_fitness_list, worst_fitness_list, avg_fitness_list, all_fitness

class GeneticAlgorithmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritma Genetika — Knapsack Problem")
        self.root.configure(bg=BG_DARK)
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=ACCENT, height=50)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🧬  Algoritma Genetika  —  Knapsack Problem",
            bg=ACCENT, fg="white",
            font=("Consolas", 14, "bold"), pady=10
        ).pack(side="left", padx=20)

        tk.Label(
            header,
            text="Seleksi: RWS  |  Crossover: Uniform  |  Mutasi: Inversion",
            bg=ACCENT, fg="#ddd6fe",
            font=("Consolas", 9), pady=10
        ).pack(side="right", padx=20)

        # Body
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=12, pady=10)

        # Panel Kiri
        left = tk.Frame(body, bg=BG_DARK, width=280)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        self._build_left_panel(left)

        # Panel Kanan (grafik + log)
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        self._build_right_panel(right)

    def _build_left_panel(self, parent):
        # Info Barang
        card = self._card(parent, "📦  Data Barang")
        headers = ["Nama", "Keuntungan", "Ukuran"]
        for col, h in enumerate(headers):
            tk.Label(card, text=h, bg=BG_CARD, fg=ACCENT,
                     font=("Consolas", 8, "bold")).grid(row=0, column=col, padx=6, pady=2, sticky="w")
        for row, (nama, keunt, ukuran) in enumerate(barang, start=1):
            tk.Label(card, text=nama,    bg=BG_CARD, fg=TEXT_LIGHT, font=("Consolas", 8)).grid(row=row, column=0, padx=6, pady=1, sticky="w")
            tk.Label(card, text=keunt,   bg=BG_CARD, fg=YELLOW_C,   font=("Consolas", 8)).grid(row=row, column=1, padx=6, pady=1)
            tk.Label(card, text=ukuran,  bg=BG_CARD, fg=BLUE_C,     font=("Consolas", 8)).grid(row=row, column=2, padx=6, pady=1)

        tk.Label(card, text=f"Kapasitas Gudang: {KAPASITAS_GUDANG}",
                 bg=BG_CARD, fg=ACCENT2,
                 font=("Consolas", 9, "bold")).grid(row=len(barang)+1, column=0, columnspan=3, pady=(6, 2))

        card2 = self._card(parent, "⚙️  Parameter GA")

        params = [
            ("Jumlah Generasi",  "jumlah_generasi",  "50"),
            ("Ukuran Populasi",  "jumlah_populasi",  "20"),
            ("Prob. Crossover",  "prob_crossover",   "0.8"),
            ("Prob. Mutasi",     "prob_mutasi",       "0.1"),
        ]
        self.param_vars = {}
        for i, (label, key, default) in enumerate(params):
            tk.Label(card2, text=label, bg=BG_CARD, fg=TEXT_LIGHT,
                     font=("Consolas", 8)).grid(row=i, column=0, sticky="w", padx=6, pady=3)
            var = tk.StringVar(value=default)
            self.param_vars[key] = var
            entry = tk.Entry(card2, textvariable=var, width=8,
                             bg=BG_PANEL, fg=ACCENT2, insertbackground=ACCENT2,
                             font=("Consolas", 9), relief="flat", bd=2)
            entry.grid(row=i, column=1, padx=6, pady=3)

        # Tombol Jalankan
        self.btn_run = tk.Button(
            parent, text="▶  Jalankan GA",
            bg=ACCENT, fg="white",
            font=("Consolas", 11, "bold"),
            relief="flat", cursor="hand2",
            activebackground="#6a58e6", activeforeground="white",
            command=self._on_run
        )
        self.btn_run.pack(fill="x", pady=(4, 2))

        self.btn_clear = tk.Button(
            parent, text="🗑  Reset",
            bg=BG_PANEL, fg=TEXT_DIM,
            font=("Consolas", 9),
            relief="flat", cursor="hand2",
            activebackground=BG_CARD,
            command=self._on_reset
        )
        self.btn_clear.pack(fill="x", pady=(0, 6))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(parent, variable=self.progress_var,
                                        maximum=100, mode="determinate")
        self.progress.pack(fill="x", pady=(0, 4))

        self.lbl_progress = tk.Label(parent, text="", bg=BG_DARK, fg=TEXT_DIM,
                                     font=("Consolas", 8))
        self.lbl_progress.pack()

        card3 = self._card(parent, "🏆  Hasil Terbaik")
        self.lbl_keuntungan = tk.Label(card3, text="Keuntungan : -",
                                       bg=BG_CARD, fg=ACCENT2, font=("Consolas", 9, "bold"))
        self.lbl_keuntungan.grid(row=0, column=0, sticky="w", padx=6, pady=2)
        self.lbl_ukuran = tk.Label(card3, text="Ukuran Pakai: -",
                                   bg=BG_CARD, fg=BLUE_C, font=("Consolas", 9))
        self.lbl_ukuran.grid(row=1, column=0, sticky="w", padx=6, pady=2)
        self.lbl_barang = tk.Label(card3, text="Barang: -",
                                   bg=BG_CARD, fg=TEXT_LIGHT, font=("Consolas", 8),
                                   wraplength=220, justify="left")
        self.lbl_barang.grid(row=2, column=0, sticky="w", padx=6, pady=2)

    def _build_right_panel(self, parent):
        # Grafik matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.fig.patch.set_facecolor(BG_DARK)
        self.ax.set_facecolor(BG_PANEL)
        self.ax.set_title("Perkembangan Nilai Fitness", color=TEXT_LIGHT, fontsize=10)
        self.ax.set_xlabel("Generasi", color=TEXT_DIM)
        self.ax.set_ylabel("Fitness", color=TEXT_DIM)
        self.ax.tick_params(colors=TEXT_DIM)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(BG_CARD)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=(0, 6))

        # Log generasi
        log_frame = tk.Frame(parent, bg=BG_PANEL, bd=0)
        log_frame.pack(fill="x")

        tk.Label(log_frame, text="📋  Log Generasi",
                 bg=BG_PANEL, fg=ACCENT, font=("Consolas", 8, "bold")).pack(anchor="w", padx=8, pady=(4, 0))

        self.log_text = tk.Text(log_frame, height=6, bg=BG_PANEL, fg=TEXT_LIGHT,
                                font=("Consolas", 8), relief="flat", state="disabled",
                                insertbackground=TEXT_LIGHT)
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview, bg=BG_DARK)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True, padx=8, pady=4)
        scrollbar.pack(side="right", fill="y", pady=4)

        # Tag warna log
        self.log_text.tag_config("best",  foreground=GREEN_C)
        self.log_text.tag_config("worst", foreground=RED_C)
        self.log_text.tag_config("avg",   foreground=YELLOW_C)
        self.log_text.tag_config("header",foreground=ACCENT)

    def _card(self, parent, title):
        """Membuat card dengan judul."""
        frame = tk.LabelFrame(parent, text=title, bg=BG_CARD, fg=ACCENT,
                              font=("Consolas", 9, "bold"),
                              bd=1, relief="groove", padx=6, pady=6)
        frame.pack(fill="x", pady=(0, 8))
        return frame

    def _on_reset(self):
        self.ax.clear()
        self.ax.set_facecolor(BG_PANEL)
        self.ax.set_title("Perkembangan Nilai Fitness", color=TEXT_LIGHT, fontsize=10)
        self.ax.set_xlabel("Generasi", color=TEXT_DIM)
        self.ax.set_ylabel("Fitness", color=TEXT_DIM)
        self.ax.tick_params(colors=TEXT_DIM)
        self.canvas.draw()

        self.lbl_keuntungan.config(text="Keuntungan : -")
        self.lbl_ukuran.config(text="Ukuran Pakai: -")
        self.lbl_barang.config(text="Barang: -")
        self.progress_var.set(0)
        self.lbl_progress.config(text="")
        self._log_clear()

    def _on_run(self):
        """Validasi parameter lalu jalankan GA di thread terpisah."""
        try:
            jumlah_generasi = int(self.param_vars["jumlah_generasi"].get())
            jumlah_populasi = int(self.param_vars["jumlah_populasi"].get())
            prob_crossover  = float(self.param_vars["prob_crossover"].get())
            prob_mutasi     = float(self.param_vars["prob_mutasi"].get())
        except ValueError:
            messagebox.showerror("Input Salah", "Pastikan semua parameter diisi dengan angka yang benar.")
            return

        if not (0 < jumlah_generasi <= 500):
            messagebox.showerror("Input Salah", "Jumlah Generasi harus antara 1 - 500.")
            return
        if not (2 <= jumlah_populasi <= 200):
            messagebox.showerror("Input Salah", "Ukuran Populasi harus antara 2 - 200.")
            return
        if not (0 < prob_crossover <= 1):
            messagebox.showerror("Input Salah", "Probabilitas Crossover harus antara 0 - 1.")
            return
        if not (0 < prob_mutasi <= 1):
            messagebox.showerror("Input Salah", "Probabilitas Mutasi harus antara 0 - 1.")
            return

        self.btn_run.config(state="disabled", text="⏳  Berjalan...")
        self._on_reset()
        self._log_write("=== Mulai Algoritma Genetika ===\n", "header")

        # Simpan untuk callback
        self._total_gen = jumlah_generasi
        self._gen_data  = {"best": [], "worst": [], "avg": [], "all": []}

        def callback(gen, best, worst, avg):
            self._gen_data["best"].append(best)
            self._gen_data["worst"].append(worst)
            self._gen_data["avg"].append(avg)
            pct = (gen / self._total_gen) * 100
            self.root.after(0, self._update_progress, gen, best, worst, avg, pct)

        def task():
            result = run_ga(jumlah_generasi, jumlah_populasi,
                            prob_crossover, prob_mutasi,
                            KAPASITAS_GUDANG, callback)
            self.root.after(0, self._on_finish, result)

        threading.Thread(target=task, daemon=True).start()

    def _update_progress(self, gen, best, worst, avg, pct):
        self.progress_var.set(pct)
        self.lbl_progress.config(text=f"Generasi {gen}/{self._total_gen}")
        # Log tiap 5 generasi atau generasi terakhir
        if gen % 5 == 0 or gen == self._total_gen:
            self._log_write(f"Gen {gen:>3}  ", "header")
            self._log_write(f"Best={best:<6}", "best")
            self._log_write(f"  Worst={worst:<6}", "worst")
            self._log_write(f"  Avg={avg:.1f}\n", "avg")

    def _on_finish(self, result):
        best_individu, best_fitness, best_list, worst_list, avg_list, all_fitness = result

        # Hitung info solusi
        selected_items  = [barang[i][0] for i in range(len(best_individu)) if best_individu[i] == 1]
        selected_size   = sum(barang[i][2] for i in range(len(best_individu)) if best_individu[i] == 1)

        self.lbl_keuntungan.config(text=f"Keuntungan : {best_fitness}")
        self.lbl_ukuran.config(text=f"Ukuran Pakai: {selected_size} / {KAPASITAS_GUDANG}")
        self.lbl_barang.config(text="Barang: " + ", ".join(selected_items) if selected_items else "Tidak ada")

        # Update grafik
        gens = range(1, len(best_list) + 1)
        self.ax.clear()
        self.ax.set_facecolor(BG_PANEL)

        # Scatter semua fitness (transparan)
        for i, flist in enumerate(all_fitness):
            self.ax.scatter([i + 1] * len(flist), flist, color="gray", alpha=0.08, s=8)

        self.ax.plot(gens, best_list,  color=GREEN_C,  linewidth=1.8, label="Tertinggi")
        self.ax.plot(gens, worst_list, color=RED_C,    linewidth=1.5, label="Terendah", linestyle="--")
        self.ax.plot(gens, avg_list,   color=YELLOW_C, linewidth=1.5, label="Rata-rata", linestyle="-.")

        self.ax.set_title("Perkembangan Nilai Fitness", color=TEXT_LIGHT, fontsize=10)
        self.ax.set_xlabel("Generasi", color=TEXT_DIM)
        self.ax.set_ylabel("Nilai Fitness (Keuntungan)", color=TEXT_DIM)
        self.ax.tick_params(colors=TEXT_DIM)
        self.ax.legend(facecolor=BG_CARD, edgecolor=ACCENT, labelcolor=TEXT_LIGHT, fontsize=8)
        self.ax.grid(True, color=BG_CARD, linewidth=0.5)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(BG_CARD)

        self.canvas.draw()

        # Log hasil akhir
        self._log_write("\n=== SELESAI ===\n", "header")
        self._log_write(f"Keuntungan Maks : {best_fitness}\n", "best")
        self._log_write(f"Ukuran Terpakai : {selected_size}/{KAPASITAS_GUDANG}\n", "avg")
        self._log_write(f"Barang Terpilih : {', '.join(selected_items)}\n", "best")

        self.btn_run.config(state="normal", text="▶  Jalankan GA")
        self.progress_var.set(100)

    def _log_write(self, text, tag=None):
        self.log_text.config(state="normal")
        if tag:
            self.log_text.insert("end", text, tag)
        else:
            self.log_text.insert("end", text)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _log_clear(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeneticAlgorithmApp(root)
    root.mainloop()