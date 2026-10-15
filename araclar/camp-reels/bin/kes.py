#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v2: her reels için Remotion'ın okuyacağı küçük klipleri hazırlar (OLGU katmanı).

edit/klip_NN/
  slayt.mp4      slayt crop'u 1080x608 (paylasim/slayt düzeninde), sessiz
  konusmaci.mp4  konuşmacı crop'u 1080x608 (paylasim) ya da 1080x1350 (konusmaci), sessiz
  ses.wav        konuşma, iki geçişli loudnorm -14 LUFS, 48 kHz
  klip.json      düzen, parçalar, süre, kelimeler (reels zaman çizelgesinde, düzeltilmiş), cümleler
  slayt_serit.jpg  yönetmen için: her 2 sn bir slayt karesi, zaman damgalı

Kesim sınırları v1 ile aynı: uret.sinirla (kelime + sessizlik).
Kullanım: python3 bin/kes.py <proje> [--no 1]
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uret import (FFMPEG, KOK, calistir, crop, duzen, kelime_listesi, loudnorm_olc, sinirla,  # noqa: E402
                  temizle)

W = 1080
MLX = os.path.expanduser("~/.local/bin/mlx_whisper")
DOLGU_RX = re.compile(r"[\W]*(ı+|e+|hm+|ım+|ıh+|eh+m*|e+hm+|hı+m*|ı+hı*|a+h*|ee+m+|[äa]+h*m+)[\W]*", re.I)
DOLGU_PROMPT = "Eee, ııı, şey... Hmm, ıı, yani eee şöyle. Iıı, ee."
NEFES = 0.45      # uzun sessiz duraklama bu süreye kısalır
UZUN = 0.9        # bundan uzun sessiz duraklama kısaltılır
PAY = 0.08        # kesim kenarında kelimeye bırakılan pay


def dolgu_bul(wav16, bas, son):
    """Pencereyi dolgu-yönlendirmeli whisper ile çözer; "eee/ııı" aralıklarını kaynak zamanında döndürür.
    Normal transkript dolguları yazmıyor; prompt'ta dolgu örneği verilince yazıyor (ölçüldü: 2/2 yakalandı)."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        a = os.path.join(td, "a.wav")
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-ss", "%.3f" % bas, "-t", "%.3f" % (son - bas), "-i", wav16,
                        "-y", a], check=True)
        subprocess.run([MLX, a, "--model", "mlx-community/whisper-large-v3-turbo", "--language", "tr",
                        "--word-timestamps", "True", "--initial-prompt", DOLGU_PROMPT,
                        "--condition-on-previous-text", "False", "-o", td, "-f", "json", "--verbose", "False"],
                       capture_output=True, stdin=subprocess.DEVNULL)
        try:
            d = json.load(open(os.path.join(td, "a.json")))
        except Exception:
            return []
    return [(bas + w["start"], bas + w["end"]) for sg in d.get("segments", []) for w in sg.get("words", [])
            if DOLGU_RX.fullmatch(w["word"].strip())]


_ENERJI = {}


def enerji(wav16):
    """10 ms çerçeve RMS (dBFS) ve gürültü tabanı. Kesim sınırı bu eğrinin vadisine oturur
    (whisper kelime zamanı 50-150 ms kayıyor; kelime yutmanın ikinci sebebi buydu, 8 Eki 2026)."""
    if wav16 not in _ENERJI:
        import numpy as np
        import soundfile as sf
        x, sr = sf.read(wav16, dtype="float32")
        if x.ndim > 1:
            x = x.mean(axis=1)
        n = sr // 100
        k = len(x) // n
        rms = np.sqrt((x[: k * n].reshape(k, n) ** 2).mean(axis=1) + 1e-12)
        db = 20 * np.log10(rms)
        _ENERJI[wav16] = (db, float(np.percentile(db, 10)))
    return _ENERJI[wav16]


def vadi(wav16, t0, t1):
    """[t0, t1] içindeki en sessiz 30 ms'nin ortası ve seviyesi (dB, gürültü tabanına göre)."""
    import numpy as np
    db, taban = enerji(wav16)
    i0, i1 = max(0, int(t0 * 100)), min(len(db) - 3, int(t1 * 100))
    if i1 <= i0:
        return None, 99.0
    pencere = np.convolve(db[i0:i1 + 3], np.ones(3) / 3, mode="valid")[: i1 - i0]
    j = int(np.argmin(pencere))
    return (i0 + j + 1.5) / 100.0, float(pencere[j] - taban)


