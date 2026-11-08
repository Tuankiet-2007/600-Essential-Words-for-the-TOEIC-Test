"""Parse Answer Key OCR -> scripts/data/answer_key.json (task-8).

Chay: py -3.11 scripts/parse_answer_key.py

CACH LAM: quet MOT LAN qua 4 file theo dung thu tu trang, mang theo trang thai
"bai dang doc" va "muc dang doc" XUYEN QUA ranh gioi file.

Ly do phai lam vay: sach in 2 cot nen mot bai co the bi cat qua 2 trang sach.
Vi du Lesson 37 Airlines: 335_answer_key.md ket thuc ngay sau 12 dap an
"Words In Context", con 23 dap an "Word Practice" cua no nam o 3 DONG DAU cua
336_answer_key.md. Neu reset trang thai moi file thi mat trang WP cua bai 37.

Quy tac: dong "Words in Context:" / "Word Practice:" luon thuoc ve LESSON HEADER
gan nhat phia truoc, BAT KE file nao.

NGUYEN TAC: KHONG BIA. Cho OCR khong doc duoc thi de trong + ghi warning.
"""

from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AK_DIR = os.path.join(ROOT, "extracted_data", "mineru_md", "answer_key")
OUT_PATH = os.path.join(ROOT, "scripts", "data", "answer_key.json")
LESSONS_JSON = os.path.join(ROOT, "public", "lessons_json")

FILES = ["333_answer_key.md", "334_answer_key.md", "335_answer_key.md", "336_answer_key.md"]

# ---------------------------------------------------------------------------
# Chuan hoa OCR
# ---------------------------------------------------------------------------

_OCR_NUM = {
    "IO": "10", "lO": "10", "I0": "10", "1O": "10", "l0": "10",
    "II": "11", "ll": "11", "Il": "11", "lI": "11",
    "li": "11", "Li": "11", "LI": "11", "iI": "11", "i1": "11", "1l": "11", "1I": "11",
    "l2": "12", "I2": "12", "i2": "12",
    "l3": "13", "I3": "13", "i3": "13",
    "l4": "14", "I4": "14", "i4": "14",
    "l5": "15", "I5": "15", "i5": "15",
    "l6": "16", "I6": "16", "i6": "16",
    "l7": "17", "I7": "17", "i7": "17",
    "l8": "18", "I8": "18", "i8": "18",
    "l9": "19", "I9": "19", "i9": "19",
}
_ORD_CHARS = {"l": "1", "I": "1", "i": "1", "O": "0", "o": "0", " ": ""}


def fix_num(tok):
    """Chuan hoa token so thu tu OCR -> int, None neu khong doc duoc."""
    t = (tok or "").strip().strip(".,:;")
    if t in _OCR_NUM:
        return int(_OCR_NUM[t])
    if not t.isdigit():
        t = "".join(_ORD_CHARS.get(c, c) for c in t)
    return int(t) if t.isdigit() and 1 <= int(t) <= 99 else None


# Mot "muc" = <so> <phan cach> <gia tri>.
#
# HAI CAM BAY OCR da gap that va cach xu ly:
#
# (1) 'l'/'I'/'O' nam BEN TRONG tu thuong bi nhan nham la so:
#       "6. loyalty" -> khop 'l' -> 1 = 'oyalty'
#       "9. layout"  -> khop 'l' -> 1 = 'ayout' (de mat so 9!)
#     => Phai doi hoi co DAU PHAN CACH ([.,]) sau so, HOAC so dung ngay truoc
#        gia tri ma khong dinh chu. Cach chac chan: bat buoc co [.,] hoac
#        truong hop "14B"/"17 D" (so that + 1 chu HOA).
#
# (2) 'IO' = 10, 'II' = 11, 'li' = 11 (chuoi 2 ky tu OCR nham). Cac dang nay
#     LUON di kem dau '.' hoac ',' hoac dung truoc 1 chu HOA.
#
# Vi vay: uu tien dang CO dau phan cach; chi chap nhan dang KHONG co dau phan cach
# khi so that su gom toan chu SO (vd "14B", "8 C"), tranh nham voi chu 'l'.
ENTRY_RE = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?:"
    # dang A: <so> [.,] <khoang trang> <gia tri>   -> "1. B", "l.c", "IO. A", "12, D"
    # Chap nhan ca 'i' (OCR cua '1') va dau '-' (OCR cua '.') : "i. B", "7-A"
    r"(?P<num1>[0-9OIl i]{1,2})\s*[.,\u2014\u2013-]\s*(?=[A-Za-z(])"
    r"|"
    # dang B: <so> <khoang trang> <chu HOA don>    -> "17 D"
    r"(?P<num2>[0-9OIl i]{1,2})\s+(?=[A-Z](?![a-z]))"
    r"|"
    # dang C: <so> <chu HOA dinh lien>             -> "14B"
    r"(?P<num3>[0-9]{1,2})(?=[A-D](?![a-z]))"
    r"|"
    # dang D: <so> [.,] <ky tu OCR cua chu cai>    -> "15.8" (8 = B)
    # Chi nhan 8/4 vi do la hai chu cai hay bi OCR nham thanh so.
    r"(?P<num4>[0-9]{1,2})\s*[.,]\s*(?=[84](?![0-9]))"
    r")"
)


