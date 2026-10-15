# Kapak görseli promptları

Ürettiğin görseli bu klasöre **`aus.jpg` / `uk.jpg` / `usa.jpg` / `deu.jpg`** adıyla koy, sonra:

```sh
python3 tools/prep_covers.py && python3 build_optimal.py
```

Kırpma otomatik yapılır.

## Ortak kurallar

- **En-boy oranı 16:9** (kart 452×252pt = 1.79). En az 2000 px genişlik.
- Kadraj: **bir kadın + bir erkek** diş hekimi sağ yarıda yan yana; pencere ve sembol
  yapı sol yarıda.
- Her ikisi de **Türk, Ege/İzmir tipi**: açık tenli, **bal rengi/sarışın saç ve renkli göz**
  (yeşil veya ela), Akdenizli yüz hatları, doğal ve rahat bir duruş. 28–35 yaş.
  Kadın hekim uzun sarışın saçlı, saçı toplu. Erkek hekim kısa sarışın saçlı, hafif sakallı.
- Modern, aydınlık diş kliniği; ünit koltuğu, aydınlatma ve alet tepsisi görünür.
- Gündüz doğal ışık, yumuşak gölge, temiz beyaz-gri klinik paleti.
- İkisi de lacivert scrubs, kameraya bakıp gülümsüyor.
- Metin, logo, filigran **yok**.

## Avustralya — `aus.jpg`

> A modern, brightly lit dental clinic interior. Two Turkish dentists from the Aegean coast
> of Türkiye — a woman and a man in their early 30s with fair Mediterranean complexions,
> light honey-blonde hair and green-hazel eyes — stand side by side in the right half of the frame, both in
> navy blue scrubs, relaxed and smiling at the camera. The woman has long blonde hair tied back;
> the man has short blonde hair and light stubble. Behind them on the left, a large floor-to-ceiling
> window looks out over Sydney Harbour: the Opera House and Harbour Bridge, bright morning
> light. A dental chair, operating light and instrument tray are visible in the mid-ground.
> Clean white and light grey clinical palette, shallow depth of field, photorealistic, 16:9,
> no text or logos.

## İngiltere — `uk.jpg`

> A modern, brightly lit dental clinic interior. Two Turkish dentists from the Aegean coast
> of Türkiye — a woman and a man in their early 30s with fair Mediterranean complexions,
> light honey-blonde hair and green-hazel eyes — stand side by side in the right half of the frame, both in
> navy blue scrubs, relaxed and smiling at the camera. The woman has long blonde hair tied back;
> the man has short blonde hair and light stubble. Behind them on the left, a large floor-to-ceiling
> window looks out over London: the Houses of Parliament and Big Ben with Westminster Bridge
> over the Thames, soft overcast daylight. A dental chair, operating light and instrument tray
> are visible in the mid-ground. Clean white and light grey clinical palette, shallow depth of
> field, photorealistic, 16:9, no text or logos.

## ABD — `usa.jpg`

> A modern, brightly lit dental clinic interior. Two Turkish dentists from the Aegean coast
> of Türkiye — a woman and a man in their early 30s with fair Mediterranean complexions,
> light honey-blonde hair and green-hazel eyes — stand side by side in the right half of the frame, both in
> navy blue scrubs, relaxed and smiling at the camera. The woman has long blonde hair tied back;
> the man has short blonde hair and light stubble. Behind them on the left, a large floor-to-ceiling
> window looks out over New York City: the Manhattan skyline with the Empire State Building,
> clear morning light. A dental chair, operating light and instrument tray are visible in the
> mid-ground. Clean white and light grey clinical palette, shallow depth of field,
> photorealistic, 16:9, no text or logos.

## Almanya — `deu.jpg`

> A modern, brightly lit dental clinic interior. Two Turkish dentists from the Aegean coast
> of Türkiye — a woman and a man in their early 30s with fair Mediterranean complexions,
> light honey-blonde hair and green-hazel eyes — stand side by side in the right half of the frame, both in
> navy blue scrubs, relaxed and smiling at the camera. The woman has long blonde hair tied back;
> the man has short blonde hair and light stubble. Behind them on the left, a large floor-to-ceiling
> window looks out over Berlin: the Brandenburg Gate with the Fernsehturm television tower in
> the distance, soft afternoon daylight. A dental chair, operating light and instrument tray
> are visible in the mid-ground. Clean white and light grey clinical palette, shallow depth of
> field, photorealistic, 16:9, no text or logos.

## Notlar

- **Avustralya'yı da yenilemen gerekiyor.** Mevcut `dis-orj.jpg` tek erkek hekimli; dördü
  de iki kişili olacaksa o da yeniden üretilmeli. Üretmezsen eski görsel kalır, sorun olmaz
  ama set bir kapakta farklı görünür.
- İki kişi kadraja sığmazsa "side by side in the right half" yerine **"in the right two
  thirds"** yaz; pencere daralır ama hekimler rahatlar.
- Sarışınlık ya da göz rengi tutmuyorsa şunları güçlendir: *natural light blonde hair,
  striking green eyes, fair skin, Aegean Turkish features, natural warm expression,
  no heavy makeup.*

---

# Bayraklar

Bayraklar Pexels'ten gerçek fotoğraf olarak alındı (ücretsiz, ticari, künye yok).
Kaynaklar ve yenileme komutu README'nin "Bayraklar" bölümünde.