def sabit_unlu_bul(wav16, a, z):
    """Akustik dolgu dedektörü: "eee/ııı" = sesli + tını sabit + perde dümdüz, en az 0,3 sn.
    Ölçüldü (9 Eki 2026, Dt. İlke): dolguda spektral akı medyanın <%60'ı ve perde sapması <2 Hz;
    normal kelimelerde perde 3-13 Hz oynuyor. Kaynak zamanında [(bas, son)] döndürür."""
    import numpy as np
    import soundfile as sf
    import librosa
    x, sr = sf.read(wav16, dtype="float32", start=int(a * 16000), stop=int(z * 16000))
    if x.ndim > 1:
        x = x.mean(axis=1)
    hop = int(0.01 * sr)
    M = librosa.power_to_db(librosa.feature.melspectrogram(y=x, sr=sr, n_fft=512, hop_length=hop, n_mels=40) + 1e-10)
    e = M.max(axis=0)
    flux = np.r_[0, np.abs(np.diff(M, axis=1)).mean(axis=0)]
    flux = np.convolve(flux, np.ones(7) / 7, mode="same")
    f0, _, _ = librosa.pyin(x, fmin=70, fmax=450, sr=sr, hop_length=hop, frame_length=1024)
    n = min(len(e), len(f0))
    e, flux, f0 = e[:n], flux[:n], f0[:n]
    taban = np.percentile(e, 10)
    sesli = e > taban + 15
    med = np.median(flux[sesli]) if sesli.any() else 1.0
    # 100 ms pencerede perde sapması
    sapma = np.full(n, 99.0)
    for i in range(n):
        w = f0[max(0, i - 5): i + 5]
        w = w[~np.isnan(w)]
        if len(w) >= 6:
            sapma[i] = w.std()
    # eşikler (9 Eki 2026, 3. reels'ta kaçan iki "eee" ölçülerek): akı < %70 medyan, perde sapması < 2,5 Hz
    aday = sesli & (flux < 0.7 * med) & (sapma < 2.5)
    out, i = [], 0
    while i < n:
        if aday[i]:
            j = i
            while j < n and (aday[j] or any(aday[j + 1: j + 4])):  # 3 kareye kadar kesintiyi köprüle
                j += 1
            if j - i >= 25:
                # çekirdeği genişlet: perde çekirdek medyanının ±%6'sında ve tını ünlü olarak sürdükçe (dolgunun tamamı)
                fm = np.nanmedian(f0[i:j])
                def devam(q):
                    return 0 <= q < n and sesli[q] and flux[q] < 0.95 * med and not np.isnan(f0[q]) and abs(f0[q] - fm) / fm < 0.06
                i2, j2 = i, j
                while devam(i2 - 1):
                    i2 -= 1
                while devam(j2):
                    j2 += 1
                out.append((a + i2 / 100.0, a + j2 / 100.0))
            i = j
        i += 1
    return out


def _norm(x):
    return re.sub(r"[^a-zçğıöşü0-9]", "", x.replace("İ", "i").replace("I", "ı").lower())