def split_entries(text, kind):
    """Tach chuoi thanh dict {int: str}. kind='word' | 'abc'.

    Tra ve (entries, orphan_values). 'abc' chuan hoa ve 1 chu HOA A-D.

    `orphan_values` = cac gia tri A-D dung mot minh (bi OCR lam mat so thu tu).
    Chung KHONG bi bo im lang: tra ve de buoc sau gan lai vao o trong neu xac dinh duoc.
    """
    out, orphans = {}, []
    text = " ".join(text.split())
    marks = []
    for m in ENTRY_RE.finditer(text):
        raw = (m.group("num1") or m.group("num2")
               or m.group("num3") or m.group("num4"))
        n = fix_num(raw)
        if n is not None:
            marks.append((m.start(), m.end(), n))

    for i, (s, e, n) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        val = text[e:end].strip().strip(".,;:")
        if not val:
            continue
        if kind == "abc":
            # Chu cai trong value: co the co nhieu (vd "C C" khi mat so o giua).
            letters = re.findall(r"[A-Da-d]", val)
            if letters:
                out[n] = letters[0].upper()
                for extra in letters[1:]:
                    orphans.append(extra.upper())
                continue
            # OCR hay doc 'B' thanh '8' va 'A' thanh '4' (giong nhau ve hinh dang).
            # Chi ap dung khi value dung 1 ky tu 8/4 va khong co chu cai A-D nao.
            # Ca da kiem chung: L27 "15.8" -> muc 15 = 'B'.
            if re.fullmatch(r"[84]", val):
                out[n] = "B" if val == "8" else "A"
                orphans.append("__OCR_%s__" % val)
            # value khong doc duoc (vd "16." khong co gia tri) -> bo qua, KHONG bia
        else:
            out[n] = val
    return out, orphans



# ---------------------------------------------------------------------------
# Quet 1 lan, giu trang thai xuyen file
# ---------------------------------------------------------------------------

LESSON_RE = re.compile(r"^\s*Lesson\s+([0-9OIl]{1,2})\s+(.+?)\s*$")
WIC_RE = re.compile(r"^\s*Words?\s+[Ii]n\s*[Cc]ontext\s*:?\s*(.*)$")
WP_RE = re.compile(r"^\s*Word\s+Practice\s*:?\s*(.*)$")
REVIEW_RE = re.compile(r"^\s*Word\s+Review", re.I)
GROUP_RE = re.compile(r"^\s*Lessons?\s+[\dOIl]+\s*[\u2014\u2013-]", re.I)
PAGE_NOISE_RE = re.compile(r"^\s*[0-9]{2,3}\s*(\s*600\s+ESSENT.*)?$", re.I)


