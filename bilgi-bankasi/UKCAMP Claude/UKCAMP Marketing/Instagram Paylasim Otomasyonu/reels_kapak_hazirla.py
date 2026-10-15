#!/usr/bin/env python3
"""
Tasarlanmis bir KAPAK GORSELINI reels videosunun basina gomer.

NEDEN GEREKLI:
Instagram Reels'te kapak iki yoldan verilebiliyor: (1) videonun icinden bir kare
(`thumb_offset`), (2) harici bir kapak gorseli (`cover_url`). Make'in
`instagram-business:CreateAReelPost` modulu SADECE (1)'i aciyor -- modulde cover_url
alani yok, "Make an API Call" turu bir kacis modulu de yok. Kendi Graph API hattimiz
ise kisitli developer hesabi yuzunden kapali. Dolayisiyla tasarlanmis bir kapagi
kullanmanin tek yolu onu videonun ICINE koymak ve thumb_offset ile o kareyi gostermek.

Bu script kapagi videonun EN BASINA, varsayilan olarak TEK KARE (~1/30 sn) suresince
koyar. Instagram reels'i oynatmadan once zaten kapagi gosterdigi icin akis dogal durur;
izleyici tarafinda fark edilmez. Yayinda `--cover-ms 0` kullanilir.

ONEMLI: Kapak profil grid'inde ORTADAN KIRPILIYOR (1080x1920 kapak, grid'de dikey
kirpilmis halde gorunur). Tasarimda yazi/yuz gibi kritik ogeleri ortada tut.

Kalite: video yeniden kodlanmak zorunda (kapak karesi mevcut akisa yapistirilamaz),
ama CRF 17 ile gozle ayirt edilemez ve COZUNURLUK/FPS aynen korunur. Instagram zaten
her videoyu kendi tarafinda yeniden kodluyor.

Kullanim:
  python3 reels_kapak_hazirla.py --video ~/Downloads/video.mov --kapak ~/Downloads/kapak.jpg
  # -> ~/Downloads/video.kapakli.mp4 uretir, sonraki komutu ekrana yazar

  # Kapak 1 saniye GORUNUR olsun istenirse (intro karti gibi):
  python3 reels_kapak_hazirla.py --video v.mov --kapak k.jpg --sure 1.0
"""

import argparse
import json
import os
import subprocess
import sys


def ffprobe(path):
    """Videonun genislik/yukseklik/fps degerlerini doner."""
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-of", "json", path],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        sys.exit(f"HATA: ffprobe videoyu okuyamadi: {res.stderr.strip()[:300]}")
    st = json.loads(res.stdout)["streams"][0]
    pay, bol = st["r_frame_rate"].split("/")
    return st["width"], st["height"], float(pay) / float(bol)


def has_audio(path):
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=index", "-of", "csv=p=0", path],
        capture_output=True, text=True,
    )
    return bool(res.stdout.strip())


def main():
    ap = argparse.ArgumentParser(
        description="Tasarlanmis kapak gorselini reels videosunun basina gomer")
    ap.add_argument("--video", required=True, help="Kaynak video (mov/mp4)")
    ap.add_argument("--kapak", required=True, help="Tasarlanmis kapak gorseli (jpg/png)")
    ap.add_argument("--out", help="Cikti dosyasi (varsayilan: <video>.kapakli.mp4)")
    ap.add_argument("--sure", type=float, default=None, metavar="SN",
                    help="Kapagin videoda kalma suresi (sn). Varsayilan: tek kare "
                         "(~1/fps) -- izleyici fark etmez. 1.0 verilirse intro karti gibi gorunur.")
    ap.add_argument("--crf", type=int, default=17,
                    help="x264 kalite (dusuk = daha iyi). Varsayilan 17 = gozle ayirt edilemez.")
    args = ap.parse_args()

    for yol, ad in ((args.video, "--video"), (args.kapak, "--kapak")):
        if not os.path.exists(yol):
            sys.exit(f"HATA: {ad} dosyasi yok: {yol}")

    w, h, fps = ffprobe(args.video)
    sure = args.sure if args.sure else 1.0 / fps
    sesli = has_audio(args.video)
    out = args.out or f"{os.path.splitext(args.video)[0]}.kapakli.mp4"

    # Kapak videonun olculerine getiriliyor: once orana sadik kucultme, sonra
    # ortalanmis padding. Boylece farkli en-boy oranindaki kapak da bozulmadan oturur.
    kapak_zinciri = (
        f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},format=yuv420p[c]"
    )
    video_zinciri = f"[1:v]fps={fps},format=yuv420p,setsar=1[v]"
    filtre = f"{kapak_zinciri};{video_zinciri};[c][v]concat=n=2:v=1:a=0[outv]"

    cmd = ["ffmpeg", "-y",
           "-loop", "1", "-t", f"{sure}", "-i", args.kapak,
           "-i", args.video]
    if sesli:
        # Kapak karesi icin sessizlik uretilip videonun sesiyle birlestiriliyor;
        # aksi halde ses video karsisinda bir kare kayardi.
        cmd += ["-f", "lavfi", "-t", f"{sure}",
                "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
        filtre += ";[2:a][1:a]concat=n=2:v=0:a=1[outa]"
    cmd += ["-filter_complex", filtre, "-map", "[outv]"]
    if sesli:
        cmd += ["-map", "[outa]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-crf", str(args.crf), "-preset", "medium",
            "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(fps),
            "-movflags", "+faststart", out]

    print(f"Video   : {w}x{h} @ {fps:g} fps{'' if sesli else '  (ses yok)'}")
    print(f"Kapak   : {args.kapak}")
    print(f"Sure    : {sure:.3f} sn ({'tek kare' if not args.sure else 'gorunur intro'})")
    print("Kodlaniyor...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not os.path.exists(out):
        sys.exit(f"HATA: ffmpeg basarisiz:\n{res.stderr.strip()[-1500:]}")

    mb = os.path.getsize(out) / 1024 / 1024
    print(f"\n✓ Hazir: {out}  ({mb:.1f} MB)")
    print("\nSonraki adim -- kapagi DOGRULA, sonra yayinla:")
    print(f'  python3 make_publish.py --ig-type reel --caption cap.txt \\')
    print(f'      --media "<public video url>" --cover-ms 0 --cover-preview "{out}"')
    print("  (onizleme JPEG'i acilip kapak dogrulandiktan sonra --live --yes eklenir)")


if __name__ == "__main__":
    main()
