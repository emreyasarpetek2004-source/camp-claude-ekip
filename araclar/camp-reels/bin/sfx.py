#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SFX kütüphanesi: ElevenLabs sound-generation ile bir kez üretilir, sfx/<ad>.wav olarak saklanır.
Anahtar ~/Developer/video-use/.env (ELEVENLABS_API_KEY); ekrana basılmaz.
Her ses -20 LUFS'a normalize edilir, baştaki sessizlik kırpılır (zamanlama hassas olsun diye).
Kullanım: python3 bin/sfx.py [--yeniden ad]
"""
import json, os, subprocess, sys, urllib.request

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG = os.path.expanduser("~/.local/bin/ffmpeg")
SESLER = {
    "whoosh": ("clean fast cinematic whoosh transition, short, no music", 0.8),
    "swoosh_out": ("soft airy swoosh out transition, subtle, short", 0.6),
    "pop": ("soft UI pop sound, bubbly click, short, clean", 0.3),
    "tick": ("crisp single UI tick click, minimal, short", 0.2),
    "ding": ("bright gentle notification ding, single chime, clean", 0.8),
    "riser": ("short tension riser swell, cinematic, clean, no music", 1.2),
    "shutter": ("camera shutter click, single, crisp", 0.4),
    "impact": ("soft deep cinematic impact boom hit, subtle, clean", 0.9),
}


def anahtar():
    for s in open(os.path.expanduser("~/Developer/video-use/.env")):
        if s.startswith("ELEVENLABS_API_KEY="):
            return s.split("=", 1)[1].strip().strip('"')
    sys.exit("ELEVENLABS_API_KEY yok")


def uret(ad, metin, sure, key):
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation",
                                 data=json.dumps({"text": metin, "duration_seconds": max(0.5, sure),
                                                  "prompt_influence": 0.6}).encode(),
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    mp3 = os.path.join(KOK, "sfx", ad + ".mp3")
    open(mp3, "wb").write(urllib.request.urlopen(req, timeout=120).read())
    wav = os.path.join(KOK, "sfx", ad + ".wav")
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-i", mp3, "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,loudnorm=I=-20:TP=-3,"
                    "atrim=0:%.2f,afade=t=out:st=%.2f:d=0.08" % (sure, max(0, sure - 0.08)),
                    "-ar", "48000", "-ac", "2", wav], check=True)
    os.remove(mp3)
    print("ok", ad, wav)


def main():
    key = anahtar()
    yeniden = sys.argv[2:] if len(sys.argv) > 2 and sys.argv[1] == "--yeniden" else []
    for ad, (metin, sure) in SESLER.items():
        if os.path.exists(os.path.join(KOK, "sfx", ad + ".wav")) and ad not in yeniden:
            continue
        uret(ad, metin, sure, key)


if __name__ == "__main__":
    main()
