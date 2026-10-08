#!/usr/bin/env python3
"""Telegram kanalidagi postlarni o'qib, data.json dagi "reels" ro'yxatini yangilaydi.

Kanal: t.me/s/toshkent_1khm (ochiq ko'rinish). Faqat SINCE sanasidan keyingi
postlar olinadi. "site" va "tanlov" bo'limlariga tegilmaydi.
"""
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

CHANNEL = "toshkent_1khm"
SINCE = "2026-09-01"
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data.json"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

POST_RE = re.compile(r'<div class="tgme_widget_message[^"]*"[^>]*data-post="([^"]+)"(.*?)(?=<div class="tgme_widget_message[^"]*"[^>]*data-post="|\Z)', re.S)
TEXT_RE = re.compile(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', re.S)
TIME_RE = re.compile(r'<time[^>]*datetime="([^"]+)"')
PHOTO_RE = re.compile(r'tgme_widget_message_photo_wrap[^"]*"[^>]*style="[^"]*background-image:url\(\'([^\']+)\'\)')


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def clean(fragment):
    s = re.sub(r"<br\s*/?>", "\n", fragment)
    s = re.sub(r"</p>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def parse(page):
    out = []
    for post_id, body in POST_RE.findall(page):
        num = int(post_id.split("/")[1])
        t = TEXT_RE.search(body)
        tm = TIME_RE.search(body)
        out.append({
            "num": num,
            "date": (tm.group(1)[:10] if tm else ""),
            "text": clean(t.group(1)) if t else "",
            "photos": PHOTO_RE.findall(body),
        })
    return out


def collect():
    seen, all_posts, cursor = set(), [], None
    for _ in range(40):
        url = f"https://t.me/s/{CHANNEL}" + (f"?before={cursor}" if cursor else "")
        posts = parse(fetch(url))
        if not posts:
            break
        fresh = [p for p in posts if p["num"] not in seen]
        for p in fresh:
            seen.add(p["num"])
            all_posts.append(p)
        oldest = min(posts, key=lambda p: p["num"])
        if oldest["date"] and oldest["date"] < SINCE:
            break
        cursor = oldest["num"]
    return sorted(all_posts, key=lambda p: p["num"])


def davr(text):
    s = text.lower()
    rules = [
        ("zakovat", ["zakovat", "intellektual o"]),
        ("fittime", ["sport", "futbol", "voleybol", "kross", "musobaqa", "sog'lom turmush"]),
        ("kitobxon", ["kitobxon", "kitob o", "kutubxona"]),
        ("yolovchi", ["yo'l xarakati", "yo’l xarakati", "yo'l harakati", "yhxb", "piyoda"]),
        ("eko", ["ekolog", "ko'chat", "ko’chat", "hashar", "tozalik"]),
        ("tanaffus", ["tanaffus"]),
        ("tanlov", ["ko'rik-tanlov", "ko’rik-tanlov", "tanlov g'olib"]),
    ]
    for key, words in rules:
        if any(w in s for w in words):
            return key
    return "ch1"


def title_of(text, num):
    first = next((l.strip() for l in text.split("\n") if l.strip()), "")
    first = re.sub(r"^[^\w“\"']+", "", first)
    if not first:
        return f"Lavha №{num}"
    return first if len(first) <= 95 else first[:93].rstrip() + "…"


def body_of(text):
    lines = [l.strip() for l in text.split("\n")]
    lines = [l for l in lines[1:] if l and not l.startswith("#")]
    body = "\n".join(lines)
    body = re.sub(r"\n?Bizni kuzating.*$", "", body, flags=re.S)
    return body.strip()


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    posts = [p for p in collect() if p["date"] >= SINCE and (p["photos"] or len(p["text"]) > 60)]
    posts = [p for p in posts if p["text"].strip() != "Channel photo updated"]

    reels = []
    for p in posts:
        reels.append({
            "title": title_of(p["text"], p["num"]),
            "davr": davr(p["text"]),
            "sana": p["date"],
            "joy": "Toshkent tuman 1-son texnikumi",
            "ishtirok": "",
            "tashkilotchi": "",
            "matn": body_of(p["text"]),
            "natija": "",
            "photo": p["photos"][0] if p["photos"] else "",
            "photos": p["photos"][:8],
            "link": f"https://t.me/{CHANNEL}/{p['num']}",
        })
    reels.sort(key=lambda r: r["sana"], reverse=True)

    # Qo'lda yozilgan lavhalar (Telegramga bog'lanmaganlari) saqlanib qoladi
    manual = [r for r in data.get("reels", []) if not str(r.get("link", "")).startswith(f"https://t.me/{CHANNEL}/")]
    data["reels"] = reels + manual

    new = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if DATA.read_text(encoding="utf-8") == new:
        print("o'zgarish yo'q")
        return 0
    DATA.write_text(new, encoding="utf-8")
    print(f"{len(reels)} ta lavha yangilandi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