def parse_all():
    """Tra ve (lessons, titles, notes). lessons[lid] = {wic:{}, wp:{}, warns:[]}."""
    lessons, titles, notes = {}, {}, []
    cur_lid = None
    mode = None                     # 'wic' | 'wp' | None

    def rec(lid):
        return lessons.setdefault(lid, {"words_in_context": {}, "word_practice": {},
                                        "warnings": [],
                                        "_wic_orphans": [], "_wp_orphans": []})

    for fn in FILES:
        path = os.path.join(AK_DIR, fn)
        if not os.path.isfile(path):
            notes.append("thieu file %s" % fn)
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()

        for raw in lines:
            s = raw.strip()
            if not s:
                continue
            if PAGE_NOISE_RE.match(s):
                continue

            # Tieu de nhom "Lessons 21-25 Financing and Budgeting" -> bo qua
            if GROUP_RE.match(s):
                continue

            m = LESSON_RE.match(s)
            if m:
                lid = fix_num(m.group(1))
                title = m.group(2).strip()
                if lid is None or lid > 50:
                    continue
                cur_lid = lid
                titles.setdefault(lid, title)
                mode = None
                rec(lid)
                continue

            if REVIEW_RE.match(s):
                # "Word Review" khong thuoc bai nao -> ket thuc muc hien tai.
                mode = None
                continue

            m = WIC_RE.match(s)
            if m:
                mode = "wic"
                if cur_lid is None:
                    notes.append("%s: 'Words in Context' truoc moi Lesson -> bo qua" % fn)
                    continue
                got, orphan = split_entries(m.group(1), "word")
                for k, v in got.items():
                    rec(cur_lid)["words_in_context"][k] = v
                rec(cur_lid)["_wic_orphans"] += orphan
                continue

            m = WP_RE.match(s)
            if m:
                mode = "wp"
                if cur_lid is None:
                    notes.append("%s: 'Word Practice' truoc moi Lesson -> bo qua" % fn)
                    continue
                got, orphan = split_entries(m.group(1), "abc")
                for k, v in got.items():
                    rec(cur_lid)["word_practice"][k] = v
                rec(cur_lid)["_wp_orphans"] += orphan
                continue

            # Dong noi tiep cua muc dang doc (OCR xuong dong)
            if mode == "wic" and cur_lid is not None:
                got, orphan = split_entries(s, "word")
                for k, v in got.items():
                    rec(cur_lid)["words_in_context"].setdefault(k, v)
                rec(cur_lid)["_wic_orphans"] += orphan
            elif mode == "wp" and cur_lid is not None:
                got, orphan = split_entries(s, "abc")
                for k, v in got.items():
                    rec(cur_lid)["word_practice"].setdefault(k, v)
                rec(cur_lid)["_wp_orphans"] += orphan
                # Gia tri bi tach khoi so cua no (OCR xuong dong):
                #   L40: "... 15. A 16." roi dong sau "B 17 A"
                #        -> 'B' dung dau dong, TRUOC so 17 => la gia tri cua muc 16.
                led = re.match(r"^\s*([A-D])(?=\s|$)", s)
                if led:
                    rec(cur_lid)["_wp_orphans"].append(led.group(1))

    # Chuan hoa khoa ve CHUOI so ("1".."12"/"23") TRUOC khi sua/khoi phuc, de moi
    # buoc sau dung nhat quan. (Trong qua trinh parse khoa la int; neu de lan lon
    # int/str thi buoc kiem o trong se luon bao thieu.)
    for r in lessons.values():
        r["words_in_context"] = {str(k): v for k, v in r["words_in_context"].items()}
        r["word_practice"] = {str(k): v for k, v in r["word_practice"].items()}

    _post_fix(lessons, notes)
    return lessons, titles, notes


def _post_fix(lessons, notes):
    """Sua cac ca OCR nham so da duoc XAC MINH BANG TAY (khong bia)."""
    # 12 tu muc tieu cua tung bai (lay tu JSON) - dung lam bang chung doi chieu.
    targets = {}
    for lid in range(1, 51):
        p = os.path.join(LESSONS_JSON, "lesson_%02d.json" % lid)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                targets[lid] = [(w.get("word") or "").lower()
                                for w in json.load(f).get("words_to_learn", [])]

    for lid, r in sorted(lessons.items()):
        wic = r["words_in_context"]

        # L05/L06: sach chi co 12 muc, nhung OCR doc "21./22." (nham so TRANG).
        # Bang chung: L05 dien 1..10 roi "21. location / 22. register".
        # 12 tu muc tieu cua L05 gom 'location' va 'register' -> day chinh la
        # muc 11 va 12. Doi chieu voi danh sach tu muc tieu truoc khi sua.
        if lid in (5, 6):
            tset = set(targets.get(lid, []))
            for k in (21, 22, 23):
                ks, kd = str(k), str(k - 10)
                if ks in wic and kd not in wic and 1 <= k - 10 <= 12:
                    val = wic[ks]
                    hit = val.lower() in tset or any(
                        val.lower() in t or t in val.lower() for t in tset)
                    wic[kd] = wic.pop(ks)
                    r["warnings"].append(
                        "WIC: %d -> %d (OCR nham so trang; '%s' %s trong 12 tu muc tieu)"
                        % (k, k - 10, val, "CO" if hit else "KHONG"))

        # L49 WP: OCR doc "7-A" -> 'A' (da xu ly o tang tokenizer, day la luoi an toan)
        wp = r["word_practice"]
        for k, v in list(wp.items()):
            if v not in ("A", "B", "C", "D"):
                fixed = re.sub(r"[^A-D]", "", v.upper())
                if len(fixed) == 1:
                    wp[k] = fixed
                    r["warnings"].append("WP: %r -> %r (bo ky tu rac)" % (v, fixed))

    # Sau khi da sua cac ca nghiem ngat, moi khoi phuc theo vi tri.
    _recover_gaps(lessons)


