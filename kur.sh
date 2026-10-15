#!/bin/bash
# CAMP GROUP Claude sistemleri: yerel kurulum. Var olan dosyanin uzerine yazmaz.
set -u
R="$(cd "$(dirname "$0")" && pwd)"

kopyala() { # kaynak hedef
  if [ -e "$2" ]; then echo "  ATLANDI (zaten var): $2"; else mkdir -p "$(dirname "$2")"; cp -R "$1" "$2"; echo "  + $2"; fi
}

echo "Ajanlar..."
for f in "$R"/claude/agents/*.md; do kopyala "$f" "$HOME/.claude/agents/$(basename "$f")"; done

echo "Skill'ler..."
for d in "$R"/claude/skills/*/; do kopyala "${d%/}" "$HOME/.claude/skills/$(basename "$d")"; done

echo "Ortak kurallar (CLAUDE.md)..."
if [ -e "$HOME/.claude/CLAUDE.md" ]; then
  cp "$HOME/.claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md.yedek"
  { echo; cat "$R/CLAUDE.md"; } >> "$HOME/.claude/CLAUDE.md"
  echo "  mevcut dosyaya eklendi (yedek: CLAUDE.md.yedek)"
else
  kopyala "$R/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
fi

echo "Bilgi bankalari..."
for d in "$R"/bilgi-bankasi/*/; do
  hedef="$HOME/Documents/$(basename "$d")"; mkdir -p "$hedef"
  (cd "$d" && find . -type f) | while read -r f; do kopyala "$d/$f" "$hedef/$f"; done
done

echo "Araclar..."
for d in "$R"/araclar/*/; do
  ad="$(basename "$d")"
  if [ "$ad" = "bin" ]; then
    mkdir -p "$HOME/bin"; kopyala "$d/camp-ig-publish" "$HOME/bin/camp-ig-publish"; chmod +x "$HOME/bin/camp-ig-publish" 2>/dev/null
  else
    kopyala "${d%/}" "$HOME/$ad"
  fi
done

echo "Eklentiler ve ucuncu taraf skill'ler..."
if command -v claude >/dev/null 2>&1; then
  claude plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill >/dev/null 2>&1
  claude plugin marketplace add OthmanAdi/planning-with-files >/dev/null 2>&1
  for p in superpowers@claude-plugins-official ui-ux-pro-max@ui-ux-pro-max-skill planning-with-files@planning-with-files; do
    claude plugin install "$p" >/dev/null 2>&1 && echo "  + $p" || echo "  ! $p kurulamadi (Claude Code icinde /plugin install $p deneyin)"
  done
else
  echo "  ! claude komutu yok: once Claude Code'u kurun, sonra kur.sh'i tekrar calistirin"
fi
if [ -d "$HOME/.claude/skills/gstack" ]; then echo "  ATLANDI (zaten var): gstack"
elif command -v bun >/dev/null 2>&1; then
  git clone -q --single-branch --depth 1 https://github.com/garrytan/gstack.git "$HOME/.claude/skills/gstack" && (cd "$HOME/.claude/skills/gstack" && ./setup) && echo "  + gstack"
else echo "  ! gstack icin Bun gerekli: brew install oven-sh/bun/bun, sonra kur.sh'i tekrar calistirin"; fi
if [ -d "$HOME/Developer/video-use" ]; then echo "  ATLANDI (zaten var): video-use"
else
  mkdir -p "$HOME/Developer" && git clone -q https://github.com/browser-use/video-use "$HOME/Developer/video-use" && echo "  + video-use (Python kurulumu: ~/Developer/video-use/install.md)"
fi
[ -e "$HOME/.claude/skills/video-use" ] || ln -s "$HOME/Developer/video-use" "$HOME/.claude/skills/video-use"
[ -e "$HOME/.claude/skills/manim-video" ] || ln -s "$HOME/Developer/video-use/skills/manim-video" "$HOME/.claude/skills/manim-video"

echo
echo "Bitti. Sirada: KURULUM.md 4-6. adimlar (servis baglantilari, gizli anahtarlar, arac kurulumlari)."
