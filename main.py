"""Sistem pakar risiko kompor gas portabel (kaleng butana) dengan forward chaining.
Mesin inferensi ditulis sendiri, tanpa library sistem pakar."""

import json
import sys

fileKB = "kb_kompor.json"

def bacaKB(path=fileKB):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def syaratTerpenuhi(aturan, memori):
    ada = [s in memori for s in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)

def faktaDasar(kb):
    hasil = {r["maka"] for r in kb["aturan"]}
    urut = []
    for r in kb["aturan"]:
        for s in r["jika"]:
            if s not in hasil and s not in urut:
                urut.append(s)
    return urut

def kesimpulanAkhir(kb, asal):
    dipakai = {s for r in kb["aturan"] for s in r["jika"]}
    return [f for f in asal if f not in dipakai]

def forwardChaining(kb, fakta_awal):
    memori = set(fakta_awal)
    asal = {}  
    log = []   
    siklus = 0
    while True:
        cocok = [r for r in kb["aturan"]
                 if syaratTerpenuhi(r, memori) and r["maka"] not in memori]
        if not cocok:
            break
        siklus += 1
        r = cocok[0]
        memori.add(r["maka"])
        asal[r["maka"]] = r
        log.append((siklus, r))
    return memori, asal, log

def tulisAlasan(fakta, asal, memori, tingkat=1):
    r = asal[fakta]
    terpakai = [s for s in r["jika"] if s in memori]
    print("  " * tingkat + f"{fakta}  <- {r['id']} ({', '.join(terpakai)}) [{r['sumber']}]")
    for s in terpakai:
        if s in asal:
            tulisAlasan(s, asal, memori, tingkat + 1)

def show(kb, fakta_awal):
    memori, asal, log = forwardChaining(kb, fakta_awal)
    print("\nFakta awal:", ", ".join(sorted(fakta_awal)) if fakta_awal else "(tidak ada)")
    print()
    for siklus, r in log:
        print(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
    print(f"Siklus {len(log) + 1}: tidak ada aturan baru, berhenti")
    akhir = kesimpulanAkhir(kb, asal)
    print()
    if not akhir:
        print("Kesimpulan: tidak ada kesimpulan dari fakta yang diberikan")
    else:
        print("Kesimpulan:", "; ".join(akhir))
        print("Alasan:")
        for k in akhir:
            tulisAlasan(k, asal, memori)
    print("\nCatatan:", kb["batas"])
    return akhir

def ask(kb):
    print(kb["judul"])
    print("Jawab y/t.")
    ya = []
    for i, f in enumerate(faktaDasar(kb), 1):
        while True:
            j = input(f"{i}. Apakah {f}? (y/t) > ").strip().lower()
            if j in ("y", "t"):
                break
            print("   Ketik y atau t.")
        if j == "y":
            ya.append(f)
    return ya

if __name__ == "__main__":
    kb = bacaKB()
    if len(sys.argv) > 1 and sys.argv[1] == "--ya":
        
        dasar = faktaDasar(kb)
        nomor = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[2] else []
        show(kb, [dasar[n - 1] for n in nomor])
    else:
        show(kb, ask(kb))