def _recover_gaps(lessons):
    """Khoi phuc cac muc bi OCR lam MAT SO THU TU nhung GIA TRI van con.

    Nguyen tac bat buoc: CHI dien khi so o trong == so gia tri mo coi VA vi tri
    la duy nhat. Neu so gia tri < so o trong thi KHONG the biet dap an -> de trong.

    Cac ca cu the (da doc file goc lam bang chung):
      L27 WP: "15.8"               -> '8' la OCR cua 'B' (nham chu B thanh so 8)
      L44 WP: "3. C C 5. B"        -> gia tri 'C' mo coi thu 2 = muc 4 (mat so)
      L48 WIC: "10. regardless li. aspect" -> 'li.' = OCR cua '11.'
      L40 WP: "... 15. A 16." + "B 17 A"   -> 'B' sau '16.' = gia tri muc 16
    """
    # L48 WIC: 'li. aspect' bi gop vao muc 10 -> tach thanh muc 11.
    r48 = lessons.get(48)
    if r48:
        v = r48["words_in_context"].get("10", "")
        m = re.match(r"^(.*?)\s+[Ll][Ii]\.\s*(.+)$", v)
        if m and "11" not in r48["words_in_context"]:
            r48["words_in_context"]["10"] = m.group(1).strip()
            r48["words_in_context"]["11"] = m.group(2).strip()
            r48["warnings"].append(
                "WIC: tach 'li.' -> muc 11 = %r (OCR nham '11')" % m.group(2).strip())

    # L27 WP: '15.8' -> chu '8' la OCR cua 'B' (nham chu B thanh so 8).
    # Danh dau __OCR_x__ duoc tokenizer dat vao _wp_orphans -> chuyen thanh warning
    # roi loai khoi danh sach orphan that (de khong bi tinh la gia tri mo coi).
    for lid, r in sorted(lessons.items()):
        marks = [o for o in r["_wp_orphans"] if o.startswith("__OCR_")]
        if marks:
            r["_wp_orphans"] = [o for o in r["_wp_orphans"]
                                if not o.startswith("__OCR_")]
            for mk in marks:
                d = mk.strip("_").replace("OCR_", "")
                r["warnings"].append(
                    "WP: OCR doc chu %s thanh so %s o mot muc (da doi lai thanh chu)"
                    % ("B" if d == "8" else "A", d))

    # L40 WP: so 16 bi OCR an, gia tri 'B' bi tach sang dong ke tiep (thanh orphan).
    r40 = lessons.get(40)
    if r40 and "16" not in r40["word_practice"] and r40["_wp_orphans"]:
        if len(r40["_wp_orphans"]) == 1:
            r40["word_practice"]["16"] = r40["_wp_orphans"].pop(0)
            r40["warnings"].append(
                "WP: muc 16 = %r (so bi OCR an, gia tri nam o dong ke tiep)"
                % r40["word_practice"]["16"])

    # Quy tac TONG QUAT: neu so o trong == so gia tri mo coi thi dien theo thu tu.
    for lid, r in sorted(lessons.items()):
        wp, orphans = r["word_practice"], list(r["_wp_orphans"])
        gaps = [n for n in range(1, 24) if str(n) not in wp]
        if orphans and len(orphans) == len(gaps):
            for n, v in zip(gaps, orphans):
                wp[str(n)] = v
                r["warnings"].append(
                    "WP: muc %d = %r (so thu tu bi OCR an, gia tri con nguyen)"
                    % (n, v))
            r["_wp_orphans"] = []
        elif orphans:
            # KHONG du bang chung -> KHONG dien. Bao ro de nguoi doc biet.
            r["warnings"].append(
                "WP: %d gia tri mo coi nhung %d o trong (thieu %s) -> KHONG dien"
                " vi khong xac dinh duoc vi tri: orphans=%s"
                % (len(orphans), len(gaps), gaps, orphans))

    # Bao ro cac bai con thieu muc vi OCR XOA HAN (khong co gia tri nao de khoi phuc).
    for lid, r in sorted(lessons.items()):
        wic_gaps = [n for n in range(1, 13) if str(n) not in r["words_in_context"]]
        wp_gaps = [n for n in range(1, 24) if str(n) not in r["word_practice"]]
        if wic_gaps:
            r["warnings"].append(
                "WIC: thieu muc %s — OCR xoa han, KHONG the khoi phuc (khong bia)" % wic_gaps)
        if wp_gaps and not r["_wp_orphans"]:
            r["warnings"].append(
                "WP: thieu muc %s — OCR xoa han ca so lan gia tri, KHONG the khoi phuc"
                " (khong bia)" % wp_gaps)


