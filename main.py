from model_controller_sakeu import kontroller, MASUKAN, KELUARAN, KATEGORI_KELUARAN
import tkinter as tk
from tkinter import ttk
from view_sakeu import TabDashboard, TabRiwayat, DialogTambahTransaksi, DialogTarget, buat_tombol


# APLIKASI UTAMA
class AplikasiKeuangan(tk.Tk):
    def __init__(self):
        super().__init__()
        self.kontroller = kontroller()
        self.title("SAKU")
        self.configure(bg="#f0f0f0")
        self.geometry("900x650")
        self.minsize(800, 550)
        self._buat_ui()

    def _buat_ui(self):
        # Menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        menu_transaksi = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Transaksi", menu=menu_transaksi)
        menu_transaksi.add_command(label="Tambah Transaksi", command=self._buka_tambah)
        menu_transaksi.add_command(label="Atur Target", command=self._buka_target)
        menu_transaksi.add_separator()
        menu_transaksi.add_command(label="Keluar", command=self.quit)

        # Notebook untuk tab
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_dashboard = TabDashboard(self.notebook, self.kontroller)
        self.notebook.add(self.tab_dashboard, text=" Dashboard")

        self.tab_riwayat = TabRiwayat(self.notebook, self.kontroller, self._refresh_semua)
        self.notebook.add(self.tab_riwayat, text="Riwayat")

        # Tombol cepat
        frame_tombol = tk.Frame(self, bg="#f0f0f0")
        frame_tombol.pack(fill="x", padx=10, pady=(0, 10))
        buat_tombol(frame_tombol, "Tambah Transaksi", self._buka_tambah, "#3498db", "white").pack(side="left", padx=5)
        buat_tombol(frame_tombol, "Atur Target", self._buka_target, "#f39c12", "white").pack(side="left", padx=5)

    def _buka_tambah(self):
        DialogTambahTransaksi(self, self.kontroller, self._refresh_semua)

    def _buka_target(self):
        lap = self.kontroller.buat_laporan()
        target = lap["progres_tabungan"]["target"]
        DialogTarget(self, self.kontroller, target, self._refresh_semua)

    def _refresh_semua(self):
        self.tab_dashboard.refresh()
        self.tab_riwayat.refresh()

if __name__ == "__main__":
    app = AplikasiKeuangan()
    app.mainloop()