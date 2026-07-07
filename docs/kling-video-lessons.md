# Kling image-to-video ders notları (2026-07-07)

Coremagna real estate video sample'ı (Kingham cottage, `real-estate-videos.html`)
için Kling 2.5 Turbo Pro (kie.ai) ile yapılan üretimlerden çıkan sonuçlar.
Bir sonraki video üretim turunda (bu proje veya başka biri) baştan
tekrarlamamak için.

## 1. "Slow push-in" her sahneye yazılırsa fotoğraf + zoom hissi verir

İlk turda 7 sahnenin neredeyse tamamına "camera slowly pushes in / dolly
forward" yazıldı. Sonuç: kullanıcı "sanki bir fotoğrafı koymuş, zoom in
yapıyor gibi" dedi — haklıydı. Düz bir push-in'de foreground/background
aynı hızda büyür, gözün "3D uzayda kamera" diye okuduğu asıl ipucu
(parallax — ön/arka planın farklı hızda kayması) yoktur.

**Düzeltme denemesi (yarım başarı):** Prompt'u "gerçek 3D kamera hareketi,
zoom değil" + yakın bir foreground nesnesi (tezgah kenarı, saksı) + güçlü
parallax talebiyle yeniden yazmak bazı sahnelerde işe yaradı (mutfak —
tezgah kenarı yakınken model gerçek bir kayma üretti), bazılarında
yaramadı (dış cephe — üç farklı prompt denemesine rağmen kamera neredeyse
hiç hareket etmedi).

## 2. Kling saf yanal kaydırma (pan/track) konusunda çok isteksiz

Muhtemel sebep: yanal hareket, kare kenarında **daha önce hiç görünmemiş
içerik** üretmeyi gerektirir (kamera sağa kayınca solda yeni bahçe/duvar
parçası ortaya çıkmalı). Model bunu riskli bulup "güvenli" tarafı seçiyor:
neredeyse donuk kalıyor. Bu bir prompt yazım sorunu değil, tek görselden
üretimin (image-to-video) yapısal sınırı gibi görünüyor. `cfg_scale`'i
0.5'ten 0.7-0.8'e çıkarmak biraz yardımcı oluyor ama garanti değil.

## 3. Asıl bulgu: yavaş+temiz değil, hızlı+enerjik olan işe yarıyor

İki referans videoyu (rakip "Rendy" promosu + kullanıcının kendi
influencer-avatarlı `killer_reel.mp4`'ü) kare kare incelemek asıl dersi
verdi:

- Rendy videosunda etkileyicilik kamera hareketinden değil, **ışık/zaman
  dönüşümünden** (gündüz → alacakaranlık → gece, pencereler ışıklanıyor,
  mumlar yanıyor) ve **çok sık kesmeden** (yarım saniyede bir farklı açı)
  geliyordu. Kamera kendisi neredeyse hep sabit.
- `killer_reel.mp4`'te ise **hızlı FPV-drone tarzı uçuş + belirgin motion
  blur** var. Kamera kapıdan/koridordan "içeri uçuyor", ön plandaki
  mobilyalar bulanıklaşarak geçiyor.

Ortak nokta: **hız (ya kesme hızı ya da hareket hızı) modelin çizgi/doku
tutarsızlıklarını gözden saklıyor.** Yavaş ve "temiz" kalmaya çalışmak
tam tersi etki yapıyor — hata görünür kalıyor ve model de hatadan
kaçınmak için hareketi bastırıyor.

## 4. Bir sonraki deneme için doğru prompt yönü

Slow/gentle/calm yerine:

- "FPV drone, fast energetic forward flight, strong cinematic motion blur"
- Kameranın gireceği somut bir hedef tarif et (kapı, pencere, şömine) —
  "bursts through the doorway", "accelerates toward"
- Ön plandaki nesnelerin **bilinçli olarak bulanıklaşmasını** iste
  ("rush past in the foreground", "blur past")
- `cfg_scale` 0.75-0.8 (varsayılan 0.5 çok sıkı, hareketi bastırıyor)
- Negative prompt'a `static shot, frozen frame, no movement, still photo`
  ekle — Kling'i donuk kalmaktan caydırıyor

Alternatif/tamamlayıcı yön (ışık dönüşümü): dış cephe gündüz fotoğrafını
önce bir görsel editörle akşam versiyonuna çevirip, videoyu o akşam
görselinden ürettirmek — before gündüz fotoğrafı, after akşam videosu.
Henüz denenmedi.

## 5. Pratik notlar

- kie.ai `kling/v2-5-turbo-image-to-video-pro` modelinin tam id'si budur
  (dokümanlardaki "v25-turbo-..." kısa formu API'de 422 döner).
- `cfg_scale` yalnızca 0.1'in katları kabul ediliyor (0.75 → 500 hata
  "must be a multiple of 0.1").
- kie.ai upload endpoint'i (`kieai.redpandaai.co/api/file-stream-upload`)
  ara sıra 401/timeout veriyor, birkaç saniye sonra tekrar deneyince
  çalışıyor — anahtar/bakiye sorunu değil, geçici servis dalgalanması.
- 5 saniyelik bir video ~42 kredi (~$0.21) tutuyor.
- Üretilen videoyu değerlendirirken tek kareye bakmak yeterli değil —
  başlangıç/orta/son karesini referans çizgileriyle üst üste koyup
  gerçekten hareket olup olmadığını doğrulamak gerekiyor (göz tek kareden
  "hareketli mi" diye ayırt edemiyor, kıyaslamalı bakmak şart).
