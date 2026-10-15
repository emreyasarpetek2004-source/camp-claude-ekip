# Kurulum Rehberi

Bu rehber, CAMP GROUP Claude sistemlerini kendi Mac'inize kurmanız içindir. Toplam süre: ~30-45 dk.

## 1. Temel araçlar

1. **Claude Code**: https://claude.com/claude-code adresinden kurun, CAMP GROUP hesabınızla giriş yapın.
2. **Homebrew** (Mac paket yöneticisi): Terminal'e şunu yapıştırın:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. **Gerekli programlar:**
   ```
   brew install git gh python@3.12 node ffmpeg
   ```
4. **Google Chrome** kurulu olmalı (WhatsApp, CRM ve PDF otomasyonları Chrome ile çalışır).

## 2. Repoyu indirin

```
gh auth login            # GitHub hesabınızla giriş
cd ~
gh repo clone emreyasarpetek2004-source/camp-claude-ekip
cd camp-claude-ekip
./kur.sh
```

`kur.sh` şunları yapar:
- `claude/agents/` → `~/.claude/agents/` (37 ajan)
- `claude/skills/` → `~/.claude/skills/` (kendi 7 skill'imiz)
- Eklentiler ve üçüncü taraf skill'ler: Superpowers, UI/UX Pro Max, planning-with-files, gstack, video-use (Claude Code ve Bun kuruluysa)
- `CLAUDE.md` → `~/.claude/CLAUDE.md` (ortak kurallar; mevcut dosyanız varsa yedekler)
- `bilgi-bankasi/` → `~/Documents/{AUSCAMP,UKCAMP,DENTCAMP} Claude/` (ajanlar buradan okur)
- `araclar/*` → `~/` altına (ör. `~/camp-reels`, `~/camp-video`)
- `araclar/bin/camp-ig-publish` → `~/bin/`

Var olan dosyaların üzerine yazmaz; çakışma olursa söyler.

## 3. Eklentiler (plugin)

`kur.sh` bunları otomatik kurar. Elle kurmak isterseniz Terminal'de:
```
claude plugin install superpowers@claude-plugins-official
claude plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
claude plugin install ui-ux-pro-max@ui-ux-pro-max-skill
claude plugin marketplace add OthmanAdi/planning-with-files
claude plugin install planning-with-files@planning-with-files
brew install oven-sh/bun/bun
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && (cd ~/.claude/skills/gstack && ./setup)
git clone https://github.com/browser-use/video-use ~/Developer/video-use
ln -s ~/Developer/video-use ~/.claude/skills/video-use
ln -s ~/Developer/video-use/skills/manim-video ~/.claude/skills/manim-video
```
video-use'un Python ortamı ve ElevenLabs anahtarı için `~/Developer/video-use/install.md` adımlarını izleyin.

## 4. Servis bağlantıları (her kişi KENDİ hesabıyla)

claude.ai → Ayarlar → Connectors bölümünden bağlayın:
**Asana, Make, Google Drive, Google Calendar, Notion, Meta Ads, Higgsfield, Canva, Lovable, Vercel.**

Ajanlar Asana proje ve section ID'lerini zaten biliyor; sizin Asana hesabınızın CAMP GROUP workspace'ine erişimi olması yeterli.

## 5. Gizli anahtarlar (repoda YOK, Marketing Koordinatöründen alınır)

Bu dosyalar güvenlik nedeniyle GitHub'a konmadı. Emre'den birebir (WhatsApp/1Password vb.) isteyin ve ilgili klasöre koyun:

| Dosya | Nereye | Ne için |
|---|---|---|
| `.env` (MAKE_WEBHOOK_URL, IG_USER_ID) | `~/Documents/<MARKA> Claude/<MARKA> Marketing/Instagram Paylasim Otomasyonu/` | Instagram yayını |
| `.asana_token` | aynı marka klasörü | Asana'ya gerçek dosya eki yükleme |
| Meta erişim token'ı | `Meta Reklam Otomasyonu/.env` | Reklam scriptleri |
| Quickesta CRM girişi | Chrome profilinde | CAMP LEAD |

## 6. Araçlara göre ek kurulum

| Araç | Ek adım |
|---|---|
| **camp-video / camp-reels** | video-use (3. adım) kurulu olmalı; camp-reels için `cd ~/camp-reels/remotion && npm install` |
| **camp-wa-core** (WhatsApp ortak çekirdek) | `cd ~/camp-lead-crm && python3 -m venv .venv && .venv/bin/pip install -e ~/camp-wa-core` |
| **camp-lead-crm** | Yukarıdaki venv + `bin/chrome-start.sh` ile otomasyon Chrome'unu açıp WhatsApp Web'e QR ile bağlanın. Ayrıntı: `PLAYBOOK.md` |
| **auscamp-memnuniyet** | `pip install -r requirements.txt`; aynı otomasyon Chrome'u. Ayrıntı: `PLAYBOOK.md` |
| **auscamp-webinar** | `npm install`; deploy yetkisi için Emre'den Vercel ekibine davet |
| **campverse-slides / katalog / rapor** | `pip install python-pptx pymupdf openpyxl`; PDF çıktısı Chrome ile alınır |

## 7. Deneme

Claude Code'u açıp şunu yazın:
```
AUSCAMP için önümüzdeki haftanın içerik takvimini kur
```
`auscamp-haftalik-planlayici` ajanı çalışıyorsa kurulum tamam.

## Önemli kurallar

- Hiçbir post onaysız yayınlanmaz veya Asana'ya girilmez.
- Yayın ve deploy komutları otomatik çalışmaz; Claude bir `.sh` hazırlar, siz `! ./dosya.sh` ile onaylarsınız.
- Ayrıntılı kurallar: `CLAUDE.md` ve her markanın `01_Caption_ve_Dil_Rehberi.md` dosyası.

> Ekip sürümünde camp-wa-core, camp-lead-crm, auscamp-memnuniyet, campverse-slides ve meta-ads-rapor yer almaz; yukarıdaki tabloda bu araçlara ait satırlar yalnızca private repo için geçerlidir.