def altyazi_tamamla(klip_wav, kelimeler, duzeltme):
    """Klip sesini kelime zamanlı yeniden çözer; mevcut altyazıda olmayan 2+ kelimelik kısımları ekler."""
    import difflib
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        a = os.path.join(td, "k.wav")
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-i", klip_wav, "-ac", "1", "-ar", "16000", "-y", a], check=True)
        subprocess.run([MLX, a, "--model", "mlx-community/whisper-large-v3-turbo", "--language", "tr", "--word-timestamps", "True",
                        "-o", td, "-f", "json", "--verbose", "False", "--condition-on-previous-text", "False"],
                       capture_output=True, stdin=subprocess.DEVNULL)
        try:
            d = json.load(open(os.path.join(td, "k.json")))
        except Exception:
            return kelimeler, []
    yeni = [{"w": w["word"].strip(), "b": round(w["start"], 3), "e": round(w["end"], 3)}
            for sg in d.get("segments", []) for w in sg.get("words", []) if w["word"].strip()]
    yeni = [w for w in yeni if not re.search(r"altyaz|abone|izlediğiniz", w["w"], re.I) and not DOLGU_RX.fullmatch(w["w"])]
    A = [_norm(w["w"]) for w in kelimeler]
    B = [_norm(w["w"]) for w in yeni]
    out, eklenen, son = [], [], 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        out += kelimeler[son:i1]
        son = i1
        eksik = (j2 - j1) - (i2 - i1)
        # değiştirme yalnız metinler gerçekten farklıysa: "beni" -> "tabii ki var olan tecrübeni" benzerlik 0,30 (eksik cümle);
        # "Kenntnisprüfung'un" -> "Katniss Proof'un" 0,56-0,65 (whisper'ın bozuk yazımı, bizimki doğru). Eşik 0,45.
        benzer = difflib.SequenceMatcher(None, "".join(A[i1:i2]), "".join(B[j1:j2])).ratio() if op == "replace" else 0.0
        if (op == "insert" and eksik >= 2) or (op == "replace" and eksik >= 2 and benzer < 0.45):
            parca = []
            for w in yeni[j1:j2]:
                m = temizle(w["w"], duzeltme) or w["w"]
                if parca and m[:1] in ("'", "’"):  # "B2 'nin" -> "B2'nin"
                    parca[-1]["w"] += m
                    parca[-1]["e"] = w["e"]
                    continue
                parca.append({"w": m, "b": w["b"], "e": w["e"], "nokta": w["w"].rstrip().endswith((".", "?", "!"))})
            out += parca
            eklenen.append("'%s' -> '%s'" % (" ".join(x["w"] for x in kelimeler[i1:i2]), " ".join(x["w"] for x in parca)))
            son = i2
    out += kelimeler[son:]
    return out, eklenen


