#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EDL'den TEK GEÇİŞTE final video üretir.

Neden kendi birleştiricimiz: video-use'un render.py'si `scale=1920:-2` dayatıyor ve araya
normalleştirme adımı koymak gerekiyordu. O da ikinci bir kodlama demekti ve kaynağın
1,10 Mbps'ini 0,55 Mbps'e düşürdü (21.09.2026'da yaşandı, kullanıcı kaliteyi geri istedi).

Burada zincir tek: kaynak -> kırp -> ölçekle -> birleştir -> kodla. Ara dosya yok, ikinci
kodlama yok. Ses için iki geçiş var ama ilk geçiş yalnız ÖLÇÜM yapar, video kodlamaz.

Kanvas 1920x1080. Yan bant YOK: kaydın koyu kenar boşluğu kırpılır, kalan içerik kanvasa
oturur. İçerikten piksel kesilmez (kırpma sınırı ölçümle bulunur).
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yerlesim

FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
FFPROBE = os.path.expanduser("~/.local/bin/ffprobe")


def olc(video):
    o = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0", video],
                       capture_output=True, text=True).stdout.strip().split(",")
    return int(o[0]), int(o[1])


def icerik_kutusu(video, ornek=(30, 300, 600, 900), esik=60, oran=0.02):
    """Koyu zemin dışındaki gerçek içerik sınırları. İçerik kesilmesin diye en geniş kutu."""
    import numpy as np
    from PIL import Image
    w, h = olc(video)
    ust, alt, sol, sag = h, 0, w, 0
    sure = float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", video], capture_output=True,
                                text=True).stdout.strip())
    for t in [x for x in ornek if x < sure] or [sure / 2]:
        p = subprocess.run([FFMPEG, "-nostats", "-v", "error", "-ss", str(t), "-i", video,
                            "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                           capture_output=True)
        im = np.asarray(Image.open(io.BytesIO(p.stdout)).convert("L"))
        satir = (im > esik).mean(axis=1)
        sutun = (im > esik).mean(axis=0)
        if not (satir > oran).any():
            continue
        ust = min(ust, int(np.argmax(satir > oran)))
        alt = max(alt, im.shape[0] - 1 - int(np.argmax(satir[::-1] > oran)))
        sol = min(sol, int(np.argmax(sutun > oran)))
        sag = max(sag, im.shape[1] - 1 - int(np.argmax(sutun[::-1] > oran)))
    return sol, ust, sag, alt


def kirpma(video, hedef_en=16, hedef_boy=9):
    """İçeriği kesmeden, koyu boşluktan kırparak hedef orana en çok yaklaşan pencere."""
    w, h = olc(video)
    if abs(w / float(h) - hedef_en / float(hedef_boy)) < 0.005:
        return None, (w, h)
    sol, ust, sag, alt = icerik_kutusu(video)
    ic_w, ic_h = sag - sol + 1, alt - ust + 1
    gereken_h = int(round(w * hedef_boy / float(hedef_en)))
    if gereken_h >= ic_h:
        # Koyu boşluktan simetriğe yakın kırp, içeriği tam kapsa
        bosluk = gereken_h - ic_h
        y = max(0, min(h - gereken_h, ust - bosluk // 2))
        return "%d:%d:0:%d" % (w, gereken_h, y), (w, gereken_h)
    # İçerik hedef orandan yüksek: yalnız koyu boşluğu at, kalan oran farkı ölçeklemeye kalır
    return "%d:%d:0:%d" % (w, ic_h, ust), (w, ic_h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edl")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--genislik", type=int, default=1920)
    ap.add_argument("--yukseklik", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--crf", type=int, default=14)
    ap.add_argument("--preset", default="faster")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--ses-olcme", action="store_true", help="loudnorm olcumunu atla")
    ap.add_argument("--ders-kaynak", default="DERS",
                    help="ders yerlesimi uygulanacak kaynak adi (kart kirpma + balonu ice tasima)")
    ap.add_argument("--balon-kenar", type=float, default=0.015,
                    help="balonun kenarlardan bosluk orani (varsayilan %1.5)")
    ap.add_argument("--yerlesim-yok", action="store_true",
                    help="ders yerlesimini uygulama, duz kirp/olcek kullan")
    ap.add_argument("--kaydir", type=int, default=0,
                    help="kart kirpmasini bu kadar piksel YUKARI kaydir; balonun tasan "
                         "tepesi kareye girsin (kullanıcı 22.09.2026). Ustte olusan serit "
                         "siyaha boyanir, altta karttan ayni kadar gider.")
    ap.add_argument("--balon-tasi", action="store_true",
                    help="balonu kartin icine tasi + hayalet yamasi uygula "
                         "(VARSAYILAN KAPALI: kullanıcı 22.09.2026'da 'hoca kendi goruntusunu "
                         "nereye koyduysa orada kalsin' dedi)")
    ap.add_argument("--balon-olcek", default="oto",
                    help="balon boyutu: 'oto' (yaziya binmeyen en buyuk) ya da 0.50-1.00")
    ap.add_argument("--keskinlik", default="3:3:0.8:3:3:0.0",
                    help="buyutme sonrasi unsharp ayari, kapatmak icin 'yok'")
    ap.add_argument("--paralel", default="oto",
                    help="ayni anda kac parca kodlanir: 'oto' (bellege gore) ya da sayi")
    ap.add_argument("--parca-sn", type=float, default=420.0,
                    help="bir parca en fazla kac saniye kodlanir (bellek tavani)")
    ap.add_argument("--tek-gecis", action="store_true",
                    help="tum grafigi tek ffmpeg'de kur (bellek yogun, uzun derste SIGKILL riski)")
    a = ap.parse_args()

    edl = json.load(open(a.edl))
    kok = os.path.dirname(os.path.abspath(a.edl))
    kaynak = {k: (v if os.path.isabs(v) else os.path.join(kok, v))
              for k, v in edl["sources"].items()}
    sira = list(kaynak.keys())
    # Balon yerlesim plani (05.10.2026, kullanıcı secimi B): edit/balon_plan.json varsa
    # balon %90 boyda tamamen kartin icine, kayittaki yerine tasinir; hayaletin yalniz
    # acikta kalan pikselleri maskeyle yamalanir.
    plan_yol = os.path.join(kok, "balon_plan.json")
    plan = json.load(open(plan_yol)) if os.path.exists(plan_yol) else None

    # Her kaynak icin kirpma bir kez hesaplanir
    kirp, ders_yer = {}, None
    for k, yol_k in kaynak.items():
        if k == a.ders_kaynak and not a.yerlesim_yok:
            g = ({"kart": tuple(plan["kart"]), "balon": tuple(plan["balon_kaynak"])}
                 if plan else yerlesim.geometri(yol_k))
            if g["kart"] and not a.balon_tasi and not plan:
                # Balon kayittaki yerinde kalir. Kirpma yukari kaydirilir ki balonun
                # kartin ustune tasan tepesi kareye girsin; ustte kalan serit siyahlanir.
                kx, ky, kw, kh = g["kart"]
                yeni_y = max(0, ky - a.kaydir)
                serit = ky - yeni_y
                kirp[k] = "%d:%d:%d:%d" % (kw, kh, kx, yeni_y)
                # Ust serit BOYANMAZ: kaydin kendi zemini oldugu gibi kalir
                # (22.09.2026 kararı: "banta gerek yok direkt kirpmayi 30 piksel kaydir")
                globals()["SIYAH_SERIT"] = 0
                print("%-8s %s -> KART %dx%d @%d,%d · %d px yukari kaydirildi"
                      % (k, "x".join(map(str, olc(yol_k))), kw, kh, kx, yeni_y, serit))
                continue
            if g["kart"] and g["balon"]:
                ders_yer = g
                kx, ky, kw, kh = g["kart"]
                bx, by, br = g["balon"]
                kirp[k] = "%d:%d:%d:%d" % (kw, kh, kx, ky)
                print("%-8s %s -> KART %dx%d @%d,%d (oran %.3f) · BALON r=%.0f, %.0f px kart disinda"
                      % (k, "x".join(map(str, olc(yol_k))), kw, kh, kx, ky,
                         kw / float(kh), br, max(0, ky - (by - br))))
                continue
            print("%-8s ders yerlesimi olculemedi, duz kirpmaya dusuluyor" % k)
        c, _ = kirpma(yol_k)
        kirp[k] = c
        print("%-8s %s -> kirp=%s" % (k, "x".join(map(str, olc(yol_k))), c or "yok"))

    girdi = []
    for k in sira:
        girdi += ["-i", kaynak[k]]

    # Balon maskesi bir kez uretilir
    maske_yolu, balon_cap, balon_kirp, balon_xy, maske_indeks = None, 0, None, None, None
    if ders_yer:
        kx, ky, kw, kh = ders_yer["kart"]
        bx, by, br = ders_yer["balon"]
        olcek = a.genislik / float(kw)
        if plan:
            bo = 1.0
        elif str(a.balon_olcek).lower() in ("oto", "auto"):
            bo = yerlesim.balon_olcek_oner(kaynak[a.ders_kaynak], ders_yer["kart"],
                                           ders_yer["balon"], pay_orani=a.balon_kenar)
            print("         balon olcegi (olculdu): %.2f  -> yaziya binmeyen en buyuk daire" % bo)
        else:
            bo = float(a.balon_olcek)
        # Balon kenarindan 3 px iceriden kirpilir: Loom balonunun kenar pikselleri
        # kayittaki koyu zeminle karisik, daire maskesi onlari alinca tepede koyu bir
        # yay goruluyordu (05.10.2026).
        br_ic = br - 3 if plan else br
        if plan:
            # Balon kayitta kadraj kenarina tasiyorsa (CH02: tepe -5 px) kirpim merkezli
            # kalsin diye yaricap kadraj icinde kalacak kadar daraltilir; kayma olmaz.
            gen0, yuk0 = olc(kaynak[a.ders_kaynak])
            br_ic = min(br_ic, bx, by, gen0 - bx, yuk0 - by)
        b0x, b0y = int(round(bx - br_ic)), int(round(by - br_ic))
        bcap = int(round(2 * br_ic))
        gen, yuk = olc(kaynak[a.ders_kaynak])
        b0x = max(0, min(gen - bcap, b0x)); b0y = max(0, min(yuk - bcap, b0y))
        balon_kirp = "%d:%d:%d:%d" % (bcap, bcap, b0x, b0y)
        balon_cap = max(2, int(round(bcap * olcek * bo)) // 2 * 2)
        pay = int(round(a.balon_kenar * a.genislik))
        balon_xy = (a.genislik - balon_cap - pay, pay)
        # Kart kirpildiginda orijinal balonun kart ICINDE kalan parcasi (hayalet)
        # ust kenara degdigi icin daha buyuk bir daireyle ortulemez; slaytin kendi
        # arka planindan yatay gerilmis bir seritle kapatilir.
        if plan:
            balon_cap = int(plan["cap"]); balon_xy = (int(plan["x"]), int(plan["y"]))
        hx0 = int(round((bx - br - kx) * olcek)) - 6
        hx1 = int(round((bx + br - kx) * olcek)) + 6
        hy1 = int(round((by + br - ky) * olcek)) + 6
        hx0 = max(0, hx0); hx1 = min(a.genislik, hx1); hy1 = min(a.yukseklik, max(2, hy1))
        serit_w = 16
        yama = {"x": hx0, "w": max(2, hx1 - hx0), "h": hy1,
                "sx": max(0, hx0 - serit_w - 2), "sw": serit_w}
        yama["y"] = 0; yama["maske"] = None
        if plan:
            yama = dict(plan["yama"]) if plan.get("yama") else None
            if yama:
                yama["maske"] = os.path.join(kok, "yama_maske.png")
                if yama.get("tip") == "removelogo":
                    yama["ust_maske"] = os.path.join(kok, "yama_ust.png")
                    yama["kucuk"] = os.path.join(kok, "yama_kucuk.png")
                    yama["sag_maske"] = os.path.join(kok, "yama_sag.png") if yama.get("sag") else None
        if yama:
          print("         hayalet yamasi: x=%d w=%d h=%d  (serit x=%d w=%d)"
              % (yama["x"], yama["w"], yama["h"], yama["sx"], yama["sw"]))
        maske_yolu = os.path.join(kok, "balon_maske.png")
        yerlesim.maske_uret(balon_cap, maske_yolu)
        toplam = sum(float(r["end"]) - float(r["start"]) for r in edl["ranges"]) + 1.0
        maske_indeks = len(sira)
        girdi.extend(["-loop", "1", "-framerate", str(a.fps), "-t", "%.3f" % toplam,
                      "-i", maske_yolu])
        yama_indeks = None
        if yama and yama.get("maske"):
            yama_indeks = len(sira) + 1
            girdi.extend(["-loop", "1", "-framerate", str(a.fps), "-t", "%.3f" % toplam,
                          "-i", yama["maske"]])
        print("         balon -> %dx%d, kartin icine (%d,%d), pay %d px"
              % (balon_cap, balon_cap, balon_xy[0], balon_xy[1], pay))

    vf, af, n, balonlu = [], [], 0, []
    for r in edl["ranges"]:
        i = sira.index(r["source"])
        c = kirp[r["source"]]
        yerlesimli = bool(ders_yer) and r["source"] == a.ders_kaynak
        bas = "[%d:v]trim=start=%s:end=%s,setpts=PTS-%s/TB" % (i, r["start"], r["end"], r["start"])
        if yerlesimli:
            vf.append(bas + ",split=2[ham%d][bal%d]" % (n, n))
            kesk = "" if str(a.keskinlik).lower() in ("yok", "none", "") else ",unsharp=%s" % a.keskinlik
            vf.append("[ham%d]crop=%s,scale=%d:%d:flags=lanczos%s,setsar=1,fps=%d:start_time=0,split=2[kart%d][yamakaynak%d]"
                      % (n, c, a.genislik, a.yukseklik, kesk, a.fps, n, n))
            if not yama:
                vf.append("[yamakaynak%d]nullsink;[kart%d]null[taban%d]" % (n, n, n))
            elif yama.get("maske"):
                vf.append("[yamakaynak%d]crop=%d:%d:%d:%d,scale=%d:%d,boxblur=2:1,format=yuva420p[yr%d]"
                          % (n, yama["sw"], yama["h"], yama["sx"], yama["y"], yama["w"], yama["h"], n))
                vf.append("[%d:v]format=gray,scale=%d:%d[pm%d]" % (yama_indeks, yama["w"], yama["h"], n))
                vf.append("[yr%d][pm%d]alphamerge[yama%d]" % (n, n, n))
                vf.append("[kart%d][yama%d]overlay=%d:%d:shortest=1[taban%d]" % (n, n, yama["x"], yama["y"], n))
            else:
                vf.append("[yamakaynak%d]crop=%d:%d:%d:0,scale=%d:%d,boxblur=2:1[yama%d]"
                          % (n, yama["sw"], yama["h"], yama["sx"], yama["w"], yama["h"], n))
                vf.append("[kart%d][yama%d]overlay=%d:0[taban%d]" % (n, n, yama["x"], n))
            vf.append("[bal%d]crop=%s,scale=%d:%d:flags=lanczos,setsar=1,fps=%d:start_time=0[bkirp%d]"
                      % (n, balon_kirp, balon_cap, balon_cap, a.fps, n))
            balonlu.append(n)
        else:
            zincir = bas
            if c:
                zincir += ",crop=%s" % c
            zincir += (",scale=%d:%d:flags=lanczos,setsar=1,fps=%d:start_time=0[v%d]"
                       % (a.genislik, a.yukseklik, a.fps, n))
            vf.append(zincir)
        af.append("[%d:a]atrim=start=%s:end=%s,asetpts=PTS-STARTPTS,"
                  "aresample=48000,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
                  "afade=t=in:st=0:d=0.03,afade=t=out:st=%s:d=0.03[a%d]"
                  % (i, r["start"], r["end"], max(0.0, float(r["end"]) - float(r["start"]) - 0.03), n))
        n += 1

    if balonlu:
        pay_lbl = "".join("[m%d]" % i for i in balonlu)
        vf.append("[%d:v]format=gray,split=%d%s" % (maske_indeks, len(balonlu), pay_lbl)
                  if len(balonlu) > 1 else
                  "[%d:v]format=gray[m%d]" % (maske_indeks, balonlu[0]))
        for i in balonlu:
            vf.append("[bkirp%d][m%d]alphamerge[balA%d]" % (i, i, i))
            vf.append("[taban%d][balA%d]overlay=%d:%d:format=auto:eval=init:shortest=1[v%d]"
                      % (i, i, balon_xy[0], balon_xy[1], i))

    birlesim = ("".join("[v%d][a%d]" % (i, i) for i in range(n))
                + "concat=n=%d:v=1:a=1[vout][acat]" % n)
    temel = ";".join(vf + af + [birlesim])

    # Her parca icin kendi kendine yeten grafik: girdi 0 = kaynak, girdi 1 = maske
    # Uzun parcalar bellegi sisiriyor: 71 dakikalik tek blok 16 GB'lik makinede
    # ffmpeg'i SIGKILL ettirdi (22.09.2026). Her range bellek tavanina gore bolunur.
    bolunmus = []
    for r in edl["ranges"]:
        b, e = float(r["start"]), float(r["end"])
        n_alt = max(1, int((e - b) / a.parca_sn) + (1 if (e - b) % a.parca_sn > 1 else 0))
        adim = (e - b) / n_alt
        for i in range(n_alt):
            alt = dict(r)
            alt["start"] = round(b + i * adim, 3)
            alt["end"] = round(b + (i + 1) * adim, 3) if i < n_alt - 1 else e
            alt["fade_in"] = (i == 0)          # ses solulmasi yalniz gercek sinirda
            alt["fade_out"] = (i == n_alt - 1)
            bolunmus.append(alt)
    # Hoca balonu kayit sirasinda slaytin icine tasidiysa (balon_plan "balonsuz", HAM zaman)
    # o araliklarda yerlesim UYGULANMAZ: kart oldugu gibi, balon zaten icerde. (06.10.2026)
    bsz = (plan or {}).get("balonsuz") or []
    if bsz:
        yeni = []
        for r in bolunmus:
            if r["source"] != a.ders_kaynak:
                yeni.append(r); continue
            b, e = float(r["start"]), float(r["end"])
            kes = sorted({x for iv in bsz for x in iv if b + 0.5 < x < e - 0.5})
            sinir = [b] + kes + [e]
            for k in range(len(sinir) - 1):
                alt = dict(r); alt["start"], alt["end"] = round(sinir[k], 3), round(sinir[k + 1], 3)
                if k > 0: alt["fade_in"] = False
                if k < len(sinir) - 2: alt["fade_out"] = False
                orta = (sinir[k] + sinir[k + 1]) / 2
                alt["balonsuz"] = any(x0 <= orta <= x1 for x0, x1 in bsz)
                yeni.append(alt)
        bolunmus = yeni
        print("  balonsuz aralik (hoca balonu tasimis): %s -> %d parca yerlesimsiz"
              % (bsz, sum(1 for r in bolunmus if r.get("balonsuz"))))
    if len(bolunmus) != len(edl["ranges"]):
        print("  bellek icin %d range -> %d parca (en fazla %.0f sn)"
              % (len(edl["ranges"]), len(bolunmus), a.parca_sn))

    def _kapatma_zinciri(r):
        """EDL'deki kapatma bolgelerini bu parcaya uygun drawbox'a cevirir.

        Slaytta yanlis bir bolum varsa (hocanin 'gorselde bir hata olmus' dedigi
        yer) o dikdortgen slaydin kendi arka plan rengiyle kapatilir; bulanik kutu
        yerine duz renk, cunku amac 'orada oyle bir sey yokmus' gibi durmasi.
        Koordinatlar KAYNAK karede, kirpmadan once uygulanir. (23.09.2026)
        """
        out = []
        for k in edl.get("kapatma", []) or []:
            if k.get("kaynak", a.ders_kaynak) != r["source"]:
                continue
            a0, b0 = float(k["bas"]), float(k["bit"])
            rs, re_ = float(r["start"]), float(r["end"])
            if b0 <= rs or a0 >= re_:
                continue
            i0, i1 = max(a0, rs) - rs, min(b0, re_) - rs
            # delogo cevre piksellerden dolduruyor: duz renk dolgusunun biraktigi
            # hafif ton farki bile olmuyor, gradyanli zeminde de dikis vermiyor.
            # Acik renk istenirse (k["renk"]) drawbox'a duser. (23.09.2026)
            if k.get("renk"):
                out.append("drawbox=x=%d:y=%d:w=%d:h=%d:color=%s:t=fill:enable='between(t\\,%.3f\\,%.3f)'"
                           % (int(k["x"]), int(k["y"]), int(k["w"]), int(k["h"]),
                              k["renk"], i0, i1))
            else:
                out.append("delogo=x=%d:y=%d:w=%d:h=%d:enable='between(t\\,%.3f\\,%.3f)'"
                           % (int(k["x"]), int(k["y"]), int(k["w"]), int(k["h"]), i0, i1))
        return ("," + ",".join(out)) if out else ""

    vf_parca = []
    for r in bolunmus:
        kay = kaynak[r["source"]]
        c = kirp[r["source"]]
        yerlesimli = bool(ders_yer) and r["source"] == a.ders_kaynak and not r.get("balonsuz")
        sure_p = float(r["end"]) - float(r["start"])
        kesk = ("" if str(a.keskinlik).lower() in ("yok", "none", "")
                else ",unsharp=%s" % a.keskinlik)
        g = []
        if yerlesimli:
            # Video zaman damgasi ILK KAREYE degil kesim anina gore korunur: degisken kare
            # hizli Loom kaydinda ilk kare kesimden 0-36 ms sonra geliyor, PTS-STARTPTS onu
            # 0'a cekip goruntuyu sesin onune geciriyordu (CH02 olcumu: +17..+83 ms, 5 Eki 2026).
            g.append("[0:v]null%s,split=2[ham][bal]" % _kapatma_zinciri(r))
            g.append("[ham]crop=%s,scale=%d:%d:flags=lanczos%s,setsar=1,fps=%d:start_time=0,split=2[kart][yk]"
                     % (c, a.genislik, a.yukseklik, kesk, a.fps))
            if not yama:
                g.append("[yk]nullsink"); g.append("[kart]null[taban]")
            elif yama.get("tip") == "removelogo":
                u = int(yama["ust"])
                sg = int(yama.get("sag") or 0)
                g.append("[yk]split=3[yk1][yk2][yk3]" if sg else "[yk]split=2[yk1][yk2]")
                g.append("[yk1]crop=%d:%d:%d:0,scale=%d:%d,format=yuva420p[bd]"
                         % (yama["sw"], u, yama["sx"], yama["w"], u))
                g.append("[3:v]format=gray,scale=%d:%d[tm]" % (yama["w"], u))
                g.append("[bd][tm]alphamerge[bda]")
                g.append("[yk2]crop=%d:%d:%d:0[yb]" % (yama["w"], yama["h"], yama["x"]))
                # removelogo 1/4 olcekte (hiz), sonuc tam boya buyutulup yalniz hayalet
                # maskesinin icine konur; maske disindaki slayt pikselleri hic degismez.
                if sg:
                    # Sag kenar bandi (CH24): bolge kadrajin sag kenarina dayaninca removelogo orada
                    # kaynak bulamaz (pembe). Bolgenin sag alt kosesinden 16x16 ornek dikey gerilir.
                    g.append("[yk3]crop=%d:16:%d:%d,scale=%d:%d,format=yuva420p[sb]"
                             % (sg, yama["x"] + yama["w"] - sg, yama["h"] - 16, sg, yama["h"]))
                    g.append("[4:v]format=gray,scale=%d:%d[smk]" % (sg, yama["h"]))
                    g.append("[sb][smk]alphamerge[sba]")
                    g.append("[yb][sba]overlay=%d:0:shortest=1[ybs]" % (yama["w"] - sg))
                    g.append("[ybs][bda]overlay=0:0:shortest=1,split=2[yb1][yb2]")
                else:
                    g.append("[yb][bda]overlay=0:0:shortest=1,split=2[yb1][yb2]")
                g.append("[yb1]scale=%d:%d:flags=area,removelogo=f=%s,scale=%d:%d:flags=bicubic,"
                         "format=yuva420p[dl]" % (yama["w"] // 4, yama["h"] // 4, yama["kucuk"],
                                                  yama["w"], yama["h"]))
                g.append("[2:v]format=gray,scale=%d:%d[am]" % (yama["w"], yama["h"]))
                g.append("[dl][am]alphamerge[dla]")
                g.append("[yb2][dla]overlay=0:0:shortest=1[yama]")
                g.append("[kart][yama]overlay=%d:0:shortest=1[taban]" % yama["x"])
            elif yama.get("maske"):
                g.append("[yk]crop=%d:%d:%d:%d,scale=%d:%d,boxblur=2:1,format=yuva420p[yr]"
                         % (yama["sw"], yama["h"], yama["sx"], yama["y"], yama["w"], yama["h"]))
                g.append("[2:v]format=gray,scale=%d:%d[pm]" % (yama["w"], yama["h"]))
                g.append("[yr][pm]alphamerge[yama]")
                g.append("[kart][yama]overlay=%d:%d:shortest=1[taban]" % (yama["x"], yama["y"]))
            else:
                g.append("[yk]crop=%d:%d:%d:0,scale=%d:%d,boxblur=2:1[yama]"
                         % (yama["sw"], yama["h"], yama["sx"], yama["w"], yama["h"]))
                g.append("[kart][yama]overlay=%d:0[taban]" % yama["x"])
            g.append("[bal]crop=%s,scale=%d:%d:flags=lanczos,setsar=1,fps=%d:start_time=0[bkirp]"
                     % (balon_kirp, balon_cap, balon_cap, a.fps))
            g.append("[1:v]format=gray[msk]")
            g.append("[bkirp][msk]alphamerge[balA]")
            g.append("[taban][balA]overlay=%d:%d:format=auto:eval=init:shortest=1[vout]"
                     % (balon_xy[0], balon_xy[1]))
            girdi_p = ["-ss", "%.3f" % float(r["start"]), "-t", "%.3f" % sure_p, "-i", kay,
                       "-loop", "1", "-framerate", str(a.fps),
                       "-t", "%.3f" % (sure_p + 1), "-i", maske_yolu]
            if yama and yama.get("tip") == "removelogo":
                girdi_p += ["-loop", "1", "-framerate", str(a.fps),
                            "-t", "%.3f" % (sure_p + 1), "-i", yama["maske"],
                            "-loop", "1", "-framerate", str(a.fps),
                            "-t", "%.3f" % (sure_p + 1), "-i", yama["ust_maske"]]
                if yama.get("sag_maske"):
                    girdi_p += ["-loop", "1", "-framerate", str(a.fps),
                                "-t", "%.3f" % (sure_p + 1), "-i", yama["sag_maske"]]
            elif yama and yama.get("maske"):
                girdi_p += ["-loop", "1", "-framerate", str(a.fps),
                            "-t", "%.3f" % (sure_p + 1), "-i", yama["maske"]]
        else:
            z = "[0:v]null" + _kapatma_zinciri(r)
            if c:
                z += ",crop=%s" % c
            kesk2 = ("" if str(a.keskinlik).lower() in ("yok", "none", "")
                     or r["source"] != a.ders_kaynak else ",unsharp=%s" % a.keskinlik)
            z += ",scale=%d:%d:flags=lanczos%s,setsar=1" % (a.genislik, a.yukseklik, kesk2)
            sh = globals().get("SIYAH_SERIT", 0)
            if sh and r["source"] == a.ders_kaynak:
                z += ",drawbox=x=0:y=0:w=%d:h=%d:color=black@1:t=fill" % (a.genislik, sh)
            z += ",fps=%d:start_time=0[vout]" % a.fps
            g.append(z)
            girdi_p = ["-ss", "%.3f" % float(r["start"]), "-t", "%.3f" % sure_p, "-i", kay]
        ses = ("[0:a]asetpts=PTS-STARTPTS,aresample=48000,"
               "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo")
        if r.get("fade_in", True):
            ses += ",afade=t=in:st=0:d=0.03"
        if r.get("fade_out", True):
            ses += ",afade=t=out:st=%s:d=0.03" % max(0.0, sure_p - 0.03)
        g.append(ses + "[aout]")
        vf_parca.append({"girdi": girdi_p, "graf": ";".join(g), "sure": sure_p})

    if not a.tek_gecis:
        # PARCALI URETIM (varsayilan)
        # 16 GB RAM'de 78 dakikalik dersi tek grafikte kurmak ffmpeg'i SIGKILL ettirdi
        # (22.09.2026). Parcalar tek tek kodlanip `-c copy` ile birlestirilir: her kare
        # yine BIR kez kodlanir, kalite ayni, bellek parca basina duser, uretim resumable.
        # Denetci hangi kapilarin gecerli oldugunu bilsin diye yerlesim modu yazilir
        try:
            json.dump({"balon_tasindi": bool(ders_yer and not a.yerlesim_yok and (a.balon_tasi or plan)),
                       "balon_plan": plan},
                      open(os.path.join(os.path.dirname(os.path.abspath(a.out)),
                                        "yerlesim.json"), "w"))
        except OSError:
            pass
        gecici = os.path.join(os.path.dirname(os.path.abspath(a.out)), "parca")
        os.makedirs(gecici, exist_ok=True)

        def bos_bellek_gb():
            try:
                o = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
                bos = int(re.search(r"Pages free:\s+(\d+)", o).group(1))
                spek = int(re.search(r"Pages speculative:\s+(\d+)", o).group(1))
                return (bos + spek) * 16384 / 1e9
            except Exception:
                return 0.0

        if str(a.paralel).lower() in ("oto", "auto"):
            bb = bos_bellek_gb()
            paralel = 2 if bb >= 1.5 else 1
            print("  bos bellek %.1f GB -> %d parca paralel" % (bb, paralel))
        else:
            paralel = max(1, int(a.paralel))
        # Paralelde is parcacigi sayisi dusurulur, yoksa cekirdekler birbirini yer
        ip = max(2, 8 // max(1, paralel))

        parcalar = [os.path.join(gecici, "seg_%03d.mp4" % i) for i in range(len(vf_parca))]

        import hashlib

        def anahtar(i):
            # Parca yalniz AYNI komutla ve kodlama TAMAMLANARAK uretildiyse yeniden kullanilir.
            # 6 Eki 2026: eski grafikle (serit yama, PTS-STARTPTS) uretilmis parcalar yeni
            # basimda kullanildi (CH04 hayalet), yarida oldurulen parca tam sayildi (CH03 -1150 sn).
            z = vf_parca[i]
            return hashlib.sha1(json.dumps([z["girdi"], z["graf"], a.crf, a.preset]).encode()).hexdigest()

        def gecerli(p, i=None):
            if not (os.path.exists(p) and os.path.getsize(p) > 1000):
                return False
            if i is not None:
                try:
                    if open(p + ".anahtar").read().strip() != anahtar(i):
                        return False
                except OSError:
                    return False
            k = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", p], capture_output=True, text=True)
            return k.returncode == 0 and bool(k.stdout.strip())

        def kodla(i):
            p = parcalar[i]
            if gecerli(p, i):
                return (i, 0, "zaten var")
            try:
                os.remove(p + ".anahtar")
            except OSError:
                pass
            z = vf_parca[i]
            cmd = [FFMPEG, "-nostats", "-v", "error"] + z["girdi"] + \
                  ["-filter_complex", z["graf"], "-map", "[vout]", "-map", "[aout]",
                   "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
                   "-pix_fmt", "yuv420p", "-x264-params", "keyint=48:min-keyint=24",
                   "-threads", str(ip), "-filter_complex_threads", "2",
                   "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-y", p]
            r = subprocess.run(cmd, capture_output=True)
            if r.returncode == 0 and gecerli(p):
                open(p + ".anahtar", "w").write(anahtar(i))
            return (i, r.returncode, "%.0f sn" % z["sure"])

        print("  %d parca kodlanacak (%d paralel, parca basina %d is parcacigi)"
              % (len(vf_parca), paralel, ip))
        if paralel == 1:
            sonuclar = [kodla(i) for i in range(len(vf_parca))]
        else:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=paralel) as ex:
                sonuclar = list(ex.map(kodla, range(len(vf_parca))))
        for i, rc, bilgi in sonuclar:
            if rc != 0 or not gecerli(parcalar[i]):
                sys.exit("HATA: parca %d kodlanamadi (cikis %s). Bellek yetmiyorsa "
                         "--paralel 1 ya da --parca-sn 240 dene." % (i + 1, rc))
        print("  %d parca tamam" % len(parcalar))

        liste = os.path.join(gecici, "liste.txt")
        with open(liste, "w") as f:
            for p in parcalar:
                f.write("file '%s'\n" % p.replace("'", "'\\''"))
        ham_birlesik = os.path.join(gecici, "birlesik.mp4")
        subprocess.run([FFMPEG, "-nostats", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", liste, "-c", "copy", "-y", ham_birlesik], check=True)

        # Ses seviyesi: VIDEO KOPYALANIR, yalniz ses yeniden kodlanir
        ses_f = "loudnorm=I=%s:TP=-1.5:LRA=11" % a.lufs
        if not a.ses_olcme:
            p = subprocess.run([FFMPEG, "-nostats", "-hide_banner", "-vn", "-i", ham_birlesik,
                                "-af", ses_f + ":print_format=json", "-f", "null", "-"],
                               capture_output=True, text=True)
            import re as _re
            m = {}
            for alan in ("input_i", "input_tp", "input_lra", "input_thresh"):
                g = _re.search(r'"%s"\s*:\s*"(-?[\d.inf]+)"' % alan, p.stderr or "")
                if g:
                    m[alan] = g.group(1)
            if len(m) == 4:
                ses_f += (":measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s"
                          ":linear=true" % (m["input_i"], m["input_tp"], m["input_lra"],
                                            m["input_thresh"]))
                print("  ses olculdu: I=%s TP=%s" % (m["input_i"], m["input_tp"]))
        subprocess.run([FFMPEG, "-nostats", "-v", "error", "-i", ham_birlesik,
                        "-c:v", "copy", "-af", ses_f, "-c:a", "aac", "-b:a", "256k",
                        "-ar", "48000", "-movflags", "+faststart", "-y", a.out], check=True)
        for p in parcalar + [ham_birlesik, liste]:
            try:
                os.remove(p)
            except OSError:
                pass
        try:
            os.rmdir(gecici)
        except OSError:
            pass
        o = subprocess.run([FFPROBE, "-v", "error", "-show_entries",
                            "format=duration,size,bit_rate:stream=width,height,r_frame_rate",
                            "-of", "default=noprint_wrappers=1", a.out],
                           capture_output=True, text=True).stdout
        print(o.strip()); print("->", a.out)
        return

    # 1) Ses olcumu (VIDEO KODLANMAZ)
    ses_filtre = ""
    if not a.ses_olcme:
        print("ses olcumu...")
        ses_birlesim = ("".join("[a%d]" % i for i in range(n))
                        + "concat=n=%d:v=0:a=1[acat]" % n)
        olc_graf = ";".join(af + [ses_birlesim]) + (
            ";[acat]loudnorm=I=%s:TP=-1.5:LRA=11:print_format=json[aout]" % a.lufs)
        p = subprocess.run([FFMPEG, "-nostats", "-hide_banner"] + girdi +
                           ["-filter_complex", olc_graf, "-map", "[aout]",
                            "-f", "null", "-"], capture_output=True, text=True)
        import re as _re
        m = {}
        for alan in ("input_i", "input_tp", "input_lra", "input_thresh"):
            g = _re.search(r'"%s"\s*:\s*"(-?[\d.inf]+)"' % alan, p.stderr or "")
            if g:
                m[alan] = g.group(1)
        if len(m) < 4:
            m = {}
        if m.get("input_i"):
            ses_filtre = ("loudnorm=I=%s:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:"
                          "measured_LRA=%s:measured_thresh=%s:linear=true"
                          % (a.lufs, m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"]))
            print("  olculen: I=%s TP=%s LRA=%s" % (m["input_i"], m["input_tp"], m["input_lra"]))
        else:
            sys.stderr.write("UYARI: loudnorm olcumu okunamadi, tek gecis uygulanacak\n")
            ses_filtre = "loudnorm=I=%s:TP=-1.5:LRA=11" % a.lufs

    # 2) Tek gecis kodlama
    son_graf = temel + ";[acat]%s[aout]" % (ses_filtre or "anull")
    cmd = [FFMPEG, "-nostats", "-v", "error", "-stats_period", "30"] + girdi + \
          ["-filter_complex", son_graf, "-map", "[vout]", "-map", "[aout]"]
    cmd += ["-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
            "-pix_fmt", "yuv420p", "-x264-params", "keyint=48:min-keyint=24",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
            "-movflags", "+faststart", "-y", a.out]
    print("kodlama (tek gecis, crf=%d preset=%s)..." % (a.crf, a.preset))
    subprocess.run(cmd, check=True)

    o = subprocess.run([FFPROBE, "-v", "error", "-show_entries",
                        "format=duration,size,bit_rate:stream=width,height,r_frame_rate",
                        "-of", "default=noprint_wrappers=1", a.out],
                       capture_output=True, text=True).stdout
    print(o.strip())
    print("->", a.out)


if __name__ == "__main__":
    main()
