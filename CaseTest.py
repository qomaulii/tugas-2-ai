"""Pengujian otomatis untuk sistem pakar kompor butana.
Menjalankan forward chaining pada beberapa kasus lalu membandingkan
kesimpulan akhir dengan hasil yang diharapkan."""
from main import bacaKB, forwardChaining, kesimpulanAkhir

JANGAN_NYALA = "jangan nyalakan kompor sebelum bau hilang dan periksa regulator"

KASUS = [
    ("Kasus 1 (README): kebocoran, aksesori rusak, kompor kotor",
     ["tercium bau gas", "terdengar bunyi mendesis", "selang getas atau rusak",
      "tabung berkarat atau penyok", "kompor kotor oleh sisa masakan"],
     {"komponen perlu diganti", JANGAN_NYALA, "kompor perlu dibersihkan"}),
    ("Kasus 2 (README): kasus negatif",
     ["ada api atau sumber panas"],
     set()),
    ("Kasus 3 (README): komponen rusak dan penempatan tidak aman",
     ["selang getas atau rusak", "tabung berkarat atau penyok",
      "kompor tidak berada di permukaan datar"],
     {"komponen perlu diganti", "penempatan tidak aman"}),
    ("Tambahan: rantai R1, R3, R4 (ruang tertutup dan ada api)",
     ["tercium bau gas", "ruang tertutup tanpa ventilasi", "ada api atau sumber panas"],
     {"risiko ledakan atau kebakaran tinggi", JANGAN_NYALA}),
    ("Tambahan: burner tidak menyala tetapi gas keluar",
     ["api tidak menyala tetapi gas terus keluar", "ruang tertutup tanpa ventilasi",
      "ada api atau sumber panas"],
     {"risiko ledakan atau kebakaran tinggi", JANGAN_NYALA}),
]

def jalankan():
    kb = bacaKB()
    lulus = 0
    for nama, fakta, harapan in KASUS:
        _, asal, _ = forwardChaining(kb, fakta)
        hasil = set(kesimpulanAkhir(kb, asal))
        ok = hasil == harapan
        lulus += ok
        print(("LULUS" if ok else "GAGAL"), "-", nama)
        if not ok:
            print("   diharapkan:", harapan or "tidak ada")
            print("   didapat   :", hasil or "tidak ada")
    print(f"\n{lulus} dari {len(KASUS)} kasus lulus")


if __name__ == "__main__":
    jalankan()