def kesik_dogrula(wav16, a, z, akustik=False):
    """Kesilecek ses gerçekten yalnız dolgu mu? Normal whisper + dolgu-yönlendirmeli whisper ile çözülür.
    Ölçüldü (8 Eki 2026): eski kurallar 14 kesimin 7'sinde gerçek kelime yuttu ("2020", "Yeni", "baş"...)."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        w = os.path.join(td, "k.wav")
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-ss", "%.3f" % a, "-t", "%.3f" % (z - a), "-i", wav16, "-y", w],
                       check=True)
        metinler = []
        for prompt in (None, DOLGU_PROMPT):
            cmd = [MLX, w, "--model", "mlx-community/whisper-large-v3-turbo", "--language", "tr", "-o", td, "-f", "json",
                   "--verbose", "False", "--condition-on-previous-text", "False"] + (["--initial-prompt", prompt] if prompt else [])
            subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL)
            try:
                metinler.append(json.load(open(os.path.join(td, "k.json"))).get("text", ""))
            except Exception:
                metinler.append("")
    for m in metinler:
        m = re.sub(r"altyaz[ıi]\s*m\.?\s*k\.?|izlediğiniz için teşekkür\w*|abone ol\w*", " ", m, flags=re.I)
        kelime = [x for x in re.findall(r"[\wçğıöşüÇĞİÖŞÜ']+", m)]
        gercek = [x for x in kelime if not DOLGU_RX.fullmatch(x) and x.lower() not in ("evet",)]
        # akustik aday (düz perde + sabit tını) güçlü kanıt: whisper saf ünlüden tek kısa kelime uyduruyor ("Ama")
        if akustik and len(gercek) <= 1 and all(len(x) < 5 for x in gercek):
            continue
        if gercek:
            return False, m.strip()
    return True, " / ".join(x.strip() for x in metinler)


def sessiz_oran(bosluk, a, z):
    if z <= a:
        return 1.0
    s = sum(max(0.0, min(z, x["bit"]) - max(a, x["bas"])) for x in bosluk if x["bit"] > a and x["bas"] < z)
    return s / (z - a)


def alt_parcalar(bas, son, ws, bosluk, dolgular, sil=(), wav16=None, red=None):
    """Parçayı dolgu, uzun sessiz duraklama ve elle silinen aralıklardan böler. [(bas, son)] + kesilen listesi döndürür.
    Kurallar (8 Eki 2026, kelime yutma düzeltmesi):
      - dolgu yalnız dolgu-whisper'ın işaretlediği yerde kesilir; "sesli boşluk" kuralı YOK (gerçek kelime yutuyordu)
      - sınırlar enerji vadisine oturur; vadi gürültü tabanının 12 dB üstündeyse (temiz sessizlik yok) kesilmez
      - kesilecek ses kesik_dogrula'dan geçmezse kesilmez
      - duraklama yalnız %85+ sessiz aralıkta, sessizliğin içinden kısaltılır
    sil: anlar.json'da reels'a verilen [[bas, son], ...] kaynak zamanı (kullanıcının "şu cümleyi sil" revizesi)."""
    red = red if red is not None else []
    kes = [(a, z, "sil") for a, z in sil if bas < z and a < son]
    # 1) dolgu: akustik sabit-ünlü adayları (+ dolgu-whisper işaretleri). Kesim sesli harfin İÇİNDEN yapılır:
    #    iki uçta 60 ms ünlü bırakılır, 15 ms ses geçişiyle birleşir; sınırda kelime yoktur, kelime yutulmaz.
    adaylar = list(sabit_unlu_bul(wav16, bas, son)) if wav16 else []
    for x0, x1 in dolgular:  # whisper'ın "eee" dediği yerde akustik aday yoksa, onun içinde sabit kısım ara
        if not any(x0 - 0.2 <= c0 <= x1 + 0.2 for c0, _ in adaylar) and wav16 and x1 - x0 >= 0.3:
            adaylar += [c for c in sabit_unlu_bul(wav16, x0, x1)]
    for c0, c1 in sorted(adaylar):
        k0, k1 = c0 + 0.05, c1 - 0.05
        if k1 - k0 < 0.15 or k0 < bas + 0.3 or k1 > son - 0.3:
            continue
        ok, metin = kesik_dogrula(wav16, k0, k1, akustik=True)
        if not ok:
            red.append({"bas": round(k0, 2), "son": round(k1, 2), "neden": "gerçek konuşma: " + metin[:60]})
            continue
        # dolgunun hemen önünde/arkasında uzun sessizlik varsa onu da kısalt (nefes payı kalır)
        for x in bosluk:
            if -0.1 < c0 - x["bit"] < 0.45 and x["sure"] > 0.5:
                k0 = min(k0, x["bas"] + NEFES / 2)
            if -0.1 < x["bas"] - c1 < 0.45 and x["sure"] > 0.5:
                k1 = max(k1, x["bit"] - NEFES / 2)
        kes.append((round(k0, 3), round(k1, 3), "dolgu"))
    # 2) uzun sessiz duraklama: doğrudan sessizlik haritasından (whisper kelimeyi sessizliğin üstüne yayabiliyor:
    #    3. reels'ta "teoride" 2873,8-2877,5 içinde 1,8 sn sessizlik vardı). Sessizliğin içinden kısaltılır, nefes payı kalır.
    for x in bosluk:
        a, z = x["bas"], x["bit"]
        if x["sure"] > UZUN and bas + 0.3 < a and z < son - 0.3 and not any(k[0] < z and a < k[1] for k in kes):
            kes.append((round(a + NEFES / 2, 3), round(z - NEFES / 2, 3), "duraklama"))
    # elle silinen aralığın içine düşen otomatik kesimler atılır, sonra zamana göre sıralanır
    elle = [(a, z) for a, z, tp in kes if tp == "sil"]
    kes = sorted([k for k in kes if k[2] == "sil" or not any(a - 0.05 <= k[0] and k[1] <= z + 0.05 for a, z in elle)])
    out, cur = [], bas
    for x0, x1, _ in kes:
        if x0 < cur:  # önceki kesimle çakışıyor (dolgu + duraklama): birleştir, negatif parça üretme (10 Eki 2026)
            cur = max(cur, x1)
            continue
        if x1 - x0 >= 0.15:
            out.append((cur, x0))
            cur = x1
    out.append((cur, son))
    return out, kes


def ifade_uygula(birlesik, proje, marka):
    """ifade düzeltmesi: ["Berufsel Lappnis", "Berufserlaubnis"] gibi çok kelimelik eşleşme tek kelimeye iner.
    Altyazı tamamlamadan SONRA da çalışır: tamamlama düzeltilmiş kelimeyi whisper'ın haliyle eziyordu (10 Eki 2026)."""
    ifade = list(marka.get("ifade", []))
    iy = os.path.join(proje, "edit", "ifade.json")
    if os.path.exists(iy):
        ifade += json.load(open(iy))
    for bul, yaz in ifade:
        parca = bul.split()
        i = 0
        while i <= len(birlesik) - len(parca):
            if [x["w"] for x in birlesik[i:i + len(parca)]] == parca:
                b0, e0 = birlesik[i]["b"], birlesik[i + len(parca) - 1]["e"]
                yeni = yaz.split()  # çok kelimeli düzeltme kelimelere geri bölünür (aktif kelime hapı tek kelimede kalsın)
                adim = (e0 - b0) / len(yeni)
                birlesik[i:i + len(parca)] = [{"w": y, "b": round(b0 + j * adim, 3), "e": round(b0 + (j + 1) * adim, 3),
                                               "nokta": birlesik[i + len(parca) - 1]["nokta"] and j == len(yeni) - 1}
                                              for j, y in enumerate(yeni)]
            i += 1
    return birlesik


