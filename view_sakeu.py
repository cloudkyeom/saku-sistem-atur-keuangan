import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
from model_controller_sakeu import kontroller, MASUKAN, KELUARAN, KATEGORI_KELUARAN

def format_rp(nilai):
    return f"Rp {nilai:,.0f}".replace(",", ".")

def buat_tombol(parent, teks, aksi, warna_bg="#f0f0f0", warna_fg="#333"):
    return tk.Button(parent, text=teks, command=aksi, bg=warna_bg, fg=warna_fg,
                     font=("Arial", 10), relief=tk.RAISED, padx=10, pady=5, cursor="hand2")

# tambah transaksi
class DialogTambahTransaksi(tk.Toplevel):
    def __init__(self, parent, kontroller, selesai_cb):
        super().__init__(parent)
        self.kontroller = kontroller
        self.selesai_cb = selesai_cb
        self.title("Tambah Transaksi")
        self.configure(bg="#f5f5f5")
        self.resizable(False, False)
        self.grab_set()
        self._buat_ui()
        self.geometry("400x450")
        self._tengah(parent)

    def _tengah(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _buat_ui(self):
        main = tk.Frame(self, bg="#f5f5f5", padx=20, pady=15)
        main.pack(fill="both", expand=True)

        tk.Label(main, text="Tambah Transaksi Baru", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=(0, 15))

        # Jenis Transaksi
        tk.Label(main, text="Jenis Transaksi", font=("Arial", 12, "bold"), bg="#f5f5f5", anchor="w").pack(fill="x", pady=(0, 5))
        self.var_jenis = tk.StringVar(value=MASUKAN)
        frame_jenis = tk.Frame(main, bg="#f5f5f5")
        frame_jenis.pack(fill="x", pady=(0, 10))
        tk.Radiobutton(frame_jenis, text="Pemasukan", variable=self.var_jenis, value=MASUKAN,
                       bg="#f5f5f5", command=self._update_kategori).pack(side="left", padx=5)
        tk.Radiobutton(frame_jenis, text="Pengeluaran", variable=self.var_jenis, value=KELUARAN,
                       bg="#f5f5f5", command=self._update_kategori).pack(side="left", padx=5)

        # Nominal
        tk.Label(main, text="Nominal (Rp)", font=("Arial", 12, "bold"), bg="#f5f5f5", anchor="w").pack(fill="x", pady=(0, 5))
        self.ent_jumlah = tk.Entry(main, font=("Arial", 10), width=30)
        self.ent_jumlah.pack(fill="x", pady=(0, 10))

        # Kategori
        tk.Label(main, text="Kategori", font=("Arial", 12, "bold"), bg="#f5f5f5", anchor="w").pack(fill="x", pady=(0, 5))
        self.var_kat = tk.StringVar()
        self.cmb_kat = ttk.Combobox(main, textvariable=self.var_kat, state="readonly", width=28)
        self.cmb_kat.pack(fill="x", pady=(0, 10))
        self._update_kategori()

        # Catatan
        tk.Label(main, text="Catatan (opsional)", font=("Arial", 12, "bold"), bg="#f5f5f5", anchor="w").pack(fill="x", pady=(0, 5))
        self.ent_catatan = tk.Entry(main, font=("Arial", 10), width=30)
        self.ent_catatan.pack(fill="x", pady=(0, 10))

        # Tanggal
        tk.Label(main, text=f"Tanggal: {date.today().strftime('%d %B %Y')}",
                 font=("Arial", 9), bg="#f5f5f5", fg="#666").pack(pady=(5, 15))

        # Tombol
        frame_tombol = tk.Frame(main, bg="#f5f5f5")
        frame_tombol.pack(fill="x")
        buat_tombol(frame_tombol, "Batal", self.destroy, "#e74c3c", "white").pack(side="left", padx=5)
        buat_tombol(frame_tombol, "Simpan", self._simpan, "#2ecc71", "white").pack(side="right", padx=5)

    def _update_kategori(self):
        # KATEGORI_KELUARAN, buat manual untuk pemasukan
        if self.var_jenis.get() == MASUKAN:
            daftar = ["beasiswa", "kiriman", "freelance", "lain-lain"]
        else:
            daftar = sorted(KATEGORI_KELUARAN)
        self.cmb_kat["values"] = daftar
        self.var_kat.set(daftar[0])

    def _simpan(self):
        try:
            jumlah = float(self.ent_jumlah.get().strip())
            if jumlah <= 0:
                raise ValueError("Nominal harus lebih dari 0!")
        except ValueError:
            messagebox.showerror("Error", "Nominal harus berupa angka positif!", parent=self)
            return

        catatan = self.ent_catatan.get().strip()
        try:
            self.kontroller.tambah_transaksi(
                self.var_jenis.get(), jumlah, self.var_kat.get(), catatan
            )
            self.selesai_cb()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

class DialogTarget(tk.Toplevel):
    def __init__(self, parent, kontroller, target_saat_ini, selesai_cb):
        super().__init__(parent)
        self.kontroller = kontroller
        self.selesai_cb = selesai_cb
        self.title("Atur Target")
        self.configure(bg="#f5f5f5")
        self.resizable(False, False)
        self.grab_set()
        self.geometry("350x200")
        self._tengah(parent)
        self._buat_ui(target_saat_ini)

    def _tengah(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _buat_ui(self, target_saat_ini):
        main = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main.pack(fill="both", expand=True)

        tk.Label(main, text="Target Tabungan", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=(0, 15))
        tk.Label(main, text="Masukkan target tabungan (Rp):", font=("Arial", 10), bg="#f5f5f5").pack(anchor="w")

        self.ent_target = tk.Entry(main, font=("Arial", 12, "bold"), width=25)
        self.ent_target.pack(pady=10)
        self.ent_target.insert(0, str(int(target_saat_ini)))

        frame_tombol = tk.Frame(main, bg="#f5f5f5")
        frame_tombol.pack(fill="x", pady=(10, 0))
        buat_tombol(frame_tombol, "Batal", self.destroy, "#e74c3c", "white").pack(side="left", padx=5)
        buat_tombol(frame_tombol, "Simpan", self._simpan, "#2ecc71", "white").pack(side="right", padx=5)

    def _simpan(self):
        try:
            jml = float(self.ent_target.get().strip())
            if jml < 0:
                raise ValueError("Target tidak boleh negatif!")
            self.kontroller.atur_target(jml)
            self.selesai_cb()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

class TabDashboard(tk.Frame):
    def __init__(self, parent, kontroller):
        super().__init__(parent, bg="#f0f0f0")
        self.kontroller = kontroller
        self._buat_ui()

    def _buat_ui(self):
        # Header
        header = tk.Frame(self, bg="#34495e", height=80)
        header.pack(fill="x")
        tk.Label(header, text="SAKU", font=("Arial", 18, "bold"),
                 bg="#34495e", fg="white").pack(side="left", padx=20, pady=20)
        tk.Label(header, text=date.today().strftime("%A, %d %B %Y"),
                 font=("Arial", 9), bg="#34495e", fg="#bdc3c7").pack(side="right", padx=20)

        # Frame kartu ringkasan
        frame_kartu = tk.Frame(self, bg="#f0f0f0", pady=15)
        frame_kartu.pack(fill="x", padx=20)

        for i in range(3):
            frame_kartu.columnconfigure(i, weight=1)

        self.saldo_card = self._buat_kartu(frame_kartu, "Total Saldo", "Rp 0", "#2ecc71", 0, 0)
        self.pemasukan_card = self._buat_kartu(frame_kartu, "Pemasukan", "Rp 0", "#2ecc71", 1, 0)
        self.pengeluaran_card = self._buat_kartu(frame_kartu, "Pengeluaran", "Rp 0", "#e74c3c", 2, 0)

        # Frame target
        self.frame_target = tk.Frame(self, bg="white", bd=1, relief=tk.RIDGE)
        self.frame_target.pack(fill="x", padx=20, pady=10)

        # Frame ringkasan kategori
        self.frame_kategori = tk.Frame(self, bg="#f0f0f0")
        self.frame_kategori.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh()

    def _buat_kartu(self, parent, judul, nilai, warna, kolom, baris):
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.RIDGE)
        frame.grid(row=baris, column=kolom, padx=5, pady=5, sticky="nsew")
        tk.Label(frame, text=judul, font=("Arial", 10), bg="white").pack(pady=(10, 0))
        lbl_nilai = tk.Label(frame, text=nilai, font=("Arial", 16, "bold"), bg="white", fg=warna)
        lbl_nilai.pack(pady=(0, 10))
        return lbl_nilai

    def refresh(self):
        lap = self.kontroller.buat_laporan()
        saldo = lap["saldo"]
        warna_saldo = "#2ecc71" if saldo >= 0 else "#e74c3c"

        self.saldo_card.config(text=format_rp(saldo), fg=warna_saldo)
        self.pemasukan_card.config(text=format_rp(lap["pemasukan"]), fg="#2ecc71")
        self.pengeluaran_card.config(text=format_rp(lap["pengeluaran"]), fg="#e74c3c")

        # Update target
        for w in self.frame_target.winfo_children():
            w.destroy()

        prog = lap["progres_tabungan"]
        tk.Label(self.frame_target, text="🎯 Progres Target Tabungan",
                 font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=(10, 5))
        tk.Label(self.frame_target, text=f"Saldo: {format_rp(prog['saldo'])} | Target: {format_rp(prog['target'])}",
                 font=("Arial", 10), bg="white").pack(anchor="w", padx=10)

        # Progress bar
        frame_progress = tk.Frame(self.frame_target, bg="white", height=20)
        frame_progress.pack(fill="x", padx=10, pady=(5, 10))
        canvas = tk.Canvas(frame_progress, height=20, bg="#ecf0f1", highlightthickness=0)
        canvas.pack(fill="x")
        canvas.update_idletasks()
        lebar = canvas.winfo_width() or 500
        persen = prog["persen"] / 100
        if persen > 0:
            warna = "#2ecc71" if persen < 1 else "#f39c12"
            canvas.create_rectangle(0, 0, int(lebar * persen), 20, fill=warna, outline="")
        tk.Label(self.frame_target, text=f"{prog['persen']:.1f}% tercapai",
                 font=("Arial", 9), bg="white", fg="#666").pack(anchor="e", padx=10, pady=(0, 10))

        # Update ringkasan kategori
        for w in self.frame_kategori.winfo_children():
            w.destroy()

        tk.Label(self.frame_kategori, text="Pengeluaran per Kategori",
                 font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(0, 10))

        ringkas = lap["ringkasan_pengeluaran"]
        total = sum(ringkas.values()) or 1
        grid = tk.Frame(self.frame_kategori, bg="#f0f0f0")
        grid.pack(fill="x")

        for idx, (kat, jml) in enumerate(sorted(ringkas.items(), key=lambda x: x[1], reverse=True)):
            baris = idx // 2
            kolom = idx % 2
            persen = jml / total * 100
            frame = tk.Frame(grid, bg="white", bd=1, relief=tk.RIDGE)
            frame.grid(row=baris, column=kolom, padx=5, pady=5, sticky="ew")
            grid.columnconfigure(kolom, weight=1)

            tk.Label(frame, text=f"{kat.capitalize()}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", padx=10, pady=(5, 0))
            tk.Label(frame, text=f"{format_rp(jml)} ({persen:.1f}%)",
                     font=("Arial", 10), bg="white", fg="#e74c3c" if jml > 0 else "#666").pack(anchor="w", padx=10, pady=(0, 5))

# tab riwayat transaksi
class TabRiwayat(tk.Frame):
    def __init__(self, parent, kontroller, refresh_cb):
        super().__init__(parent, bg="#f0f0f0")
        self.kontroller = kontroller
        self.refresh_cb = refresh_cb
        self._buat_ui()

    def _buat_ui(self):
        # Toolbar
        toolbar = tk.Frame(self, bg="#34495e", height=50)
        toolbar.pack(fill="x")
        tk.Label(toolbar, text="📋 Riwayat Transaksi", font=("Arial", 12, "bold"),
                 bg="#34495e", fg="white").pack(side="left", padx=15, pady=10)

        # Filter
        self.var_filter = tk.StringVar(value="semua")
        frame_filter = tk.Frame(toolbar, bg="#34495e")
        frame_filter.pack(side="right", padx=15)
        for text, val in [("Semua", "semua"), ("Pemasukan", MASUKAN), ("Pengeluaran", KELUARAN)]:
            tk.Radiobutton(frame_filter, text=text, variable=self.var_filter, value=val,
                           bg="#34495e", fg="white", selectcolor="#34495e", command=self.refresh).pack(side="left", padx=5)

        # Tabel
        frame_tabel = tk.Frame(self, bg="#f0f0f0")
        frame_tabel.pack(fill="both", expand=True, padx=15, pady=10)

        scroll_y = tk.Scrollbar(frame_tabel)
        scroll_y.pack(side="right", fill="y")

        self.tree = ttk.Treeview(frame_tabel, yscrollcommand=scroll_y.set, height=15)
        scroll_y.config(command=self.tree.yview)

        kolom = ("tanggal", "jenis", "kategori", "jumlah", "catatan", "id")
        self.tree["columns"] = kolom
        self.tree["show"] = "headings"

        lebar_kolom = {"tanggal": 100, "jenis": 90, "kategori": 120, "jumlah": 120, "catatan": 200, "id": 0}
        judul_kolom = {"tanggal": "Tanggal", "jenis": "Jenis", "kategori": "Kategori", "jumlah": "Nominal", "catatan": "Catatan", "id": ""}

        for kol in kolom:
            self.tree.heading(kol, text=judul_kolom[kol])
            self.tree.column(kol, width=lebar_kolom[kol], anchor="center")
        self.tree.column("catatan", anchor="w")
        self.tree.column("id", width=0, stretch=False)  # Sembunyikan kolom ID

        self.tree.pack(fill="both", expand=True)

        # Tombol hapus
        frame_hapus = tk.Frame(self, bg="#f0f0f0")
        frame_hapus.pack(fill="x", padx=15, pady=10)
        self.btn_hapus = buat_tombol(frame_hapus, "🗑 Hapus Transaksi Terpilih", self._hapus, "#e74c3c", "white")
        self.btn_hapus.pack()

        self.tree.bind("<<TreeviewSelect>>", self._simpan_id)
        self._id_terpilih = None
        self.refresh()

    def _simpan_id(self, event):
        seleksi = self.tree.selection()
        if seleksi:
            self._id_terpilih = self.tree.item(seleksi[0], "values")[-1]
        else:
            self._id_terpilih = None

    def _hapus(self):
        if not self._id_terpilih:
            messagebox.showwarning("Perhatian", "Pilih transaksi yang ingin dihapus!")
            return
        if messagebox.askyesno("Konfirmasi", "Hapus transaksi ini?"):
            try:
                self.kontroller.hapus_transaksi(self._id_terpilih)
                self.refresh()
                self.refresh_cb()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        lap = self.kontroller.buat_laporan()
        filter_val = self.var_filter.get()

        for t in lap["riwayat_transaksi"]:
            if filter_val != "semua" and t["jenis"] != filter_val:
                continue
            jenis_label = " Masuk" if t["jenis"] == MASUKAN else "Keluar"
            self.tree.insert("", "end", values=(
                t["tanggal"],
                jenis_label,
                t["kategori"].capitalize(),
                format_rp(t["jumlah"]),
                t["catatan"] or "-",
                t["id"]
            ))