def main():
    titles_json = {}
    for lid in range(1, 51):
        p = os.path.join(LESSONS_JSON, "lesson_%02d.json" % lid)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                titles_json[lid] = json.load(f).get("title", "")

    lessons, titles, notes = parse_all()

    out = {}
    for lid in range(1, 51):
        r = lessons.get(lid, {"words_in_context": {}, "word_practice": {},
                              "warnings": []})
        out[str(lid)] = {
            "lesson_id": lid,
            "title": titles_json.get(lid) or titles.get(lid, ""),
            "words_in_context": {str(k): v for k, v in
                                 sorted(r["words_in_context"].items(), key=lambda kv: int(kv[0]))},
            "word_practice": {str(k): v for k, v in
                              sorted(r["word_practice"].items(), key=lambda kv: int(kv[0]))},
            "warnings": r["warnings"],
        }

    # LUON ghi file, ke ca khi con muc thieu (de UI noi duoc phan da co).
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("  -> da ghi %s" % os.path.relpath(OUT_PATH, ROOT))

    print("\n=== BAO CAO PARSE ANSWER KEY ===\n")
    bad_wic, bad_wp, ok = [], [], []
    for lid in range(1, 51):
        wic, wp = out[str(lid)]["words_in_context"], out[str(lid)]["word_practice"]
        miss_wic = [n for n in range(1, 13) if str(n) not in wic]
        miss_wp = [n for n in range(1, 24) if str(n) not in wp]
        bad = [n for n, v in wp.items() if v not in ("A", "B", "C", "D")]
        if bad:
            print("  [LOI] L%02d dap an khong phai A-D: %s"
                  % (lid, [(n, wp[n]) for n in sorted(bad, key=int)]))
        if miss_wic or miss_wp:
            if miss_wic:
                bad_wic.append((lid, miss_wic))
            if miss_wp:
                bad_wp.append((lid, miss_wp))
            print("  [THIEU] L%02d '%s' WIC %d/12 thieu %s | WP %d/23 thieu %s"
                  % (lid, out[str(lid)]["title"], 12 - len(miss_wic), miss_wic or "-",
                     23 - len(miss_wp), miss_wp or "-"))
        else:
            ok.append(lid)
            print("  [DU]    L%02d '%s' WIC 12/12, WP 23/23"
                  % (lid, out[str(lid)]["title"]))

    print("\n--- TONG KET ---")
    print("  bai DU 12 WIC + 23 WP : %d / 50" % len(ok))
    print("  bai thieu WIC         : %d %s" % (len(bad_wic), [l for l, _ in bad_wic]))
    print("  bai thieu WP          : %d %s" % (len(bad_wp), [l for l, _ in bad_wp]))
    print("  tong muc WIC thieu    : %d" % sum(len(m) for _, m in bad_wic))
    print("  tong muc WP thieu     : %d" % sum(len(m) for _, m in bad_wp))
    if notes:
        for n in notes:
            print("  [NOTE] %s" % n)
    for lid in range(1, 51):
        for w in out[str(lid)]["warnings"]:
            print("  [WARN] L%02d %s" % (lid, w))

    total_missing = sum(len(m) for _, m in bad_wic) + sum(len(m) for _, m in bad_wp)
    return 0 if (len(ok) == 50 and total_missing == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
