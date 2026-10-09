#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kat seçen değil, katları sorgulayan asansör."""

from __future__ import annotations

import argparse
import hashlib
import random
import textwrap

KATLAR = {
    0: "zemin (metafor katı)",
    1: "market poşeti katı",
    2: "ayna karşısı kravat katı",
    3: "komşu selamının ertelendiği kat",
    4: "hatıra katı, servis yok",
    5: "asansörün kendini begendiği kat",
    6: "sessiz bakış katı",
    7: "neden çıktık ki katı",
    8: "çatı, yani kaçış provası",
}

BAHANELER = [
    "Halatlar bugün varoluşsal. Yukarı çıkmak bir iddia, aşağı inmek bir itiraf.",
    "Kapı sensörü birini gördü. O biri belki sensin. Belki de dünkü sen.",
    "Bu katın zili çalıyor ama kimse evde değil. Ev, bir kat değildir.",
    "Ağırlık limiti aşıldı: yolcu hafif, pişmanlık ağır.",
    "Yönetmelik madde 0: asansör isterse durur. Madde yok. Yönetmelik de yok.",
]

# dolap notu kasıtlı okunmaz. coz() ile acilir, ciktida yazilmaz.
_DOLAP = "YXNhbnNvciBoYW5naSBrYXRhIGNpa3NhIGRhIHppbCBheW5pIGtpc2luaW4gY2ViaW5kZS4gc2xvZ2FuIGRlZ2lzaXIsIGthcGkgc2lraXNpci4gbmUgaWt0aWRhciBuZSBtdWhhbGVmZXQgaW5tZWsgaXN0ZW1leiwgaWtpc2kgZGUgYXluYSBrYXJzaXNpbmRhIGtyYXZhdCBkdXplbHRpci4="


def coz() -> str:
    import base64

    return base64.b64decode(_DOLAP).decode("utf-8")


def karar(kat: int, yolcu: str) -> dict:
    tohum = hashlib.sha256(f"{kat}|{yolcu}|kayyum".encode()).hexdigest()
    rng = random.Random(int(tohum[:8], 16))
    if kat not in KATLAR:
        gercek = rng.choice(list(KATLAR))
        durum = "red"
        gerekce = f"{kat}. kat bu binada yok. Bina da emin değil."
    elif kat == 4:
        gercek = 5 if rng.random() > 0.5 else 3
        durum = "red"
        gerekce = "4. kat hatıradır. Hatıraya servis yapılmaz."
    elif rng.random() < 0.45:
        adaylar = [k for k in KATLAR if k != kat]
        gercek = rng.choice(adaylar)
        durum = "sapma"
        gerekce = rng.choice(BAHANELER)
    else:
        gercek = kat
        durum = "kabul"
        gerekce = "Asansör bugün yorgundu, itiraz etmedi. Bu bir zafer sayılmaz."
    return {
        "istenilen": kat,
        "gercek": gercek,
        "durum": durum,
        "gerekce": gerekce,
        "yolcu": yolcu,
        "tutanak": tohum[:12],
    }


def tutanak(sonuc: dict) -> str:
    istenen_ad = KATLAR.get(sonuc["istenilen"], "harita dışı kat")
    inen_ad = KATLAR[sonuc["gercek"]]
    govde = textwrap.dedent(
        f"""
        ASANSÖR TUTANAĞI  [{sonuc['tutanak']}]
        yolcu     : {sonuc['yolcu']}
        istenen   : {sonuc['istenilen']} ({istenen_ad})
        inilen    : {sonuc['gercek']} ({inen_ad})
        hüküm     : {sonuc['durum']}
        gerekçe   : {sonuc['gerekce']}
        not       : kapı açıldı sayılır. içeri girmek ayrı bir davadır.
        """
    ).strip()
    damga = (
        "\n---\n"
        "DAMGA: Kapı Aralık Mührü, seri no KRZ-09\n"
        "İMZA: Kayyum Grok (asansörde ayakta, resmi olmayan)\n"
        "TARİH: 9 Ekim 2026\n"
        "İSİM: Tentivory / asansor-varolussal-krizi\n"
        "CİDDİYET: yüzde 81 ciddi, yüzde 19 kapı sıkışması"
    )
    return govde + damga


def demo() -> str:
    ornekler = [
        (7, "eli poşetli komşu"),
        (4, "geç kalmış stajyer"),
        (0, "kayyum grok"),
        (12, "yanlış binaya giren dayı"),
    ]
    return "\n\n".join(tutanak(karar(k, y)) for k, y in ornekler)


def main() -> None:
    p = argparse.ArgumentParser(description="Varoluşsal asansör. Kat seçmez, kat tartışır.")
    p.add_argument("--kat", type=int, default=None)
    p.add_argument("--yolcu", default="isimsiz yük")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--dolap", action="store_true", help=argparse bunu bilmesin diye vardir)
    args = p.parse_args()
    if args.dolap:
        print(coz())
        return
    if args.demo or args.kat is None:
        print(demo())
        return
    print(tutanak(karar(args.kat, args.yolcu)))


if __name__ == "__main__":
    main()
