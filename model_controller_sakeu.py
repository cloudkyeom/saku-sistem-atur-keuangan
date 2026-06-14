import json
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

MASUKAN, KELUARAN = "pemasukan", "pengeluaran"
KATEGORI_KELUARAN = {"makan", "belanja", "laundry", "jajan", "akademik", "lain-lain"}

class Transaksi:
    def __init__(self, id, jenis, jumlah, kategori, catatan, tanggal, dibuat_pada):
        self.id = id
        self.jenis = jenis
        self.jumlah = jumlah
        self.kategori = kategori
        self.catatan = catatan
        self.tanggal = tanggal
        self.dibuat_pada = dibuat_pada

    @classmethod
    def buat_transaksi(cls, jenis, jumlah, kategori, catatan=""):
        if float(jumlah) <= 0: raise ValueError("Nominal harus lebih dari 0!")
        kategori = kategori.lower().strip()
        if jenis == KELUARAN and kategori not in KATEGORI_KELUARAN:
            raise ValueError(f"Kategori tidak tersedia!")
        
        return cls(id=str(uuid4()), jenis=jenis, jumlah=float(jumlah), kategori=kategori, 
                   catatan=catatan.strip(), tanggal=date.today().isoformat(), dibuat_pada=datetime.now().isoformat())

    def ke_kamus(self): return self.__dict__


# Model
class Model:
    def __init__(self, nama_file="data_keuangan.json"):
        self.berkas = Path(nama_file)
        
    def muat_data(self):
        if not self.berkas.exists(): 
            return {"target": 0.0, "transaksi": []}
        return json.loads(self.berkas.read_text(encoding="utf-8"))
        
    def simpan_data(self, data):
        self.berkas.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# Kontroller
class kontroller:
    def __init__(self, model=None):
        self.model = model or Model()

    def tambah_transaksi(self, jenis, jml, kat, cat=""):
        data = self.model.muat_data()
        trx_baru = Transaksi.buat_transaksi(jenis, jml, kat, cat)
        
        data["transaksi"].append(trx_baru.ke_kamus())
        self.model.simpan_data(data)

    def hapus_transaksi(self, id_trx):
        data = self.model.muat_data()
        jumlah_awal = len(data["transaksi"])
        
        data["transaksi"] = [t for t in data["transaksi"] if t["id"] != id_trx]
        if len(data["transaksi"]) == jumlah_awal: 
            raise ValueError("ID tidak ditemukan")
            
        self.model.simpan_data(data)

    def atur_target(self, jml):
        if jml < 0: raise ValueError("Target tidak bisa minus!")
        data = self.model.muat_data()
        data["target"] = float(jml)
        self.model.simpan_data(data)
    
    # Ini bisa jadi format view tapi nanti difinishing sama roro pas bikin GUI, tolong ya 
    def buat_laporan(self):
        data = self.model.muat_data()
        target = data["target"]
        
        riwayat = sorted(data["transaksi"], key=lambda t: t["tanggal"], reverse=True)
        
        masuk = sum(t["jumlah"] for t in riwayat if t["jenis"] == MASUKAN)
        keluar = sum(t["jumlah"] for t in riwayat if t["jenis"] == KELUARAN)
        saldo = masuk - keluar

        ringkas = {k: 0.0 for k in KATEGORI_KELUARAN}
        for t in riwayat:
            if t["jenis"] == KELUARAN:
                ringkas[t["kategori"]] += t["jumlah"]

        return {
            "saldo": saldo, "pemasukan": masuk, "pengeluaran": keluar,
            "progres_tabungan": {"target": target, "saldo": saldo, "persen": 0.0 if target == 0 else min(saldo / target * 100, 100)},
            "ringkasan_pengeluaran": ringkas, 
            "riwayat_transaksi": riwayat
        }
    
