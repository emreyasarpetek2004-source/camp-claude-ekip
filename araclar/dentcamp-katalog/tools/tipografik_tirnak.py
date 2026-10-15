#!/usr/bin/env python3
"""content/*.py içindeki düz tırnakları tipografik tırnağa çevirir.

Kataloglarda 288 düz kesme/tırnak vardı, tipografik olan yoktu; aynı ekibin
vaka çalışması belgesi ise tamamen tipografik. Fark baskıda "Word'den kopyalanmış"
izlenimi veriyordu.

Dönüşüm YALNIZCA string literal'lerin İÇİNDE yapılır — Python'un kendi tırnakları
tokenize ile ayrıştırılıp korunur, yoksa dosya bozulur.

    '  ->  ’        (Türkçe kesme: Avustralya'da -> Avustralya’da)
    \\" ... \\"  ->  “ ... ”   (çift tırnak çiftleri)

    python3 tools/tipografik_tirnak.py            # kuru çalışma, sayı verir
    python3 tools/tipografik_tirnak.py --uygula   # dosyaları yazar
"""
import io
import pathlib
import sys
import tokenize

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted((ROOT / "content").glob("*.py"))


def convert(body, quote_char):
    """String literal gövdesini dönüştürür. quote_char literal'in sınırlayıcısı."""
    out = []
    open_dq = True          # sıradaki çift tırnak açan mı kapayan mı
    i = 0
    n = len(body)
    while i < n:
        c = body[i]
        if c == "\\" and i + 1 < n:
            nxt = body[i + 1]
            if nxt == '"':
                out.append("“" if open_dq else "”")
                open_dq = not open_dq
                i += 2
                continue
            if nxt == "'":
                out.append("’")
                i += 2
                continue
            out.append(c + nxt)
            i += 2
            continue
        if c == '"' and quote_char != '"':
            out.append("“" if open_dq else "”")
            open_dq = not open_dq
            i += 1
            continue
        if c == "'" and quote_char != "'":
            out.append("’")
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def process(path, apply):
    src = path.read_text(encoding="utf-8")
    lines = src.splitlines(keepends=True)
    edits = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type != tokenize.STRING:
            continue
        (r0, c0), (r1, c1) = tok.start, tok.end
        if r0 != r1:
            continue                       # çok satırlı docstring'lere dokunma
        lit = tok.string
        # önek (f, r, b …) ve sınırlayıcıyı ayır
        k = 0
        while lit[k] not in "\"'":
            k += 1
        q = lit[k]
        qlen = 3 if lit[k:k + 3] in ('"""', "'''") else 1
        if qlen == 3:
            continue
        head, body, tail = lit[:k + 1], lit[k + 1:-1], lit[-1]
        new_body = convert(body, q)
        if new_body != body:
            edits.append((r0 - 1, c0, c1, head + new_body + tail))

    if not edits:
        return 0
    for r, c0, c1, new in sorted(edits, key=lambda e: (-e[0], -e[1])):
        lines[r] = lines[r][:c0] + new + lines[r][c1:]
    if apply:
        path.write_text("".join(lines), encoding="utf-8")
    return len(edits)


if __name__ == "__main__":
    apply = "--uygula" in sys.argv
    total = 0
    for f in FILES:
        n = process(f, apply)
        total += n
        if n:
            print(f"{f.name}: {n} literal")
    print(f"toplam {total} literal " + ("yazıldı" if apply else "(kuru çalışma)"))
