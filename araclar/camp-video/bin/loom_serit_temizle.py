#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teslim edilen derslerin SOL KENARINDAKI Loom katmanini kapatir.

Loom kaydin icine kendi arayuzunu gomuyor: cizim arac cubugu (renk paleti +
kalem + "Done") ve kayit kontrol paneli (durdur + sayac). Ikisi birbirinin
yerini aliyor, yani kenar hic bos kalmiyor.

Yontem: x=0..84 seridini slayt kenar boslugunun rengiyle doldurmak. Slayt
icerigi x=80'den basliyor ve o 4 piksel ham kayitta zaten katmanin altinda,
yani kayip yok. Koyu kapak/kapanis slaytlarinda beyaz serit kendisi goze
batacagi icin oralarda DOKUNULMAZ (--koyu-atla, varsayilan).

Kesimler degismez: yalnizca goruntu yeniden kodlanir, ses kopyalanir.
(23.09.2026 - kullanicinin karari bekleniyor, bkz. takip/KULLANICIYA-SORULACAK.md)
"""
import argparse, json, os, subprocess, sys, glob
import numpy as np

TESLIM = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli")
GENISLIK = 84
ACIK_ESIK = 170.0        # serit ortalamasi bunun ustundeyse slayt acik
OPENER    = 7.0          # CAMPVERSE acilis karti: Loom katmani yok, DOKUNULMAZ

def sure(y):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","csv=p=0",y],capture_output=True,text=True).stdout.strip() or 0)

def acik_araliklar(yol, fps=2.0):
    """Sol seridin acik (beyaz kenar boslugu) oldugu zaman araliklari."""
    p = subprocess.Popen(["ffmpeg","-v","error","-i",yol,
        "-vf","crop=%d:1080:0:0,fps=%g,scale=8:32"%(GENISLIK,fps),
        "-f","rawvideo","-pix_fmt","rgb24","-"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n=8*32*3; acik=[]
    while True:
        ham=p.stdout.read(n)
        if len(ham)<n: break
        a=np.frombuffer(ham,dtype=np.uint8)
        acik.append(float(a.mean())>ACIK_ESIK)
    p.stdout.close(); p.wait()
    ar=[]; bas=None
    for k,v in enumerate(acik):
        t=k/fps
        if v and bas is None: bas=t
        elif not v and bas is not None:
            ar.append([bas,t]); bas=None
    if bas is not None: ar.append([bas,len(acik)/fps])
    # opener kendi videosu, uzerinde Loom katmani yok: serit oraya uygulanmaz
    ar=[[max(a,OPENER),b] for a,b in ar if b>OPENER]
    # 1 sn'den kisa kesintileri yut, 2 sn'den kisa araliklari at
    bir=[]
    for a in ar:
        if bir and a[0]-bir[-1][1]<=1.0: bir[-1][1]=a[1]
        else: bir.append(a)
    return [a for a in bir if a[1]-a[0]>=2.0]

def filtre(yol, koyu_atla=True):
    kutu="x=0:y=0:w=%d:h=1080:color=0xFDFDFD:t=fill"%GENISLIK
    if not koyu_atla:
        return "drawbox=%s:enable='gte(t\\,%.2f)'"%(kutu,OPENER)
    ar=acik_araliklar(yol)
    if not ar: return None
    d=sure(yol)
    # tum ders acik ise kosul gereksiz
    if len(ar)==1 and ar[0][0]<=OPENER+0.5 and ar[0][1]>d-1.0:
        return "drawbox="+kutu
    kosul="+".join("between(t\\,%.2f\\,%.2f)"%(a,b) for a,b in ar)
    return "drawbox=%s:enable='%s'"%(kutu,kosul)

def temizle(yol, crf=14, preset="faster", koyu_atla=True):
    ad=os.path.basename(yol)
    f=filtre(yol,koyu_atla)
    if f is None:
        print("%-44s ATLANDI (acik aralik yok)"%ad[:44]); return False
    gec=yol+".tmp.mp4"
    r=subprocess.run(["ffmpeg","-v","error","-y","-i",yol,"-vf",f,
        "-c:v","libx264","-preset",preset,"-crf",str(crf),"-pix_fmt","yuv420p",
        "-c:a","copy","-movflags","+faststart",gec],capture_output=True,text=True)
    if r.returncode!=0 or not os.path.exists(gec):
        print("%-44s HATA: %s"%(ad[:44], r.stderr.strip()[:120])); return False
    y=sure(yol); g=sure(gec)
    if abs(y-g)>0.5:
        print("%-44s HATA: sure kaydi %.2f -> %.2f"%(ad[:44],y,g)); os.remove(gec); return False
    os.replace(gec,yol)
    print("%-44s TEMIZ (%.1f dk)"%(ad[:44],g/60))
    return True

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("dersler",nargs="*",help="teslim dosya adi; bos ise hepsi")
    ap.add_argument("--crf",type=int,default=14)
    ap.add_argument("--preset",default="faster")
    ap.add_argument("--koyu-kapat",action="store_true",help="koyu kapaklarda da kapat")
    ap.add_argument("--kuru",action="store_true",help="yalniz filtreyi yazdir")
    a=ap.parse_args()
    hedef=[os.path.join(TESLIM,d) if not os.path.isabs(d) else d for d in a.dersler] \
          or sorted(glob.glob(TESLIM+"/*.mp4"))
    hedef=[h for h in hedef if not os.path.basename(h).startswith("00 - ")]
    n=0
    for h in hedef:
        if a.kuru:
            print("%-44s %s"%(os.path.basename(h)[:44],(filtre(h,not a.koyu_kapat) or "-")[:150]))
        else:
            n+=temizle(h,a.crf,a.preset,not a.koyu_kapat)
    if not a.kuru: print("\ntemizlenen: %d/%d"%(n,len(hedef)))
