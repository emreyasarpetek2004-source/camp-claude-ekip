#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bir dersi uçtan uca kurgular: indir → ölç → çöz → kes → üret → denetle → teslim.

(21.09.2026 kararı: "hayır önüme getirme hepsini ... sen dikkat et")
Kesim kararları otonom verilir. İlke: EMİN DEĞİLSEN KESME.

Kullanım:
    python3 bin/hat.py <loom_vid>            # tek ders
    python3 bin/hat.py <loom_vid> --kuru     # indirme+kurgu yok, sadece plan
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

KOK = os.path.expanduser("~/camp-video")
INDIR = os.path.expanduser("~/Downloads/CAMPVERSE Dersler")
EN_AZ_HAM_DISK_GB = 10   # bunun altina inerse en ESKI ham dosyalar silinir
BIN = os.path.join(KOK, "bin")
VENV = os.path.expanduser("~/Developer/video-use/.venv/bin/python")
YTDLP = os.path.expanduser("~/.local/bin/yt-dlp")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
OPENER = os.path.join(KOK, "brand/campverse/opener.mp4")
EN_AZ_DISK_GB = 8


def kos(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def disk_gb():
    s = os.statvfs(os.path.expanduser("~"))
    return s.f_bavail * s.f_frsize / 1e9


def slug(m):
    m = re.sub(r"[^A-Za-z0-9]+", "-", (m or "")).strip("-").lower()
    return m[:48] or "ders"


def kayit_bul(vid):
    d = json.load(open(os.path.join(KOK, "takip/ders_kayitlari.json")))
    for k in d["kayit"]:
        if k["loom_vid"].startswith(vid):
            return k
    return None


def bolum_bul(vid):
    try:
        lm = json.load(open(os.path.join(KOK, "takip/dersler.json")))
    except Exception:
        return None
    for x in lm:
        if x["vid"].startswith(vid) and x.get("no"):
            return x
    return None


def ince_bosluklar(video, t, yaricap=5.0, esik=-30, en_kisa=0.06):
    """Dar bir pencerede KELIME ARASI boslukları bulur.

    Kaba harita (esik -35 dB, en az 0.30 sn) olu zamani bulmak icin. Ama konusma
    akiyorsa oralarda 0.30 sn'lik bosluk yoktur; kelimeler arasi bosluk 0.08-0.15 sn'dir.
    (22.09.2026 olcumu: CH01'de 5 sinirin en yakin kaba boslugu 4-10 sn uzaktaydi.)
    """
    bas = max(0.0, t - yaricap)
    p = subprocess.run([FFMPEG, "-nostats", "-v", "info", "-ss", "%.3f" % bas,
                        "-t", "%.3f" % (yaricap * 2), "-i", video, "-af",
                        "silencedetect=noise=%ddB:d=%s" % (esik, en_kisa),
                        "-f", "null", "-"], capture_output=True, text=True)
    out, acik = [], None
    for satir in (p.stderr or "").splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", satir)
        if m:
            acik = float(m.group(1)) + bas
            continue
        m = re.search(r"silence_end:\s*([\d.]+)", satir)
        if m and acik is not None:
            out.append({"bas": acik, "bit": float(m.group(1)) + bas,
                        "sure": float(m.group(1)) + bas - acik})
            acik = None
    return out


def acilis_slayt_degisimi(video, pencere=12.0, esik=0.10):
    """Dersin basinda hoca slaytlar arasinda geziniyorsa, yerine oturdugu ani bulur.

    (22.09.2026 kararı: "en basinda hocanin slaytlari inceledigi bir kisim var onu
     kesmemissin" - CH03'te ilk 3 saniye dersin ilerisinden bir slayt duruyordu.)

    Yalniz ILK saniyelerdeki degisim sayilir: 12 sn'den sonraki degisim normal slayt
    ilerlemesidir, kesilmez.
    """
    p = subprocess.run([FFMPEG, "-nostats", "-v", "error", "-t", "%.1f" % (pencere + 3),
                        "-i", video, "-vf",
                        "select='gt(scene,%.2f)',metadata=print:file=-" % esik,
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    anlar = [float(m) for m in re.findall(r"pts_time:([\d.]+)", p.stdout or "")]
    anlar = [t for t in anlar if 0.3 <= t <= pencere]
    return max(anlar) if anlar else None


def sinira_otur(kesimler, bosluklar, pencere=2.5, pay=0.08, video=None, kullanilan=None,
                dusen=None):
    """Her kesim sinirini en yakin SESSIZLIGE oturtur.

    (22.09.2026: CH01 denetimde G7'den kaldi. Tasarimda "sinir sessizlikten gelir"
     yaziyordu ama kodda hizalama yoktu; sinirlar transkript zaman damgasindan
     geliyordu. Transkript damgasi kaba, tam kelime sinirinda degil.)

    Kesimin BASI: oncesindeki bosluga; SONU: sonrasindaki bosluga oturur.
    Boylece birlesme yerinde kelime kesilmez, tik sesi olmaz.
    """
    out = []
    genis = pencere
    for k in kesimler:
        bas, bit = float(k["bas"]), float(k["bit"])
        # Kelime zamanli dogrulamadan gelen sinir ("kesin") yalniz kelime arasi
        # bosluga oynatilir; 2,5 sn'lik pencere temiz cumlenin basini yutuyordu.
        # (05.10.2026: CH70 talimat kesimi "Simdi burada dermatolojik emergency'ler
        #  var" cumlesini, CH61 kesimi dogru dozu goturmustu.)
        pencere = 0.2 if k.get("kesin") else genis
        if k.get("kesin") and video:
            # Kesin sinirda once KELIME ARASI ince bosluk aranir; kaba haritadaki
            # uzak bir sessizlige ziplamak kelime yutuyordu (CH02, 05.10.2026:
            # 421.06 -> 420.65 "dusunurum"un sonunu kesiyordu).
            ib = [b for b in ince_bosluklar(video, bas) if b["bas"] - 0.2 <= bas <= b["bit"] + 0.2]
            ie = [b for b in ince_bosluklar(video, bit) if b["bas"] - 0.2 <= bit <= b["bit"] + 0.2]
            if ib:
                b = min(ib, key=lambda b: abs((b["bas"] + b["bit"]) / 2 - bas))
                bas = round(min(max(bas, b["bas"] + 0.02), b["bit"] - 0.02), 3) if b["bit"] - b["bas"] > 0.04 else round((b["bas"] + b["bit"]) / 2, 3)
            if ie:
                b = min(ie, key=lambda b: abs((b["bas"] + b["bit"]) / 2 - bit))
                bit = round(min(max(bit, b["bas"] + 0.02), b["bit"] - 0.02), 3) if b["bit"] - b["bas"] > 0.04 else round((b["bas"] + b["bit"]) / 2, 3)
            if bit - bas >= 0.3:
                y = dict(k); y["bas"], y["bit"] = bas, bit
                y["hizalandi"] = (abs(bas - float(k["bas"])) > 0.01 or abs(bit - float(k["bit"])) > 0.01)
                y["ince"] = bool(ib and ie)
                out.append(y)
                continue
        # YON SART: kesimin BASI, kendisinden ONCE baslayan (ya da kendisini iceren) bir
        # bosluga oturur. Yon dayatilmazsa bas ileri kayip sonla ayni bosluga dusuyor ve
        # kesim eriyor. (CH18, 23.09.2026: 2051.6-2054.2 boyle yok olmustu.)
        def _once(b):
            return b["bas"] <= bas + pay

        def _yakin_b(liste):
            return [b for b in liste
                    if abs(b["bit"] - bas) <= pencere or abs(b["bas"] - bas) <= pencere]

        # Once YON tercihli ara. Bulunamazsa yonden vazgecip en yakin bosluga oturt:
        # G7'nin derdi tik sesi ve kelime ortasi kesim, o da hangi yonde olursa olsun
        # sessizlige oturmakla cozuluyor. (CH06, 23.09.2026: yon sarti yuzunden 2442.60
        # hic hizalanamamis ve kapi kalmisti.)
        # Sira onemli: kaba haritada YANLIS yonde bir bosluk bulunursa, ince kelime
        # araligindaki DOGRU yondeki bosluga hic bakilmiyor ve sinir ters yone
        # cekiliyordu. (CH09, 23.09.2026: kesim bitisi 2583.75'ten 2581.9'a geri
        # kayip dikis tekrarini geri getirmisti.) Once yonu dogru olanlar denenir.
        aday_b = [b for b in _yakin_b(bosluklar) if _once(b)]
        _ince_b = None
        if not aday_b and video:
            _ince_b = ince_bosluklar(video, bas)
            aday_b = [b for b in _yakin_b(_ince_b) if _once(b)]
        if not aday_b:
            aday_b = _yakin_b(bosluklar)
        if not aday_b and video:
            _ince_b = _ince_b if _ince_b is not None else ince_bosluklar(video, bas)
            aday_b = _yakin_b(_ince_b)
        if kullanilan is not None and _ince_b:
            kullanilan.extend([b for b in aday_b if b in _ince_b])
        if aday_b:
            b = min(aday_b, key=lambda b: min(abs(b["bit"] - bas), abs(b["bas"] - bas)))
            bas = round(min(b["bit"] - pay, max(b["bas"] + pay, bas)), 3)
            if bas < b["bas"] or bas > b["bit"]:
                bas = round((b["bas"] + b["bit"]) / 2.0, 3)
        # Kesimin SONU, kendisinden SONRA biten (ya da kendisini iceren) bosluga oturur.
        def _sonra(b):
            return b["bit"] >= bit - pay

        def _yakin_e(liste):
            # Kesimin SONU, hizalanmis BASIN gerisine dusemez: yoksa iki uc ayni
            # bosluga oturuyor ve kesim eriyor. (CH13, 23.09.2026: 830.3-831.6
            # "Kalemimi aldim" kesimi boyle kayboluyordu.)
            return [b for b in liste
                    if b["bit"] > bas + 0.4
                    and (abs(b["bas"] - bit) <= pencere or abs(b["bit"] - bit) <= pencere)]

        aday_e = [b for b in _yakin_e(bosluklar) if _sonra(b)]
        _ince_e = None
        if not aday_e and video:
            _ince_e = ince_bosluklar(video, bit)
            aday_e = [b for b in _yakin_e(_ince_e) if _sonra(b)]
        if not aday_e:
            aday_e = _yakin_e(bosluklar)
        if not aday_e and video:
            _ince_e = _ince_e if _ince_e is not None else ince_bosluklar(video, bit)
            aday_e = _yakin_e(_ince_e)
        if kullanilan is not None and _ince_e:
            kullanilan.extend([b for b in aday_e if b in _ince_e])
        if aday_e:
            b = min(aday_e, key=lambda b: min(abs(b["bas"] - bit), abs(b["bit"] - bit)))
            bit = round(max(b["bas"] + pay, min(b["bit"] - pay, bit)), 3)
            if bit < b["bas"] or bit > b["bit"]:
                bit = round((b["bas"] + b["bit"]) / 2.0, 3)
        if bit - bas < 0.4:
            # Sessizce elemek tehlikeli: kesim kayboluyor ama kimse gormuyor.
            # (CH13, 23.09.2026: 830.3-831.6 "Kalemimi aldim" boyle dusmustu.)
            print("  UYARI: kesim sessizlige oturunca eridi, DUSURULDU: %.2f-%.2f (%s)"
                  % (float(k["bas"]), float(k["bit"]), str(k.get("gerekce", ""))[:60]))
            if dusen is not None:
                dusen.append(dict(k))
            continue
        y = dict(k); y["bas"], y["bit"] = bas, bit
        y["hizalandi"] = (abs(bas - float(k["bas"])) > 0.01 or abs(bit - float(k["bit"])) > 0.01)
        out.append(y)
    return out


def talimat_dakikalari(kayit):
    if not kayit or "talimat_cozum" not in kayit:
        return []
    return [p["saniye"] for p in kayit["talimat_cozum"].get("noktalar", [])]


def indirilenlere_koy(dosya, final_yolu, ham_yolu):
    """Kullanıcı takip edebilsin diye editli ve ham halleri Indirilenler'e koyar.

    (22.09.2026 kararı: "benim takip edebilmem icin tum projeyi indirilenlerden yap
     ham halleri ve edit sonrasi halleri")

    Ham dosyalar KOPYALANMAZ, TASINIR: 33 dersin hami ~16 GB, editlisi ~8 GB tutar ve
    diskte o kadar bos alan yok. Ayrica alan daralirsa en ESKI ham dosyalar silinir;
    editli olanlara hicbir zaman dokunulmaz.
    """
    ham_dizin = os.path.join(INDIR, "Ham")
    ed_dizin = os.path.join(INDIR, "Editli")
    os.makedirs(ham_dizin, exist_ok=True)
    os.makedirs(ed_dizin, exist_ok=True)
    subprocess.run(["cp", final_yolu, os.path.join(ed_dizin, dosya)])
    hedef = os.path.join(ham_dizin, dosya.replace(".mp4", " (ham).mp4"))
    if os.path.exists(ham_yolu):
        # TASIMA YOK. Ham proje klasorunde KALIR: brief yeniden basmak, kesim
        # listesini degistirip yeniden uretmek ve sahne taramasi icin gerekiyor.
        # Sabit baglanti ayni inode'u gosterdigi icin ikinci kopya yer tutmaz.
        # (23.09.2026: CH15 dahil 15 dersin hami bu yuzden kaybolmus, brief'ler
        #  0 slayt degisimiyle uretilmisti.)
        if not os.path.exists(hedef):
            try:
                os.link(ham_yolu, hedef)
            except OSError:
                subprocess.run(["cp", ham_yolu, hedef])
    # Alan daralirsa en eski ham dosyalari dus
    try:
        hamlar = sorted((os.path.join(ham_dizin, f) for f in os.listdir(ham_dizin)
                         if f.endswith(".mp4")), key=os.path.getmtime)
        while hamlar and disk_gb() < EN_AZ_HAM_DISK_GB:
            e = hamlar.pop(0)
            os.remove(e)
            print("  (yer acmak icin en eski ham silindi: %s)" % os.path.basename(e))
    except OSError:
        pass


def takibe_isle(bol, vid, fin, edit, ad):
    """Teslim edilen dersi takip defterine yaz (kullanıcı: 'sen ayri bir tabloda tut')."""
    try:
        sure_dk = None
        try:
            r = kos([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", fin])
            sure_dk = int(round(float(r.stdout.strip()) / 60.0))
        except Exception:
            pass
        kesim = 0
        my = os.path.join(edit, "model_kesim.json")
        if os.path.exists(my):
            mk = json.load(open(my))
            for anahtar in ("kesimler", "kesim", "kesim_listesi", "cuts"):
                if isinstance(mk.get(anahtar), list):
                    kesim = len([k for k in mk[anahtar]
                                 if k.get("karar") not in ("atla", "kesme", "reddedildi")])
                    break
        notu = "model kurgusu · %d kesim" % kesim if kesim else "model kurgusu"
        cmd = ["python3", os.path.join(BIN, "takip.py"), "ekle", "--vid", vid,
               "--bolum", (bol or {}).get("chapter", ad), "--not", notu]
        if bol:
            cmd += ["--bolum-no", str(bol["no"])]
            if bol.get("kitap_no"):
                cmd += ["--kitap-no", str(bol["kitap_no"])]
        if sure_dk:
            cmd += ["--sure", str(sure_dk)]
        kos(cmd)
        kos(["python3", os.path.join(BIN, "takip.py"), "kur"])
    except Exception as e:
        print("  (takip defterine yazilamadi: %s)" % e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vid")
    ap.add_argument("--kuru", action="store_true")
    ap.add_argument("--hazirla", action="store_true",
                    help="yalniz indir/olc/coz/EDL yaz (ag + GPU asamasi)")
    ap.add_argument("--indir", action="store_true",
                    help="yalniz indir ve kaynagi dogrula (ag asamasi)")
    ap.add_argument("--uret", action="store_true",
                    help="yalniz uret/denetle/teslim (islemci asamasi)")
    ap.add_argument("--crf", type=int, default=14)
    ap.add_argument("--yalniz-denetim", action="store_true",
                    help="--uret ile: final.mp4 edl.json'dan yeniyse yeniden basmadan denetle + teslim et "
                         "(denetci duzeltildiginde dogru basilmis dersi bosuna yeniden kodlamamak icin)")
    ap.add_argument("--model", action="store_true",
                    help="kesimleri edit/model_kesim.json'dan al (sezgisel dedektorleri atla)")
    a = ap.parse_args()

    t0 = time.time()
    kayit = kayit_bul(a.vid)
    if not kayit:
        sys.exit("HATA: %s takip/ders_kayitlari.json icinde yok" % a.vid)
    vid = kayit["loom_vid"]
    bol = bolum_bul(vid)
    ad = ("CH%02d %s" % (bol["no"], bol["chapter"])) if bol else (kayit["link_tarih"][:10])
    proje = os.path.join(KOK, "projects", "campverse-%s-%s" % (slug(ad), vid[:8]))
    edit = os.path.join(proje, "edit")
    os.makedirs(edit, exist_ok=True)
    ham = os.path.join(proje, "ders.mp4")
    print("=== %s  (%s) ===" % (ad, vid[:8]))

    if disk_gb() < EN_AZ_DISK_GB:
        sys.exit("HATA: disk %.1f GB, en az %d GB gerek" % (disk_gb(), EN_AZ_DISK_GB))

    if a.uret:
        # Hazirlik zaten yapilmis: dogrudan uretime atla
        if not os.path.exists(os.path.join(edit, "edl.json")):
            sys.exit("HATA: edl.json yok, once --hazirla calistirilmali")
        fin = os.path.join(edit, "final.mp4")
        if a.yalniz_denetim and os.path.exists(fin) and os.path.getmtime(fin) > os.path.getmtime(os.path.join(edit, "edl.json")):
            print("  yeniden basilmadi (final.mp4 edl'den yeni), yalniz denetim")
            r = subprocess.CompletedProcess([], 0, "", "")
        else:
            print("  uretiliyor (hazirlik atlandi)...")
            r = kos([VENV, os.path.join(BIN, "olustur.py"), os.path.join(edit, "edl.json"),
                     "-o", os.path.join(edit, "final.mp4"), "--crf", str(a.crf)])
        kontrol = kos([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                       "-of", "csv=p=0", fin])
        if not os.path.exists(fin) or kontrol.returncode != 0 or not kontrol.stdout.strip():
            if os.path.exists(fin):
                os.remove(fin)
            sys.exit("HATA: uretim basarisiz / cikti bozuk\n" + (r.stderr or "")[-400:])
        d = kos(["python3", os.path.join(BIN, "denetle.py"), proje])
        print("  " + "\n  ".join(d.stdout.strip().splitlines()))
        if d.returncode != 0:
            # Sifir kodla donmek kuyrugun bunu "TAMAM" saymasina yol aciyordu; final.mp4
            # kesim listesinden yeni oldugu icin ders bir daha hic denenmezdi ve
            # kilcikli bir edit sessizce teslim edilmis sayilirdi. (23.09.2026)
            open(os.path.join(edit, ".denetim_kaldi"), "w").write(d.stdout)
            sys.exit("DENETIM KALDI, teslim edilmedi")
        try:
            os.remove(os.path.join(edit, ".denetim_kaldi"))
        except OSError:
            pass
        if bol:
            dosya = "%02d - %s.mp4" % (bol["no"], bol["chapter"].strip())
        else:
            dosya = "00 - %s (%s).mp4" % (kayit["link_tarih"][:10].replace(".", "-"), vid[:8])
        dosya = re.sub(r'[/:\\]', "-", dosya)
        tes = os.path.join(KOK, "teslim/campverse", dosya)
        subprocess.run(["cp", fin, tes])
        indirilenlere_koy(dosya, fin, ham)
        takibe_isle(bol, vid, fin, edit, ad)
        print("  TESLIM: %s  ·  %.1f dk" % (dosya, (time.time() - t0) / 60))
        return

    # 1) indir. Onden indirme sürüyorsa ikinci bir indirme BASLATMA, bekle.
    kilit = os.path.join(proje, ".indiriliyor")
    bekle = 0
    while not os.path.exists(ham) and os.path.exists(kilit) and bekle < 2400:
        if bekle == 0:
            print("  onden indirme suruyor, bekleniyor...")
        time.sleep(5); bekle += 5
    if not os.path.exists(ham):
        if a.kuru:
            print("  [kuru] indirme atlandi"); return
        print("  indiriliyor...")
        for deneme in range(3):
            r = kos([YTDLP, "--no-playlist", "-f", "bv*+ba/b",
                     "--retries", "10", "--fragment-retries", "50",
                     "--socket-timeout", "30", "--abort-on-unavailable-fragment",
                     "-o", os.path.join(proje, "ders.%(ext)s"), kayit["url"]])
            if os.path.exists(ham):
                break
            hata = (r.stderr or "")[-300:]
            # Loom hiz sinirina takildiysa beklemek gerek, tekrar tekrar vurmak isi bozar
            bekleme = 120 * (deneme + 1)
            print("  indirme basarisiz (deneme %d/3), %d sn bekleniyor" % (deneme + 1, bekleme))
            if deneme < 2:
                time.sleep(bekleme)
        if not os.path.exists(ham):
            sys.exit("HATA: indirme basarisiz (3 deneme)\n" + hata)
    sure = float(kos([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", ham]).stdout.strip())
    # KAYNAK DOGRULAMASI: yarim inmis ses sessizce bozuk video uretiyor.
    # (22.09.2026: CH01'in sesi 26 dk, videosu 78 dk indi; transkript ve kesim analizi
    #  de yalnizca ilk 26 dakikaya dayandi, uretim 7. parcada patladi.)
    vs = kos([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
              "stream=duration", "-of", "csv=p=0", ham]).stdout.strip()
    as_ = kos([FFPROBE, "-v", "error", "-select_streams", "a:0", "-show_entries",
               "stream=duration", "-of", "csv=p=0", ham]).stdout.strip()
    try:
        vd, ad_ = float(vs), float(as_)
    except ValueError:
        vd = ad_ = 0.0
    if vd > 0 and ad_ > 0 and abs(vd - ad_) / vd > 0.01:
        print("  KAYNAK BOZUK: video %.1f dk, ses %.1f dk -> yeniden indiriliyor"
              % (vd / 60, ad_ / 60))
        os.remove(ham)
        for f in os.listdir(edit):
            if f in ("sessizlik.json", "transkript_tam.json", "kesimler.json"):
                os.remove(os.path.join(edit, f))
        import shutil
        shutil.rmtree(os.path.join(edit, "parca"), ignore_errors=True)
        sys.exit("HATA: kaynak eksik inmis, silindi. Sonraki turda yeniden indirilecek.")
    print("  ham: %.1f dk" % (sure / 60))
    # Kullanıcı indirilen hami HEMEN gorebilsin: sabit baglanti, diskte ekstra yer tutmaz.
    # (22.09.2026 kararı: "neden ch01'i indirilenlere kaydetmedin")
    try:
        hd = os.path.join(INDIR, "Ham")
        os.makedirs(hd, exist_ok=True)
        if bol:
            hadi = "%02d - %s (ham).mp4" % (bol["no"], bol["chapter"].strip())
        else:
            hadi = "00 - %s (%s) (ham).mp4" % (kayit["link_tarih"][:10].replace(".", "-"), vid[:8])
        hedef = os.path.join(hd, re.sub(r"[/:\\]", "-", hadi))
        if not os.path.exists(hedef):
            os.link(ham, hedef)
            print("  Indirilenler/Ham -> %s" % os.path.basename(hedef))
    except OSError as e:
        print("  (ham baglanti kurulamadi: %s)" % e)
    if a.indir:
        print("  INDI: %s" % proje); return

    # 2) sessizlik
    sy = os.path.join(edit, "sessizlik.json")
    if not os.path.exists(sy):
        kos([VENV, os.path.join(BIN, "sessizlik.py"), ham])
    ses = json.load(open(sy))

    # 3) transkript
    ty = os.path.join(edit, "transkript_tam.json")
    if not os.path.exists(ty):
        print("  transkript...")
        kos([VENV, os.path.join(BIN, "asr.py"), ham, "--tam", "--out", ty])

    # 4) kesim adaylari + karar
    if a.model:
        my = os.path.join(edit, "model_kesim.json")
        if not os.path.exists(my):
            sys.exit("HATA: %s yok. Once kurgu_brief.py + camp-video-kurgucu calistirilmali." % my)
        mk = json.load(open(my))

        def _sn(k, *adlar):
            # Ajan semayi bazen "bas"/"bit", bazen "bas_s"/"bit_s" olarak donduruyor.
            for ad in adlar:
                if k.get(ad) is not None:
                    return float(k[ad])
            raise SystemExit("HATA: model kesiminde %s alani yok: %r" % (adlar, k))

        # Ajan ust anahtari ders ders farkli adlandiriyor (kesimler / kesim / ...).
        _liste = None
        for ad in ("kesimler", "kesim", "kesim_listesi", "cuts"):
            if isinstance(mk.get(ad), list):
                _liste = mk[ad]; break
        if _liste is None:
            sys.exit("HATA: model_kesim.json icinde kesim listesi bulunamadi (anahtarlar: %s)"
                     % list(mk.keys()))
        uyg = []
        for k in _liste:
            if k.get("karar") in ("atla", "kesme", "reddedildi"):
                continue
            b, e_ = _sn(k, "bas", "bas_s"), _sn(k, "bit", "bit_s")
            if k.get("supheli"):
                # Yazili dakika EMIRDIR: modelin tereddudu kullanıcının talimatini
                # gecersiz kilmaz. Talimat kapsamayan supheli kesim ise atlanir.
                tal = k.get("talimat") or k.get("talimat_dakika")
                if tal is None:
                    tal = next((sn for sn in talimat_dakikalari(kayit)
                                if b - 90 <= sn <= e_ + 90), None)
                if tal is None:
                    print("  supheli kesim atlandi: %.1f-%.1f (%s)"
                          % (b, e_, str(k.get("gerekce", ""))[:60]))
                    continue
                print("  supheli ama TALIMATLI (%s. dk) -> uygulandi: %.1f-%.1f"
                      % (tal if tal < 200 else int(tal) // 60, b, e_))
            uyg.append({"bas": b, "bit": e_, "tur": k.get("tur", "model"),
                        "gerekce": str(k.get("gerekce", ""))[:200],
                        "kesin": bool(k.get("kesin"))})
        for k in (mk.get("supheli") if isinstance(mk.get("supheli"), list) else []) or []:
            try:
                print("  supheli (uygulanmadi): %.1f-%.1f · %s"
                      % (_sn(k, "bas", "bas_s"), _sn(k, "bit", "bit_s"),
                         str(k.get("gerekce", ""))[:60]))
            except SystemExit:
                pass
        uyg.sort(key=lambda x: x["bas"])
        # ortusme kontrolu
        for i in range(1, len(uyg)):
            if uyg[i]["bas"] < uyg[i - 1]["bit"]:
                sys.exit("HATA: model kesimleri ortusuyor (%.1f < %.1f)"
                         % (uyg[i]["bas"], uyg[i - 1]["bit"]))
        for k in uyg:
            if k["bit"] <= k["bas"]:
                sys.exit("HATA: model kesimi gecersiz (%.1f >= %.1f)" % (k["bas"], k["bit"]))
        # talimat kapsama: yazili dakika EMIRDIR, kapsanmayan varsa uretim durur
        # Bir dakika ya konum olarak kapsanir ya da model o kesimi ACIKCA o dakikaya
        # baglar. Yazili dakika bazen kayittaki gercek yerle ortusmuyor (CH16: mesajda
        # "6. dk" yaziyor ama bastan alma 11. dakikada). Kapinin isi sessiz atlamayi
        # yakalamak; gerekcelendirilmis eslemeyi bozmak degil.
        _isaretli = set()
        for k in _liste:
            t = k.get("talimat") or k.get("talimat_dakika")
            if t is not None:
                _isaretli.add(int(t) if int(t) < 200 else int(t) // 60)
        eksik_tal = [sn // 60 for sn in talimat_dakikalari(kayit)
                     if not any(x["bas"] - 90 <= sn <= x["bit"] + 90 for x in uyg)
                     and (sn // 60) not in _isaretli]
        if eksik_tal:
            sys.exit("HATA: talimat dakikalari kapsanmadi: %s. dk" % eksik_tal)
        oran = 100.0 * sum(x["bit"] - x["bas"] for x in uyg) / max(1.0, sure)
        if oran > 12.0:
            sys.exit("HATA: kesim orani %%%.1f, %%12 ustu" % oran)
        print("  model karari: %d kesim, %%%.1f" % (len(uyg), oran))
    else:
        uyg = None
    ky = os.path.join(edit, "kesimler.json")
    if not os.path.exists(ty):
        sys.exit("HATA: transkript uretilmedi (%s). ASR yarida kesilmis olabilir." % ty)
    if not a.model:
        r = kos([VENV, os.path.join(BIN, "tekrar_bul.py"), ty, "--out", ky, "--sessizlik", sy])
        if not os.path.exists(ky):
            sys.exit("HATA: kesim cozumu uretilmedi\n" + (r.stderr or "")[-300:])
        kes = json.load(open(ky))
        uyg = sorted(kes.get("uygulanan", []), key=lambda x: x["bas"])

        # 4b) WhatsApp talimati varsa: karsilanmayan dakikalarda esigi dusur
        # (22.09.2026 kararı: "nereleri kesmeni istedigim bile yazilmis") Yazili dakika
        # EMIRDIR. Yakinda kucuk bir kesim olmasi "karsilandi" saymaz; o dakikayi kapsayan
        # ya da ona 45 sn'den yakin bir kesim aranir, yoksa en guclu aday zorla uygulanir.
        eksik = []
        for sn in talimat_dakikalari(kayit):
            kapsiyor = any(x["bas"] - 45 <= sn <= x["bit"] + 45 for x in uyg)
            if not kapsiyor:
                # once atlanmis adaylar arasinda o bolgeye denk gelen var mi
                zorla = [a for a in kes.get("aday", [])
                         if a.get("karar") == "atla" and a["bas"] - 90 <= sn <= a["bit"] + 90]
                if zorla:
                    z = max(zorla, key=lambda a: a["bit"] - a["bas"])
                    z["karar"], z["gerekce"] = "uygula", "TALIMAT: %d. dk kesilmeli" % (sn // 60)
                    uyg.append(z)
                    print("  talimat %d. dk -> atlanan aday zorla uygulandi (%.0f sn)"
                          % (sn // 60, z["bit"] - z["bas"]))
                    kapsiyor = True
            if not kapsiyor:
                # TALIMAT VAR AMA ADAY YOK: yeniden cekimin imzasi "soyler - durur - bastan
                # soyler". O dakikadaki EN BUYUK duraklamayi bul, ondan onceki konusma
                # blogunu kes. (22.09.2026, CH15: hoca hiperkalsemiyi farkli kelimelerle
                # bastan anlatmis; kelime benzerligi dusuk oldugu icin dedektor goremedi.)
                civar = [b for b in ses["bosluk"] if abs(b["bas"] - sn) <= 60 and b["sure"] >= 1.0]
                if civar:
                    b = max(civar, key=lambda x: x["sure"])
                    onceki = [x for x in ses["bosluk"] if x["bit"] < b["bas"] - 3 and x["sure"] >= 0.8]
                    blok_bas = onceki[-1]["bit"] if onceki else max(0.0, b["bas"] - 45)
                    if 3.0 <= b["bit"] - blok_bas <= 90.0:
                        uyg.append({"bas": round(blok_bas, 2), "bit": round(b["bit"] - 0.2, 2),
                                    "tur": "talimat_blok",
                                    "gerekce": "TALIMAT %d. dk: duraklamadan onceki blok" % (sn // 60)})
                        print("  talimat %d. dk -> blok kesildi (%.0f sn, duraklama %.1f sn)"
                              % (sn // 60, b["bit"] - blok_bas, b["sure"]))
                        kapsiyor = True
            if not kapsiyor:
                yakin = [b for b in ses["bosluk"]
                         if abs(b["bas"] - sn) <= 90 and b["sure"] >= 2.0]
                if yakin:
                    b = max(yakin, key=lambda b: b["sure"])
                    uyg.append({"bas": round(b["bas"] + 0.35, 2), "bit": round(b["bit"] - 0.35, 2),
                                "tur": "olu_zaman", "gerekce": "talimat %d. dk, %.1f sn sessizlik"
                                % (sn // 60, b["sure"])})
                else:
                    eksik.append(sn // 60)
    # 4c) Sinirlari sessizlige oturt: birlesme yerinde kelime kesilmesin
    ince_kullanilan, dusen_kesim = [], []
    uyg = sinira_otur(uyg, ses["bosluk"], video=ham, kullanilan=ince_kullanilan,
                      dusen=dusen_kesim)
    if a.model:
        # Kapsama denetimi hizalamadan ONCE yapilmisti; hizalama bir kesimi
        # dusurmusse yazili emir karsiliksiz kalir. Tekrar bakilir.
        kalan_tal = [sn // 60 for sn in talimat_dakikalari(kayit)
                     if not any(x["bas"] - 90 <= sn <= x["bit"] + 90 for x in uyg)
                     and (sn // 60) not in _isaretli]
        if kalan_tal:
            sys.exit("HATA: hizalama sonrasi talimat dakikalari kapsanmiyor: %s. dk\n"
                     "  dusen kesimler: %s" % (kalan_tal, dusen_kesim))
    if ince_kullanilan:
        # Denetci ayni kanita baksin: kullanilan ince bosluklar haritaya islenir
        ses["bosluk"] = sorted(ses["bosluk"] + ince_kullanilan, key=lambda b: b["bas"])
        ses["ince_eklendi"] = len(ince_kullanilan)
        json.dump(ses, open(sy, "w"), indent=1)
    hiz = sum(1 for x in uyg if x.get("hizalandi"))
    if hiz:
        print("  %d kesim siniri sessizlige hizalandi" % hiz)
    uyg.sort(key=lambda x: x["bas"])

    # 5) bas/son kirpma
    # Ders hocanin konusmaya basladigi anda baslar, oncesinde bos an birakilmaz.
    # (22.09.2026 kararı: "dersler direkt hocanin konusmaya basladigi yerden baslamali")
    if a.model:
        # Model transkripti gordu: acilista slayt gezinmesi mi yoksa ders mi
        # anlatiliyor kararini o verir. Sezgisel acilis_slayt_degisimi bunu
        # ayirt edemedigi icin CH03'te gercek anlatimi kirpmisti.
        bk = mk.get("bas_kirpma") or {}
        sk = mk.get("son_kirpma") or {}
        bas = round(float(bk.get("baslangic_s", max(0.0, ses["ilk_konusma"] - 0.25))), 2)
        son = round(float(sk.get("bitis_s", min(sure, ses["son_konusma"] + 1.5))), 2)
        bas = max(0.0, min(bas, sure))
        son = max(bas + 1.0, min(son, sure))

        def _sessizlige_otur(t, yon):
            """Bas/son kirpma sinirini de sessizlige oturt.

            Hizalama simdiye kadar yalniz kesim listesine uygulaniyordu; model bas
            kirpma yaptiginda o sinir ham kaliyor ve G7 kapisi kaliyordu.
            (CH31, 23.09.2026: bas kirpma 29.50 sessizlige oturmamisti.)

            Aday sirasi kesimlerdekiyle ayni: kaba-yonlu -> ince-yonlu -> serbest.
            Yon onemli, cunku bas ileri (daha cok atar), son geri kaydirilmali;
            ters yon modelin bilerek attigi bozuk acilisi geri getiriyor.
            (CH47: 6.54 -> 5.31 olunca yanlis baslangic kadraja giriyordu.)
            """
            if t <= 0.05:
                return t
            if any(b["bas"] - 0.15 <= t <= b["bit"] + 0.15 for b in ses["bosluk"]):
                return t

            def _yakin(liste):
                return [b for b in liste
                        if abs(b["bas"] - t) <= 3.0 or abs(b["bit"] - t) <= 3.0]

            def _yonlu(liste):
                return [b for b in liste
                        if (b["bit"] >= t if yon == "bas" else b["bas"] <= t)]

            ince = None
            aday = _yonlu(_yakin(ses["bosluk"]))
            if not aday:
                ince = ince_bosluklar(ham, t, yaricap=3.0)
                aday = _yonlu(_yakin(ince))
            if not aday:
                aday = _yakin(ses["bosluk"])
            if not aday:
                ince = ince if ince is not None else ince_bosluklar(ham, t, yaricap=3.0)
                aday = _yakin(ince)
            if not aday:
                return t
            if ince:
                eklenen = [b for b in aday if b in ince]
                if eklenen:
                    ses["bosluk"] = sorted(ses["bosluk"] + eklenen, key=lambda b: b["bas"])
                    json.dump(ses, open(sy, "w"), indent=1)
            b = min(aday, key=lambda b: min(abs(b["bas"] - t), abs(b["bit"] - t)))
            yeni_t = round(b["bit"] - 0.08 if yon == "bas" else b["bas"] + 0.08, 3)
            if yeni_t < b["bas"] or yeni_t > b["bit"]:
                yeni_t = round((b["bas"] + b["bit"]) / 2.0, 3)
            print("  %s kirpma sessizlige oturtuldu: %.2f -> %.2f" % (yon, t, yeni_t))
            return yeni_t

        bas = _sessizlige_otur(bas, "bas")
        son = _sessizlige_otur(son, "son")
        son = max(bas + 1.0, min(son, sure))
        if bk.get("yapildi"):
            print("  bas kirpma (model): %.2f sn · %s" % (bas, bk.get("gerekce", "")[:70]))
        if sk.get("yapildi"):
            print("  son kirpma (model): %.2f sn · %s" % (son, sk.get("gerekce", "")[:70]))
    else:
        bas = max(0.0, round(ses["ilk_konusma"] - 0.25, 2))
        sl = acilis_slayt_degisimi(ham)
        if sl and sl > bas:
            print("  acilista slayt gezinmesi: ders %.2f sn'den basliyor" % sl)
            bas = round(sl, 2)
        son = round(min(sure, ses["son_konusma"] + 1.5), 2)

    # 6) EDL
    ranges = [{"source": "OPENER", "start": 0.0, "end": 6.006, "beat": "OPENER",
               "reason": "CAMPVERSE acilisi"}]
    imlec = bas
    for k in uyg:
        if k["bas"] <= imlec or k["bas"] >= son:
            continue
        ranges.append({"source": "DERS", "start": round(imlec, 2),
                       "end": round(min(k["bas"], son), 2), "beat": "BODY",
                       "reason": "kesim oncesi"})
        imlec = max(imlec, min(k["bit"], son))
    ranges.append({"source": "DERS", "start": round(imlec, 2), "end": son,
                   "beat": "BODY", "reason": "son parca"})
    ranges = [r for r in ranges if r["end"] - r["start"] > 0.3]
    toplam = sum(r["end"] - r["start"] for r in ranges)
    kesilen = (son - bas) - (toplam - 6.006)
    oran = 100.0 * kesilen / max(1.0, son - bas)
    if a.model:
        print("  kesim: %d adet, %.1f sn (%%%.1f)  ·  karar: MODEL"
              % (len(uyg), kesilen, oran))
        atlanan, eksik = [], []
    else:
        print("  kesim: %d adet, %.1f sn (%%%.1f)  ·  atlanan aday: %d"
              % (len(uyg), kesilen, oran, len(kes.get("aday", [])) - len(kes.get("uygulanan", []))))
        atlanan = [x for x in kes.get("aday", []) if x.get("karar") == "atla"]
    if atlanan or eksik:
        json.dump({"ders": ad, "vid": vid, "atlanan": atlanan, "talimat_eksik": eksik},
                  open(os.path.join(edit, "sorulacak.json"), "w"),
                  ensure_ascii=False, indent=1)
    if eksik:
        print("  UYARI: talimattaki %s. dakikalarda aday bulunamadi" % eksik)
    if oran > 12:
        sys.exit("DUR: kesim orani %%%.1f, cok yuksek. Elle bakilmali." % oran)

    import hashlib, shutil as _sh
    # Slaytta yanlis bir bolum varsa arka plan rengiyle kapatilir. Liste ayri
    # dosyada tutulur ki kesim listesinden bagimsiz duzeltilebilsin.
    kapatma = []
    ky = os.path.join(edit, "kapatma.json")
    if os.path.exists(ky):
        try:
            kapatma = json.load(open(ky)).get("kapatma", [])
        except Exception as e:
            sys.exit("HATA: kapatma.json okunamadi: %s" % e)
        for k in kapatma:
            for alan in ("bas", "bit", "x", "y", "w", "h"):
                if alan not in k:
                    sys.exit("HATA: kapatma kaydinda '%s' yok: %r" % (alan, k))
        if kapatma:
            print("  %d slayt bolgesi kapatilacak" % len(kapatma))
    yeni_imza = hashlib.md5(
        json.dumps([ranges, kapatma], sort_keys=True).encode()).hexdigest()
    imza_yolu = os.path.join(edit, "edl_imza.txt")
    eski_imza = open(imza_yolu).read().strip() if os.path.exists(imza_yolu) else ""
    if eski_imza and eski_imza != yeni_imza:
        _sh.rmtree(os.path.join(edit, "parca"), ignore_errors=True)
        for f in ("final.mp4",):
            try:
                os.remove(os.path.join(edit, f))
            except OSError:
                pass
        print("  EDL degisti -> eski parcalar silindi")
    open(imza_yolu, "w").write(yeni_imza)

    json.dump({"version": 1, "sources": {"OPENER": OPENER, "DERS": ham},
               "kapatma": kapatma,
               "ranges": ranges, "grade": "none", "overlays": [], "subtitles": False,
               "total_duration_s": round(toplam, 3)},
              open(os.path.join(edit, "edl.json"), "w"), ensure_ascii=False, indent=1)
    if a.kuru:
        print("  [kuru] uretim atlandi"); return
    if a.hazirla:
        print("  HAZIR: %s" % proje); return

    # 7) uret
    print("  uretiliyor...")
    r = kos([VENV, os.path.join(BIN, "olustur.py"), os.path.join(edit, "edl.json"),
             "-o", os.path.join(edit, "final.mp4"), "--crf", str(a.crf)])
    fin = os.path.join(edit, "final.mp4")
    kontrol = kos([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                   "-of", "csv=p=0", fin])
    if not os.path.exists(fin) or kontrol.returncode != 0 or not kontrol.stdout.strip():
        if os.path.exists(fin):
            os.remove(fin)
        sys.exit("HATA: uretim basarisiz / cikti bozuk\n" + (r.stderr or "")[-600:])

    # 8) denetle
    d = kos(["python3", os.path.join(BIN, "denetle.py"), proje])
    print("  " + "\n  ".join(d.stdout.strip().splitlines()))
    if d.returncode != 0:
        # Isaret dosyasi: kuyruk ayni kusurlu kurguyu sonsuz kez basmasin. Kesim
        # listesi duzeltilince bu dosyadan yeni olur ve ders kendiliginden yeniden
        # denenir. (23.09.2026)
        open(os.path.join(edit, ".denetim_kaldi"), "w").write(d.stdout)
        sys.exit("DENETIM KALDI, teslim edilmedi")
    try:
        os.remove(os.path.join(edit, ".denetim_kaldi"))
    except OSError:
        pass

    # 9) teslim + temizlik
    if bol:
        dosya = "%02d - %s.mp4" % (bol["no"], bol["chapter"].strip())
    else:
        dosya = "00 - %s (%s).mp4" % (kayit["link_tarih"][:10].replace(".", "-"), vid[:8])
    dosya = re.sub(r'[/:\\]', "-", dosya)
    tes = os.path.join(KOK, "teslim/campverse", dosya)
    subprocess.run(["cp", os.path.join(edit, "final.mp4"), tes])
    indirilenlere_koy(os.path.basename(tes), os.path.join(edit, "final.mp4"), ham)
    takibe_isle(bol, vid, os.path.join(edit, "final.mp4"), edit, ad)
    print("  TESLIM: %s  ·  %.1f dk toplam" % (os.path.basename(tes), (time.time() - t0) / 60))


if __name__ == "__main__":
    main()
