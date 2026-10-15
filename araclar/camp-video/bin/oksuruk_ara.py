#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ham kayitta OKSURUK / bogaz temizleme arar.

Yontem: ASR'nin metin uretmedigi boslukta, ani yukselen genis bantli
0.15-0.9 sn'lik bir ses patlamasi. Konusma icindeki unsuz patlamalari
(p,t,k,s) elenir cunku onlar bosluk icinde degildir.
(23.09.2026 kararı: "ch32 de oksuruyor mesela o kismi kirpmamisiz")
"""
import sys, json, os, subprocess
import numpy as np

def bul(tarama_yolu):
    """Girdi: takip/teslim_tarama/<ders>.json — teslim edilen videonun
    ince ASR segmentleri. Ses de teslim edilen videodan okunur."""
    d = json.load(open(tarama_yolu))
    yol = os.path.expanduser("~/Downloads/CAMPVERSE Dersler/Editli/" + d["ders"])
    konus = sorted((s["bas"], s["bit"]) for s in d.get("segment", []))

    w = subprocess.run(["ffmpeg","-v","error","-i",yol,"-ac","1","-ar","16000",
                        "-f","s16le","-"], capture_output=True).stdout
    a = np.frombuffer(w, dtype=np.int16).astype(np.float32)/32768
    P=320; N=len(a)//P
    f=a[:N*P].reshape(N,P)
    db=20*np.log10(np.sqrt((f**2).mean(axis=1))+1e-9)
    W=np.hanning(P); S=np.abs(np.fft.rfft(f*W,axis=1))+1e-9
    duz=np.exp(np.log(S).mean(axis=1))/S.mean(axis=1)
    taban=np.percentile(db,20)

    # ASR bosluklari (>=0.7 sn)
    bosluk=[]
    for i in range(len(konus)-1):
        g0,g1=konus[i][1],konus[i+1][0]
        if g1-g0>=0.7: bosluk.append((g0,g1))
    if konus and konus[0][0]>=0.7: bosluk.insert(0,(0.0,konus[0][0]))

    bulgu=[]
    for g0,g1 in bosluk:
        i0,i1=int(g0/0.02),min(N,int(g1/0.02))
        if i1-i0<8: continue
        yuk=db[i0:i1]>taban+13
        k=0
        while k<len(yuk):
            if yuk[k]:
                j=k
                while j<len(yuk) and yuk[j]: j+=1
                sure=(j-k)*0.02
                if 0.14<=sure<=0.90:
                    seg=slice(i0+k,i0+j)
                    tepe=float(db[seg].max()); dz=float(duz[seg].mean())
                    # ani yukselme: hemen oncesi en az 14 dB sessiz
                    onc=db[max(0,i0+k-8):i0+k]
                    if len(onc) and tepe-float(onc.mean())>=14 and dz>=0.10:
                        bulgu.append({"bas":round((i0+k)*0.02,2),"bit":round((i0+j)*0.02,2),
                                      "tepe_db":round(tepe,1),"duzluk":round(dz,2),
                                      "bosluk":[round(g0,2),round(g1,2)]})
                k=j
            else: k+=1
    return bulgu


if __name__=="__main__":
    import glob
    D=os.path.expanduser("~/camp-video/takip/teslim_tarama")
    hedef=sys.argv[1:] or sorted(glob.glob(D+"/*.json"))
    tum={}
    for f in hedef:
        if not f.endswith(".json"): f=os.path.join(D,f+".json")
        try: b=bul(f)
        except Exception as ex:
            print(os.path.basename(f),"HATA",ex); continue
        ad=os.path.basename(f)[:-5]
        tum[ad]=b
        if b:
            print("%-40s %d aday"%(ad[:40],len(b)))
            for x in b: print("     %8.2f-%8.2f (%.2fs) tepe %5.1f duzluk %.2f  bosluk %s"
                              %(x["bas"],x["bit"],x["bit"]-x["bas"],x["tepe_db"],x["duzluk"],x["bosluk"]))
    json.dump(tum,open(os.path.expanduser("~/camp-video/takip/oksuruk.json"),"w"),
              ensure_ascii=False,indent=1)
    print("\ntoplam aday:",sum(len(v) for v in tum.values()),"· ders:",sum(1 for v in tum.values() if v))