def klip_hazirla(proje, r, kel, yer, marka, bosluk):
    meta = json.load(open(os.path.join(proje, "proje.json")))
    no = r["no"]
    kd = os.path.join(proje, "edit", "klip_%02d" % no)
    os.makedirs(kd, exist_ok=True)
    duzeltme = dict(marka.get("duzeltme", {}))
    dy = os.path.join(proje, "edit", "duzeltme.json")
    if os.path.exists(dy):
        duzeltme.update(json.load(open(dy)))

    parcalar, kelimeler, t, kesilen, red = [], [], 0.0, [], []
    wav16 = os.path.join(proje, "edit", "ses.wav")
    for kp, p in enumerate(r["parcalar"]):
        bas, son, ws = sinirla(p, kel, bosluk)
        dolgular = dolgu_bul(wav16, bas, son) if r.get("dolgu_kes", True) else []
        alt, kes = alt_parcalar(bas, son, ws, bosluk, dolgular, r.get("sil", []), wav16, red)
        kesilen += [{"bas": round(a, 3), "son": round(z, 3), "tip": tp} for a, z, tp in kes]
        for ai, (ab, az) in enumerate(alt):
            # alt sınırlar kelime arasında; ilk ve son alt parçada kelime sınırı sinirla'dan gelir
            parcalar.append({"bas": round(ab, 3), "son": round(az, 3), "cikis_bas": round(t, 3), "Kullanici_parca": kp,
                             "ic": ai > 0})
            for w in ws:
                # kelime, süresinin en çok kaldığı alt parçaya atanır; bir parçada 80 ms+ kalıyorsa düşmez
                # ("söyleyeyim… aaaama": uzatma kesilir, "Ama" altyazıda kalır; 9 Eki 2026)
                ort = {j: max(0.0, min(w["e"], z_) - max(w["b"], a_)) for j, (a_, z_) in enumerate(alt)}
                en_iyi = max(ort, key=ort.get)
                if en_iyi == ai and ort[ai] >= min(0.08, (w["e"] - w["b"]) * 0.5):
                    metin = temizle(w["w"], duzeltme) if not w["w"].startswith("'") else w["w"]
                    kelimeler.append({"w": metin or w["w"], "b": round(t + max(w["b"], ab) - ab, 3),
                                      "e": round(t + min(w["e"], az) - ab, 3), "ham": w["w"],
                                      "nokta": w["w"].rstrip().endswith((".", "?", "!"))})
            t += az - ab
    sure = round(t, 3)
    d = r.get("duzen_zorla") or duzen(yer, parcalar[0]["bas"], parcalar[-1]["son"])
    k = yer["kutu"]

    # ekler ("'nde") önceki kelimeye yapışır: altyazıda tek birim
    birlesik = []
    for w in kelimeler:
        if birlesik and (w["ham"].startswith("'") or w["ham"].startswith("’")):
            birlesik[-1]["w"] += w["ham"]
            birlesik[-1]["e"] = w["e"]
            birlesik[-1]["nokta"] = w["nokta"]
        else:
            birlesik.append(dict(w))
    for w in birlesik:
        w.pop("ham", None)
        w["w"] = re.sub(r"^(\.\.\.|…)+", "", w["w"]) or w["w"]  # whisper kelime başına "..." koyuyor

    birlesik = ifade_uygula(birlesik, proje, marka)

    n = len(parcalar)
    giris = []
    tamamlanacak = True
    for p in parcalar:
        giris += ["-ss", "%.3f" % p["bas"], "-t", "%.3f" % (p["son"] - p["bas"] + 0.2), "-i", meta["video"]]
    # SES ve GÖRÜNTÜ AYRI birleşir (10 Eki 2026): concat v+a her parçada sesi videonun kare-yuvarlanmış süresine
    # uzatıyordu; 25 fps kayıtta 13 kesimde altyazı 0,44 sn geri kaldı (R9). Ses birebir parça süresi; görüntü karesi
    # kümülatif süreye göre dağıtılır (hata difüzyonu), dudak senkronu her yerde yarım kareden küçük kalır.
    vs = [s for s in json.load(open(os.path.join(proje, "edit", "probe.json")))["streams"] if s["codec_type"] == "video"][0]
    fp_a, fp_b = (int(x) for x in vs["r_frame_rate"].split("/"))
    kfps = fp_a / fp_b
    graf, toplam, kare = [], 0.0, 0
    for i, p in enumerate(parcalar):
        d_ = p["son"] - p["bas"]
        toplam += d_
        nk = int(round(toplam * kfps)) - kare
        kare += nk
        graf.append("[%d:v]trim=end_frame=%d,setpts=PTS-STARTPTS[v%d]" % (i, nk, i))
        # her parçaya 15 ms ses geçişi: dolgu kesimlerinde klik olmasın
        graf.append("[%d:a]atrim=duration=%.6f,asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st=%.3f:d=0.015[a%d]"
                    % (i, d_, max(0, d_ - 0.015), i))
    graf.append("".join("[v%d]" % i for i in range(n)) + "concat=n=%d:v=1:a=0[cv]" % n)
    graf.append("".join("[a%d]" % i for i in range(n)) + "concat=n=%d:v=0:a=1[ca]" % n)
    harita = []
    vk = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-an"]
    if d == "paylasim":
        graf.append("[cv]fps=30,setsar=1,split=2[a][b]")
        graf.append("[a]%s,scale=%d:608:flags=lanczos[sl]" % (crop(k["slayt"]), W))
        # Zoom küçük kutusu ~300 px: önce sıkıştırma gürültüsü (hqdn3d), sonra büyütme + kontrast uyarlamalı keskinleştirme
        # (cas) + hafif kontrast/doygunluk. unsharp'a göre blok bozulması belirgin az (8 Eki 2026, gözle karşılaştırıldı).
        # Zoom'un kendi isim etiketi bizim hoca etiketimizin yanından taşıyor ("U..."): proje.json "konusmaci_maske"
        # [x, y, w, h] (kaynak piksel) verilirse kırpmadan önce delogo ile silinir (10 Eki 2026)
        mk = meta.get("konusmaci_maske")
        maske = "delogo=x=%d:y=%d:w=%d:h=%d," % tuple(mk) if mk else ""
        graf.append("[b]%s%s,hqdn3d=2:1:3:3,scale=%d:608:flags=lanczos,cas=0.7,eq=contrast=1.04:saturation=1.08[kn]" % (
            maske, crop(k["konusmaci_kucuk"]), W))
        harita = ["-map", "[sl]"] + vk + [os.path.join(kd, "slayt.mp4"), "-map", "[kn]"] + vk + [os.path.join(kd, "konusmaci.mp4")]
    elif d == "gorsel":
        # yalnız konuşmacı olan kesit, paylasim düzeninde basılır: üst panel slayt yerine görsel akışı (kullanıcı, 9 Eki 2026).
        # konuşmacı tam kareden (küçük kutudan çok daha keskin) 16:9 ortalanmış kırpılır, 1080x608.
        x0, y0, x1, y1 = k["konusmaci_tam"] or ([0, 0] + yer["kaynak"])
        w, h = x1 - x0, y1 - y0
        if w / h > 16 / 9:
            nw = int(h * 16 / 9)
            kt = [x0 + (w - nw) // 2, y0, x0 + (w - nw) // 2 + nw, y1]
        else:
            nh = int(w * 9 / 16)
            kt = [x0, y0 + (h - nh) // 2, x1, y0 + (h - nh) // 2 + nh]
        graf.append("[cv]fps=30,setsar=1,%s,scale=%d:608:flags=lanczos,cas=0.4[kn]" % (crop(kt), W))
        harita = ["-map", "[kn]"] + vk + [os.path.join(kd, "konusmaci.mp4")]
    elif d == "slayt":
        graf.append("[cv]fps=30,setsar=1,%s,scale=%d:608:flags=lanczos[sl]" % (crop(k["slayt"]), W))
        harita = ["-map", "[sl]"] + vk + [os.path.join(kd, "slayt.mp4")]
    else:
        x0, y0, x1, y1 = k["konusmaci_tam"] or ([0, 0] + yer["kaynak"])
        h = y1 - y0
        w = int(h * 4 / 5)
        cx = (x0 + x1) // 2
        graf.append("[cv]fps=30,setsar=1,%s,scale=%d:1350:flags=lanczos[kn]" % (crop([cx - w // 2, y0, cx + w // 2, y1]), W))
        harita = ["-map", "[kn]"] + vk + [os.path.join(kd, "konusmaci.mp4")]
    ham = os.path.join(kd, "ses_ham.wav")
    harita += ["-map", "[ca]", "-c:a", "pcm_s16le", "-ar", "48000", ham]
    calistir([FFMPEG, "-nostdin", "-v", "error", "-y"] + giris + ["-filter_complex", ";".join(graf)] + harita)

    m = loudnorm_olc(ham)
    af = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:"
          "offset=%s:linear=true" % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]))
    calistir([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", ham, "-af", af, "-ar", "48000", "-ac", "2",
              os.path.join(kd, "ses.wav")])
    os.remove(ham)

    if d in ("paylasim", "slayt"):
        subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", os.path.join(kd, "slayt.mp4"), "-vf",
                        "fps=1/2,scale=360:-1,drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='%%{pts\\:hms}':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black,"
                        "tile=4x%d" % max(1, int(sure // 8) + 1), "-frames:v", "1", os.path.join(kd, "slayt_serit.jpg")])

    # altyazı tamamlama: genel transkript bazı cümleleri hiç yazmıyor ("Tabii ki var olan tecrübeniz", "Sonra diyorlar ki tamam").
    # Klibin kendi sesi kısa bağlamda yeniden çözülür; 2+ kelimelik eksik kısımlar kelime zamanlarıyla eklenir (9 Eki 2026).
    if tamamlanacak:
        birlesik, eklenen = altyazi_tamamla(os.path.join(kd, "ses.wav"), birlesik, duzeltme)
        for x in eklenen:
            print("   + altyazıya eklendi: %s" % x)
        birlesik = ifade_uygula(birlesik, proje, marka)

    # kamera geçişi: Zoom aktif konuşmacıyı değiştirince konuşmacı klibinde sert kesme olur (moderatör "evet" der vb.)
    gecis = []
    kp = os.path.join(kd, "konusmaci.mp4")
    if os.path.exists(kp):
        pr = subprocess.run([FFMPEG, "-nostdin", "-i", kp, "-vf", "select='gt(scene,0.35)',showinfo", "-f", "null", "-"],
                            capture_output=True, text=True)
        cikis_sinir = [p["cikis_bas"] for p in parcalar[1:]]
        for m in re.finditer(r"pts_time:([\d.]+)", pr.stderr):
            t = float(m.group(1))
            if not any(abs(t - c) < 0.25 for c in cikis_sinir):  # bizim iç kesimimiz geçiş sayılmaz
                gecis.append(round(t, 2))

    # cümleler (yönetmenin okuması için): kelime indeksleriyle
    cumleler, cur = [], []
    for i, w in enumerate(birlesik):
        cur.append(i)
        if w["nokta"] or i == len(birlesik) - 1:
            cumleler.append({"i0": cur[0], "i1": cur[-1], "b": birlesik[cur[0]]["b"], "e": birlesik[cur[-1]]["e"],
                             "metin": " ".join(birlesik[j]["w"] for j in cur)})
            cur = []
    # önceki klip.json (dolgu kesimi öncesi zaman çizelgesi) yönetmen zamanlarını eşlemek için saklanır
    eski = os.path.join(kd, "klip.json")
    if os.path.exists(eski):
        import shutil
        shutil.copy(eski, os.path.join(kd, "klip_onceki.json"))
    klip = {"no": no, "marka": meta["marka"], "duzen": d, "sure": sure, "parcalar": parcalar,
            "baslik": r.get("baslik"), "soru": r.get("soru"), "kanca": r.get("kanca"),
            "hoca": r.get("hoca") or meta.get("hoca"), "webinar": meta.get("webinar"),
            "kelimeler": birlesik, "cumleler": cumleler, "kamera_gecisi": gecis, "kesilen": kesilen, "kesilmeyen": red}
    json.dump(klip, open(os.path.join(kd, "klip.json"), "w"), ensure_ascii=False, indent=1)
    print("klip %02d %-9s %5.1f sn  %d kelime  %d dolgu, %d duraklama kesildi -> %s%s" % (
          no, d, sure, len(birlesik), sum(x["tip"] == "dolgu" for x in kesilen), sum(x["tip"] == "duraklama" for x in kesilen), kd,
          ("  ⚠ KAMERA GEÇİŞİ: %s sn (başka biri kamerada olabilir, gözle bak)" % gecis) if gecis else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proje")
    ap.add_argument("--no", type=int, action="append", default=[])
    a = ap.parse_args()
    proje = os.path.abspath(a.proje)
    meta = json.load(open(os.path.join(proje, "proje.json")))
    marka = json.load(open(os.path.join(KOK, "brands", meta["marka"] + ".json")))
    kel = kelime_listesi(json.load(open(os.path.join(proje, "edit", "kelimeler.json"))))
    yer = json.load(open(os.path.join(proje, "edit", "yerlesim.json")))
    bosluk = json.load(open(os.path.join(proje, "edit", "sessizlik.json")))["bosluk"]
    for r in json.load(open(os.path.join(proje, "edit", "anlar.json")))["reels"]:
        if a.no and r["no"] not in a.no:
            continue
        klip_hazirla(proje, r, kel, yer, marka, bosluk)


if __name__ == "__main__":
    main()
