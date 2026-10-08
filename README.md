# Texnikum yoshlar lentasi

Toshkent tuman 1-son texnikumi — O'zbekiston Yoshlar ittifoqi boshlang'ich tashkilotining tadbirlar lentasi.
Statik sayt: GitHub Pages'da ishlaydi, hech qanday server kerak emas.

## Fayllar

| Fayl | Nima uchun |
|---|---|
| `index.html` | Saytning o'zi. Dizayn va bo'limlar shu yerda. |
| `data.json` | **Siz tahrirlaydigan fayl**: matnlar, lavhalar, nominatsiyalar, bog'lanish ma'lumotlari. |
| `images/` | Suratlar va audio. Yangi rasmni shu papkaga yuklaysiz. |

## Saytni yoqish (bir marta)

Repo sahifasida: **Settings → Pages → Source: Deploy from a branch → Branch: `main` / `(root)` → Save**.
Bir-ikki daqiqadan so'ng sayt `https://<foydalanuvchi>.github.io/<repo>/` manzilida ochiladi.

## Yangi lavha qo'shish

1. Rasmni `images/` papkasiga yuklang (**Add file → Upload files**).
2. `data.json` faylini oching → qalamcha (**Edit**) tugmasi.
3. `"reels": [` ichiga yangi blok qo'shing (vergulni unutmang):

```json
{
  "title": "Zakovat o'yini — guruhlararo bosqich",
  "davr": "zakovat",
  "sana": "2026-10-15",
  "joy": "Yig'ilishlar zali",
  "ishtirok": "60",
  "tashkilotchi": "Boshlang'ich tashkilot Kengashi",
  "matn": "Tadbir bayoni va tahlili...",
  "natija": "1-o'rin — 04-26 guruh",
  "photo": "images/zakovat.jpg"
}
```

4. Pastda **Commit changes**. Sayt 1–2 daqiqada yangilanadi.

### `davr` uchun mumkin bo'lgan qiymatlar

`ch1` `ch2` `ch3` `ch4` `yoz` `musobaqa` `tanlov` `yolovchi` `tanaffus` `kitobxon` `eko` `zakovat` `fittime`

## Bog'lanish va havolalar

`data.json` → `"site"` bo'limida: telefon, Telegram, e-pochta, manzil, qabul vaqti,
`googleForm` (murojaat uchun Google shakli havolasi), `telegramBot`, `rasmiySayt`,
`emblem` (masalan `images/emblema.png`), `profilePhoto` (`images/men.jpg`).

`shareUrl` bo'sh bo'lsa, QR kod saytning o'z manzilidan chiziladi — odatda bo'sh qoldirilgani ma'qul.

## Nominatsiya g'oliblari

`data.json` → `"tanlov"` ro'yxatida har bir nominatsiyaning `golib` va `guruh` katagini to'ldiring.

## Eslatma

JSON qoidalari: har bir qiymat qo'shtirnoq ichida, bloklar orasida vergul, oxirgi blokdan keyin vergul qo'yilmaydi.
Xatolik bo'lsa sayt "data.json o'qilmadi" deb ogohlantiradi — o'zgarishni orqaga qaytarib, qaytadan tahrirlang.
