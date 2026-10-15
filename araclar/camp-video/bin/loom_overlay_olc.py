#!/usr/bin/env python3
"""Her teslim edilen derste Loom sol-kenar overlay'inin kutusunu ve
slayt iceriginin sol sinirini olcer. Ders basina 8 ornek kare yeter:
Loom penceresi ders boyunca sabittir, degisen sadece hangi overlay acik.
"""
import subprocess, os, json, glob, sys
import numpy as np

BAK = 220
TESLIM = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli")

def sure(y):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",y],capture_output=True,text=True).stdout.strip() or 0)

def kare(yol, t):
    out = subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",yol,"-frames:v","1",
        "-vf","crop=%d:1080:0:0"%BAK,"-f","rawvideo","-pix_fmt","rgb24","-"],
        capture_output=True).stdout
    if len(out) < BAK*1080*3: return None
    return np.frombuffer(out,dtype=np.uint8).reshape(1080,BAK,3).astype(np.int16)

def olc(yol):
    d = sure(yol)
    ts = [d*k/9.0 for k in range(1,9)]
    ov_x = ov_y0 = ov_y1 = None
    icerik_sol = 10**9
    for t in ts:
        a = kare(yol,t)
        if a is None: continue
        r,g,b = a[...,0],a[...,1],a[...,2]
        koyu = ((r<85)&(g<85)&(b<92)&(abs(r-g)<20)&(abs(g-b)<20))
        # overlay kutusu DIKEY OLARAK KESINTISIZDIR; slayt metni satir arali.
        # her sutunda en uzun kesintisiz koyu diziyi olc.
        def en_uzun(sutun):
            en = n = 0
            for v in sutun:
                n = n+1 if v else 0
                if n > en: en = n
            return en
        run = np.array([en_uzun(koyu[:,x]) for x in range(BAK)])
        sut = run
        xs = [x for x in range(BAK) if run[x] >= 120]
        if xs:
            x1 = max(xs)
            sat = koyu[:, :x1+1].sum(axis=1)
            ys = [y for y in range(1080) if sat[y] >= max(8,(x1+1)//2)]
            if ys:
                ov_x = x1 if ov_x is None else max(ov_x,x1)
                ov_y0 = min(ys) if ov_y0 is None else min(ov_y0,min(ys))
                ov_y1 = max(ys) if ov_y1 is None else max(ov_y1,max(ys))
        # slayt marka renkleri: sari madde + yesil baslik
        marka = (((r>200)&(g>150)&(g<215)&(b<120)) |
                 ((r<90)&(g>85)&(g<160)&(b<95)))
        mx = np.nonzero(marka.sum(axis=0) >= 4)[0]
        # overlay satir araliginin DISINDA marka rengi ara
        if ov_y0 is not None:
            marka[max(0,ov_y0-4):min(1080,ov_y1+5), :] = False
        mx = np.nonzero(marka.sum(axis=0) >= 4)[0]
        mx = list(mx)
        if mx: icerik_sol = min(icerik_sol, int(min(mx)))
    return {"overlay_sag": ov_x, "overlay_y": [ov_y0, ov_y1],
            "icerik_sol": None if icerik_sol==10**9 else icerik_sol,
            "sure": round(d,1)}

if __name__ == "__main__":
    hedef = sys.argv[1:] or sorted(glob.glob(TESLIM+"/*.mp4"))
    cikti = {}
    for f in hedef:
        ad = os.path.basename(f)
        if ad.startswith("00 - "): continue
        d = olc(f); cikti[ad] = d
        print("%-42s overlay x=0..%-4s y=%-10s icerik sol=%-5s"
              % (ad[:42], d["overlay_sag"], "%s..%s"%tuple(d["overlay_y"]), d["icerik_sol"]),
              flush=True)
    yol = os.path.expanduser("~/camp-video/takip/loom_overlay.json")
    json.dump(cikti, open(yol,"w"), ensure_ascii=False, indent=1)
    print("->", yol)
