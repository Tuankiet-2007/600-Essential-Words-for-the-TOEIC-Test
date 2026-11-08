"""Chay MinerU (ban cai tai D:\\CODE\\vibecode\\TOOL\\mineru) tren anh scan cua sach,
roi chuyen Markdown -> JSON dung schema ma web app doc.

VI SAO PHAI CHAY FILE NAY O NGOAI SANDBOX
    MinerU render PDF qua ``multiprocessing.Pipe`` (named pipe). Sandbox cua DSH
    chan named pipe nen moi lan parse deu chet voi:
        PermissionError: [WinError 5] Access is denied
    Day la gioi han cua sandbox, khong phai loi cai dat. Vi vay file nay duoc
    thiet ke de BAN tu chay (nhap doi vao RUN_MINERU_OCR.bat), khong phai de
    agent chay.

CACH DUNG
    Chay thu 1 bai:      python scripts\\run_mineru_local.py --only 2
    Chay 49 bai:         python scripts\\run_mineru_local.py --from 2
    Chi OCR, khong doi:  python scripts\\run_mineru_local.py --from 2 --skip-convert
    Doi lai tu MD san co:python scripts\\run_mineru_local.py --convert-only

    Hoac nhap doi vao RUN_MINERU_OCR.bat (tu nap moi truong MinerU).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANS_ROOT = os.path.join(ROOT, "extracted_data", "lesson_page_scans")
MD_ROOT = os.path.join(ROOT, "extracted_data", "mineru_md")
OUT_DIR = os.path.join(ROOT, "lessons_json")
PUBLIC_OUT = os.path.join(ROOT, "public", "lessons_json")
BOOK_MAP = os.path.join(ROOT, "book_structure_map.json")

# Thu tu 6 trang trong moi bai, dung theo ten file do extract_pdf_assets.py sinh ra.
PAGE_ORDER = [
    "words_to_learn",
    "words_in_context",
    "word_families",
    "listening_practice",
    "reading_part5_6",
    "reading_part7",
]

TOOL_ROOT = r"D:\CODE\vibecode\TOOL\mineru"
MINERU_KIT = os.path.join(TOOL_ROOT, ".venv", "Scripts", "mineru-kit.exe")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def say(msg):
    print(f"\n=== {msg} ===", flush=True)


def ok(msg):
    print(f"  [OK] {msg}", flush=True)


def bad(msg):
    print(f"  [LOI] {msg}", flush=True)


def lesson_dir(lid):
    return os.path.join(SCANS_ROOT, f"lesson_{lid:02d}")


def scan_pages(lid):
    """Tra ve danh sach (section, duong_dan_anh) theo thu tu dung."""
    d = lesson_dir(lid)
    if not os.path.isdir(d):
        return []
    found = {}
    for name in os.listdir(d):
        if not name.lower().endswith(".png"):
            continue
        # ten dang: 013_words_to_learn.png
        for section in PAGE_ORDER:
            if name.endswith(f"_{section}.png"):
                found[section] = os.path.join(d, name)
    return [(s, found[s]) for s in PAGE_ORDER if s in found]


def mineru_env():
    """Moi truong y het cac file .cmd cua ban cai MinerU, nhung TMP/TEMP tro vao
    workspace de khong ghi ra ngoai."""
    env = dict(os.environ)
    env["MINERU_HOME"] = os.path.join(TOOL_ROOT, "home")
    env["MINERU_MODEL_VLM_ENGINE"] = "llama-cpp"
    env["UV_CACHE_DIR"] = os.path.join(TOOL_ROOT, ".cache", "uv")
    env["UV_PYTHON_INSTALL_DIR"] = os.path.join(TOOL_ROOT, ".python")
    env["HF_HOME"] = os.path.join(TOOL_ROOT, ".cache", "huggingface")
    env["MODELSCOPE_CACHE"] = os.path.join(TOOL_ROOT, ".cache", "modelscope")
    env["VIRTUAL_ENV"] = os.path.join(TOOL_ROOT, ".venv")
    venv_scripts = os.path.join(TOOL_ROOT, ".venv", "Scripts")

    # TMP/TEMP: dung temp CUA CHINH MinerU (ban cai cua ban ghi duoc o day khi
    # chay ngoai sandbox). Neu tro vao workspace cung duoc, nhung de nguyen ban
    # cai tu quan ly thi sach hon.
    tmp = os.path.join(TOOL_ROOT, ".tmp")
    os.makedirs(tmp, exist_ok=True)
    env["TMP"] = tmp
    env["TEMP"] = tmp
    env["PATH"] = venv_scripts + os.pathsep + env.get("PATH", "")
    return env


def check_install():
    problems = []
    if not os.path.isfile(MINERU_KIT):
        problems.append(f"Không thấy mineru-kit: {MINERU_KIT}")
    if not os.path.isdir(os.path.join(TOOL_ROOT, "home", "models")):
        problems.append(f"Không thấy model: {TOOL_ROOT}\\home\\models")
    if not os.path.isdir(SCANS_ROOT):
        problems.append(f"Chưa có ảnh scan: {SCANS_ROOT}")
    return problems


def ocr_one(lid, force=False, tier="standard"):
    """OCR 6 trang cua 1 bai -> extracted_data/mineru_md/lesson_NN/*.md"""
    pages = scan_pages(lid)
    if not pages:
        bad(f"Lesson {lid:02d}: không thấy ảnh scan")
        return False

    out_dir = os.path.join(MD_ROOT, f"lesson_{lid:02d}")
    os.makedirs(out_dir, exist_ok=True)

    env = mineru_env()
    done = 0
    for section, img in pages:
        target = os.path.join(out_dir, f"{section}.md")
        if os.path.exists(target) and not force:
            done += 1
            continue

        r = subprocess.run(
            [MINERU_KIT, "parse", img, "-o", target, "--tier", tier],
            cwd=TOOL_ROOT, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
        )
        if r.returncode != 0 or not os.path.exists(target):
            bad(f"  {section}: OCR thất bại")
            tail = (r.stdout or "").strip().splitlines()[-4:]
            for line in tail:
                print(f"        {line[:150]}")
            return False

        # MinerU nhung anh vao Markdown dang base64 -> 30-55 KB/trang, hau het la
        # du lieu anh chu khong phai chu. Bo di: JSON nhe di ~10 lan, ma khong mat
        # chu nao (anh Part 1 da co san trong public/part1_photos/).
        strip_base64_in_file(target)

        text_len = text_length(target)
        note = "" if text_len > 50 else "  <- trang chi co anh, khong co chu"
        done += 1
        print(f"    {section}: OK ({text_len} ký tự chữ){note}", flush=True)

    ok(f"Lesson {lid:02d}: {done}/{len(pages)} trang -> {out_dir}")
    return True


def strip_base64_in_file(path):
    """Bo anh base64 nhung trong Markdown, ghi de lai."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            raw = f.read()
    except OSError:
        return
    if "base64," not in raw:
        return
    cleaned = re.sub(r"!\[[^\]]*\]\(data:image/[^)]*\)", "", raw)
    cleaned = re.sub(r"data:image/[a-zA-Z+]+;base64,[A-Za-z0-9+/=\s]+", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    with open(path, "w", encoding="utf-8") as f:
        f.write(cleaned)


def strip_lesson_base64(lid):
    """Boc base64 khoi TAT CA file Markdown cua mot bai."""
    n = 0
    for section in PAGE_ORDER:
        p = os.path.join(MD_ROOT, f"lesson_{lid:02d}", f"{section}.md")
        if os.path.isfile(p):
            before = os.path.getsize(p)
            strip_base64_in_file(p)
            if os.path.getsize(p) < before:
                n += 1
    return n


def text_length(path):
    """Do luong chu that (da bo anh base64)."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            t = f.read()
    except OSError:
        return 0
    t = re.sub(r"data:image/[a-zA-Z+]+;base64,[A-Za-z0-9+/=\s]+", "", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)
    return len(t.strip())


# --------------------------------------------------------------------------
# Markdown -> JSON schema cua app
# --------------------------------------------------------------------------

def read_md(lid, section):
    p = os.path.join(MD_ROOT, f"lesson_{lid:02d}", f"{section}.md")
    if not os.path.isfile(p):
        return ""
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def clean_md(text):
    """Bo markup Markdown/LaTeX thua de lay chuoi sach."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)      # anh
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)    # link
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = text.replace("\\_", "_")                          # \_\_\_\_ -> ____
    # MinerU boc `$` thanh `\$` (escape LaTeX) trong cac lua chon co so tien.
    # Da doi chieu voi anh scan (vd lesson_40 cau 5: sach in "$4 $9 $13 $30")
    # -> GIA TRI DUNG, chi du ky tu `\`. Bo di de hien dung nhu sach.
    text = text.replace("\\$", "$")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Cac tu loai trong sach: v., n., adj., adv.
POS_RE = r"(?:v|n|adj|adv|prep|conj|pron|phr)\.(?:\s*,\s*(?:v|n|adj|adv)\.)?"

# Tieu de phan Listening trong MinerU. Chap nhan moi do sau "#", dam/nghieng
# markdown ("**Part 3 Conversation**", "_Part 3 Talk_") va khoang trang le.
# Vi du khop: "## Part 3 Conversation", "**Part 4 Talk**", "Part 1 Photo",
# "### Part 2 Question–Response".
PART_HEADING_RE = re.compile(
    r"^[\s>]*[#]*[\s>]*[*_]{0,2}[\s*_]*(?:part|phan)\s+([1-4])\b[\s*_:.\-]*(.*?)[\s*_]*$",
    re.IGNORECASE,
)


def parse_words_to_learn(md):
    """Tach 12 muc tu vung tu trang Words to Learn.

    Dang thuc te (MinerU co the gop dong a./b. vao cung doan):
        1. abide by v., to comply with; to conform
        a. The two parties agreed to abide by the judge's decision.
        b. For years he has abided by a commitment...
    """
    out = []
    if not md:
        return out

    # Cat thanh tung muc theo so thu tu dau dong.
    # OCR doi khi thieu dau cham: "7 failure n., ..." thay vi "7. failure n., ..."
    parts = re.split(r"\n(?=\s*\d{1,2}[.)]?\s+[A-Za-z])", md)
    for chunk in parts:
        m = re.match(r"\s*(\d{1,2})[.)]?\s+([A-Za-z][^.,]*?)\s+" + POS_RE + r"\s*(.*)", chunk, re.S)
        if not m:
            continue
        idx, word, rest = int(m.group(1)), m.group(2).strip(), m.group(3)

        # Doan cuoi khoi = entry co the chua ca cau a./b. -> tach rieng.
        body = rest

        # Nghia: phan truoc vi du dau tien.
        ex_a = re.search(r"(?:^|\n)\s*a\.\s+(.+)", body)
        if ex_a:
            meaning = body[:ex_a.start()]
        else:
            inline = re.search(r"\s+a\.\s+", body)
            meaning = body[:inline.start()] if inline else body

        meaning = re.sub(r"\s+", " ", meaning).strip(" .;,")

        examples = []
        if ex_a:
            # Truong hop chuan: a. va b. moi cai mot dong.
            for pat in (r"(?:^|\n)\s*a\.\s+(.+?)(?=(?:\n\s*b\.)|$)",
                        r"(?:^|\n)\s*b\.\s+(.+)"):
                mm = re.search(pat, body, re.S)
                if mm:
                    # clean_md: bo markup + escape LaTeX (\$, \_ ...) giong cac
                    # truong khac, de cau vi du hien dung nhu sach.
                    sent = clean_md(mm.group(1))
                    if sent:
                        examples.append({"en": sent, "vi": ""})
        elif inline:
            # MinerU gop ca muc vao mot dong, khong con \n truoc a./b.
            rest2 = body[inline.end():]
            bm2 = re.search(r"\s+b\.\s+", rest2)
            if bm2:
                a_sent = re.sub(r"\s+", " ", rest2[:bm2.start()]).strip()
                b_sent = re.sub(r"\s+", " ", rest2[bm2.end():]).strip()
                for sent in (a_sent, b_sent):
                    if sent:
                        examples.append({"en": sent, "vi": ""})
            else:
                sent = re.sub(r"\s+", " ", rest2).strip()
                if sent:
                    examples.append({"en": sent, "vi": ""})

        out.append({
            "id": idx,
            "word": re.sub(r"\s+", " ", word).strip(),
            "pos": "v.",
            "ipa": "",
            "definition_en": meaning,
            "definition_vi": "",
            "examples": examples,
            "word_family": [],
            "needs_translation": True,
        })

    # Do tu loai that tu chinh chunk (POS_RE o tren chi de nhan dien).
    for entry, chunk in zip(out, [c for c in parts if re.match(r"\s*\d{1,2}[.)]?\s+[A-Za-z]", c)]):
        pm = re.search(POS_RE, chunk)
        if pm:
            entry["pos"] = re.sub(r"\s+", "", pm.group(0).split(",")[0])

    # OCR doi khi doc cung mot muc hai lan voi cach viet hoa khac nhau
    # (vd bai 33 co ca "individual" lan "Individual"). Gop lai, uu tien muc co
    # nhieu vi du hon.
    merged = {}
    order = []
    for e in out:
        key = e["word"].lower()
        if key in merged:
            keep = merged[key]
            if len(e["examples"]) > len(keep["examples"]):
                keep["examples"] = e["examples"]
            if len(e["definition_en"]) > len(keep["definition_en"]):
                keep["definition_en"] = e["definition_en"]
            continue
        merged[key] = e
        order.append(key)

    deduped = [merged[k] for k in order]
    for i, e in enumerate(deduped, 1):
        e["id"] = i
    return deduped


def word_stem(w):
    """Goc tu de so khop trong bang Word Families.

    vd: agreement -> agree, provision -> provid, assessable -> assess,
        seriously -> serious, running -> runn.
    """
    w = w.lower().split()[0].strip(".,;:()")
    for suf in ("ations", "ation", "ments", "ment", "ings", "ing",
                "able", "ible", "ally", "edly", "ance", "ence",
                "ity", "ies", "ive", "ous", "ate", "ed", "ly", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def stem_similarity(a, b):
    """Do giong nhau giua hai goc tu (0..1)."""
    if a == b:
        return 1.0
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    if n < 3:
        return 0.0
    return n / max(1, min(len(a), len(b)))


def split_group_by_stem(rows, threshold=0.7):
    """Chia mot nhom lon thanh cac nhom nho theo goc tu.

    Can thiet cho cac trang KHONG co dong trong giua cac nhom (vd bai 46):
    MinerU tra ve 18 dong lien nhau, khong co dau hieu ranh gioi nao khac.
    Goc tu la dau hieu duy nhat con lai: moi nhom xoay quanh mot goc
    (assess/assessment/assessable), nen khi gap tu khac goc thi mo nhom moi.
    """
    if len(rows) <= 3:
        return [rows]

    groups = []
    current = [rows[0]]
    base = word_stem(rows[0]["word"])
    for row in rows[1:]:
        st = word_stem(row["word"])
        if stem_similarity(base, st) >= threshold:
            current.append(row)
        else:
            groups.append(current)
            current = [row]
            base = st
    groups.append(current)
    return groups


def normalize_book_pos(raw):
    """Chuan hoa cot tu loai cua sach ve 'verb'/'noun'/'adjective'/'adverb'.

    Sach in bang Word Families co 3 cot: tu loai | tu | vi du. Cot tu loai
    thuong la "verb", "noun", "adj", "adv" (doi khi "n.", "v.", "adj.").
    MinerU co trang doc cot nay thanh rac ("√b", "a)", "r)", "\\", ".b") nen
    CHI nhan khi chuoi doc ra dung la mot tu loai; con lai tra "" — app se tu
    suy ra tu hinh thai va danh dau ro la suy luan, KHONG trinh bay nhu sach in.

    Tra "" (khong bia) khi khong nhan dang duoc.
    """
    s = str(raw or "").strip().strip(".").lower()
    if not s:
        return ""
    # Bo cac tien to rac hay gap truoc tu loai: "a) verb", "- verb", "1 verb".
    s = re.sub(r"^[^a-z]+", "", s)
    s = re.sub(r"[^a-z]+$", "", s)
    if not s:
        return ""
    if s in ("verb", "v", "vt", "vi"):
        return "verb"
    if s in ("noun", "n", "nc"):
        return "noun"
    if s in ("adj", "adjective", "a"):
        return "adjective"
    if s in ("adv", "adverb"):
        return "adverb"
    # Dang viet day du co the kem ghi chu: "verb (past)" -> lay tu dau.
    head = s.split()[0] if s.split() else s
    return {
        "verb": "verb", "noun": "noun",
        "adj": "adjective", "adjective": "adjective",
        "adv": "adverb", "adverb": "adverb",
    }.get(head, "")


def parse_word_families(md):
    """Bang Word Families. MinerU tra ve 2 dang khac nhau tuy trang:

    (a) HTML:  <table><tr><td>agree</td><td>If both parties...</td></tr>...
    (b) Markdown pipe: | attract | The store's poor location... |
                       | --- | --- |
                       | attraction | Having a clown... |

    Dong ngan cach giua cac nhom: <td colspan="2"></td> (dang a) hoac dong
    trong (dang b).
    """
    groups = []
    if not md:
        return groups

    # Trang co the TRON CA HAI dinh dang: phan dau la bang Markdown, phan giua la
    # <table> HTML (MinerU nhan dien khac nhau tuy vung trang). Nen phai chay ca
    # hai bo doc roi ghep lai THEO THU TU XUAT HIEN trong trang, khong duoc chon
    # mot cai roi bo qua cai kia.

    # --- dang (a): HTML table, 2 hoac 3 cot ---
    #   2 cot: <td>agree</td><td>vi du...</td>
    #   3 cot: <td>verb</td><td>avoid</td><td>vi du...</td>  (cot 1 la tu loai)
    #
    # COT 1 CUA BANG 3 COT LA TU LOAI THAT CUA SACH ("verb"/"noun"/"adj"/
    # "adv") — truoc day bi vut bo va moi dong ghi pos="", khien bang
    # Verb/Noun/Adj/Adv trong app trong hoan toan. Nhung cung co trang MinerU
    # doc cot 1 thanh rac ("√b", "a)", "r)", "\", ".b") nen chi nhan khi chuoi
    # doc ra DUNG la mot tu loai; con lai de "" (app se tu suy ra va danh dau).
    html_groups = []
    if "<tr>" in md:
        current = []
        for row in re.findall(r"<tr>(.*?)</tr>", md, re.S):
            cells = [clean_md(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
            if len(cells) == 1 and not cells[0]:
                if current:
                    html_groups.append(current)
                    current = []
                continue
            if len(cells) < 2:
                continue
            row_pos = ""
            if len(cells) >= 3:
                row_pos = normalize_book_pos(cells[0])
                word, example = cells[1], cells[2]
            else:
                word, example = cells[0], cells[1]
            if not word or not re.match(r"^[A-Za-z]", word):
                continue
            current.append({"word": word, "example": example, "pos": row_pos})
        if current:
            html_groups.append(current)

    # --- dang (b): Markdown pipe table, 2 hoac 3 cot ---
    # Vi tri dong ke (| --- | --- |) khac nhau tuy trang (dau nhom hoac cuoi
    # nhom), nen bo qua dong ke va tach nhom theo dong trong — dung nhu sach in.
    pipe_groups = []
    current = []
    for line in md.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if not s and current:
                pipe_groups.append(current)
                current = []
            continue
        cells = [clean_md(c) for c in s.strip("|").split("|")]
        if cells and all(not c or set(c) <= set("- ") for c in cells):
            # Dong ke -> bo qua (vi tri cua no khac nhau tuy trang).
            continue
        row_pos = ""
        if len(cells) >= 3:
            row_pos = normalize_book_pos(cells[0])
            word, example = cells[1], cells[2]
        elif len(cells) == 2:
            word, example = cells[0], cells[1]
        else:
            continue
        if not word or not re.match(r"^[A-Za-z]", word):
            continue
        current.append({"word": word, "example": example, "pos": row_pos})
    if current:
        pipe_groups.append(current)

    # Trang khong co dong trong giua cac nhom (vd bai 46) -> tat ca 18 dong
    # thanh MOT nhom. Tach lai theo goc tu.
    pipe_groups = [g for grp in pipe_groups for g in split_group_by_stem(grp)]
    html_groups = [g for grp in html_groups for g in split_group_by_stem(grp)]

    # Neu chi co mot dinh dang -> tra ve luon.
    if not html_groups:
        return pipe_groups
    if not pipe_groups:
        return html_groups

    # Ca hai -> ghep lai. `<table>` nam o dau hay cuoi trang quyet dinh thu tu.
    html_at = md.find("<table>")
    pipe_at = md.find("\n|")
    if pipe_at == -1:
        pipe_at = md.find("|")
    if html_at != -1 and html_at < pipe_at:
        return html_groups + pipe_groups
    return pipe_groups + html_groups


def parse_word_bank_from_text(md):
    """Bang word_bank khong co ke bang. MinerU tra ve vai kieu:

    (i) 1 cum 1 dong (pho bien nhat):
            accommodate
            get in touch          <- cum nhieu tu
            take part in
    (ii) nhieu tu 1 dong, ngan cach >=1 khoang trang:
            address develop offered strategy
    (iii) tron ca hai: 'access deleted failed search' roi 'allocate'

    Dong cau van thi co dau cau ket cau -> loai. Cum nhieu tu la mot muc, khong
    tach roi (vd 'get in touch' la 1 dap an, khong phai 3).
    """
    if not md:
        return []
    bank = []
    for line in md.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("|"):
            continue
        # Cau van co dau cau -> khong phai word_bank.
        if re.search(r"[.,;:!?()\"']", s):
            continue
        toks = s.split()
        if not (1 <= len(toks) <= 40):
            continue
        if not all(re.match(r"^[A-Za-z][A-Za-z'-]*$", t) for t in toks):
            continue
        bank.append(s)
    return bank


# Tu chuc nang: gan nhu khong bao gio dung mot minh lam dap an, va OCR hay doc
# sot chung ("look forward to" bi doc thanh "look forward"). Khi so khop cum thi
# BO QUA chung.
FUNCTION_WORDS = {
    "a", "an", "the", "as", "in", "on", "of", "to", "for", "at", "by", "with",
    "up", "out", "off", "over", "into", "from", "is", "are", "be", "and", "or",
    "been", "was", "were",
}


def phrase_score(window, target):
    """Do khop giua mot cum token va mot tu muc tieu (0..1).

    Bo qua tu chuc nang o CA HAI ben truoc khi so, vi OCR hay doc sot chung:
    sach in 'look forward to' nhung Markdown co the chi con 'look forward'.
    Nho vay van khop duoc ma khong bi lech.
    """
    wt = [t for t in window.split() if t.lower() not in FUNCTION_WORDS]
    tt = [t for t in target.split() if t.lower() not in FUNCTION_WORDS]
    if not tt or not wt:
        return 0.0
    if len(wt) != len(tt):
        return 0.0
    hits = 0
    for a, b in zip(wt, tt):
        if a.lower() == b.lower() or stem_similarity(word_stem(a), word_stem(b)) >= 0.7:
            hits += 1
    return hits / len(tt)


def align_bank_to_targets(tokens, targets):
    """Cat chuoi token thanh cac muc, dung danh sach tu muc tieu lam chuan.

    Trong sach, word bank CHINH LA cac tu cua bai (co the o dang chia khac:
    'physically' trong bai, 'physical' trong bank). Nhung OCR co the:
      - doc sot tu chuc nang: 'look forward to' -> 'look forward'
      - gop sai: 'coming up with' -> 'coming' + 'up with'
      - them/bot khoang trang

    Nen khong the cat tham lam theo tung vi tri. Thay vao do: quy hoach dong —
    tim cach cat toan bo chuoi thanh DUNG so muc, sao cho moi muc khop mot tu
    muc tieu nao do, va tong diem khop cao nhat.
    """
    if not targets:
        return None

    n = len(tokens)
    want = len(targets)
    NEG = float("-inf")
    # best[k][i] = diem tot nhat khi da cat i token thanh k muc.
    best = [[NEG] * (n + 1) for _ in range(want + 1)]
    prev = [[None] * (n + 1) for _ in range(want + 1)]
    best[0][0] = 0.0

    max_len = max((len(t.split()) for t in targets), default=1)

    for k in range(1, want + 1):
        for i in range(1, n + 1):
            # Muc thu k ket thuc tai token i, bat dau tai j.
            for length in range(1, min(max_len + 1, i) + 1):
                j = i - length
                if best[k - 1][j] == NEG:
                    continue
                window = " ".join(tokens[j:i])
                local = 0.0
                for t in targets:
                    sc = phrase_score(window, t)
                    if sc <= 0.0:
                        continue
                    # Thien vi cua so co dung so token nhu tu muc tieu: neu
                    # khong, moi cach cat deu dat diem toi da va ranh gioi se
                    # tuy y ('reduce' bi cat thanh 'reduce as').
                    bonus = 0.05 if length == len(t.split()) else 0.0
                    local = max(local, sc + bonus)
                if local < 0.6:
                    continue
                total = best[k - 1][j] + local
                if total > best[k][i]:
                    best[k][i] = total
                    prev[k][i] = j

    if best[want][n] == NEG:
        return None

    # Truy vet.
    cuts = []
    i = n
    for k in range(want, 0, -1):
        j = prev[k][i]
        cuts.append(" ".join(tokens[j:i]))
        i = j
    cuts.reverse()
    return cuts


def normalize_word_bank(bank, expected=12, targets=None):
    """Dua word_bank ve dung 12 muc.

    Tra ve (danh_sach, chac_chan). `chac_chan=False` nghia la phai cat/gop cum
    ma khong khop tu muc tieu nao — nguoi doc nen kiem tra lai trang do.

    `targets` la danh sach 12 tu cua bai (neu biet): sach in word bank chinh la
    cac tu nay o dang chia khac, nen dung lam moc cat cum thi chinh xac hon.
    """
    if not bank:
        return [], True

    # Du roi -> giu nguyen.
    if len(bank) == expected:
        return bank, True

    # Neu biet 12 tu muc tieu thi luon dung chung lam moc: sach in word bank
    # chinh la cac tu nay, chi khac cach chia. Cach nay dung cho MOI kieu trinh
    # bay (1 dong, nhieu dong, hay tron), va cat dung ranh gioi cum.
    if targets:
        flat = " ".join(bank).split()
        aligned = align_bank_to_targets(flat, targets)
        if aligned is not None:
            return aligned, len(aligned) == expected

    # It hon `expected`: dong nao gop nhieu muc thi tach, dong nao la 1 cum
    # nhieu tu thi GIU NGUYEN (vd 'figure out', 'shut down' la 1 dap an).
    if len(bank) < expected and len(bank) == 1:
        # Ca word_bank don tren MOT dong -> phai cat lai thanh tung cum.
        toks = bank[0].split()
        if len(toks) > expected:
            # Uu tien dung danh sach tu muc tieu lam moc cat (chinh xac nhat).
            aligned = align_bank_to_targets(toks, targets)
            if aligned and len(aligned) == expected:
                return aligned, True
            if aligned:
                return aligned, len(aligned) == expected
            return toks, False
        return toks, True

    if len(bank) < expected:
        out = []
        for entry in bank:
            parts = entry.split()
            if len(parts) >= 3:
                # 'access deleted failed search' -> 4 muc rieng
                out.extend(parts)
            else:
                # 'figure out' / 'allocate' -> 1 muc
                out.append(entry)
        return out, True

    # Nhieu hon `expected`: co muc bi tach roi ('coming' + 'up' + 'with').
    # Dung danh sach tu muc tieu lam moc gop lai.
    if targets:
        flat = " ".join(bank).split()
        aligned = align_bank_to_targets(flat, targets)
        if aligned and len(aligned) == expected:
            return aligned, True
        if aligned and len(aligned) < len(bank):
            bank, aligned_used = aligned, True
        else:
            aligned_used = False
    else:
        aligned_used = False

    # Khong co targets (hoac gop khong dung) -> cach cu: tach dong nhieu tu roi
    # gop dan cac muc 1 tu lien nhau.
    split = []
    for entry in bank:
        parts = entry.split()
        if len(parts) > 1:
            split.extend(parts)
        else:
            split.append(entry)

    if len(split) == expected:
        return split, aligned_used

    out = list(split)
    i = 0
    while len(out) > expected and i < len(out) - 1:
        a, b = out[i], out[i + 1]
        if " " not in a and " " not in b:
            out[i:i + 2] = [f"{a} {b}"]
        else:
            i += 1
    return out, len(out) == expected


def parse_words_in_context(md, targets=None):
    """Trang Words in Context: bang word_bank (co the co ke hoac khong) +
    doan van co cho trong danh so.

    `targets`: danh sach 12 tu cua bai. Sach in word bank chinh la cac tu nay
    (dang chia khac), nen dung lam moc khi phai cat/gop cum.

    Tra ve them `bank_certain`: False khi phai gop cum ma khong khop tu muc tieu
    nao, tuc `word_bank` co the sai ranh gioi cum. Canh bao nay di vao JSON de
    nguoi doc biet trang nao can xem lai, thay vi am tham sai.
    """
    if not md:
        return {"passage": "", "word_bank": [], "blanks": [],
                "questions": [], "bank_certain": True}

    bank = []
    passage_lines = []
    in_table = False

    for line in md.splitlines():
        s = line.strip()
        if s.startswith("|"):
            in_table = True
            for c in [c.strip() for c in s.strip("|").split("|")]:
                if c and not set(c) <= set("- "):
                    bank.append(c)
            continue
        if in_table and not s:
            in_table = False
            continue
        if s.startswith("#"):
            continue
        if s:
            passage_lines.append(s)

    # Khong co bang ke -> doc word_bank tu cac dong ngan.
    #
    # Word_bank nam ngay TRUOC cau van dau tien, nhung truoc no con co tieu de
    # va cau huong dan ("Read the following passage..."). Nen khong the break
    # ngay o dong khong phai word_bank dau tien: phai tim dong word_bank dau
    # tien roi moi thu, va dung khi gap cau van that.
    bank_certain = True
    if not bank:
        seen_bank = False
        head = []
        for line in passage_lines:
            cand = parse_word_bank_from_text(line)
            if cand:
                seen_bank = True
                head.extend(cand)
            elif seen_bank:
                break          # da het khu vuc word_bank
        bank, bank_certain = normalize_word_bank(head, targets=targets)

    # Bo cac dong word_bank ra khoi passage.
    body_lines = [ln for ln in passage_lines if not parse_word_bank_from_text(ln)]
    passage = clean_md(" ".join(body_lines))

    blanks = [int(n) for n in re.findall(r"\((\d{1,2})\)", passage)]

    # Kiem tra cheo: so muc word_bank phai bang so cho trong.
    if bank and blanks and len(bank) != len(blanks):
        bank_certain = False

    return {"passage": passage, "word_bank": bank, "blanks": blanks,
            "questions": [], "bank_certain": bank_certain}


def parse_part5(md):
    """Part 5: cau hoi + 4 lua chon (A)-(D), co the xep 2 cot."""
    out = []
    if not md:
        return out

    # "10. The two sides ... ____ at midnight ..."
    blocks = re.split(r"\n(?=\s*\d{1,3}\.\s+\S)", md)
    for b in blocks:
        m = re.match(r"\s*(\d{1,3})\.\s+(.+)", b, re.S)
        if not m:
            continue
        num, body = int(m.group(1)), m.group(2)

        # Part 5 cua sach la cau 10-15. Cau 16-18 thuoc Part 6 (doan van co
        # marker), duoc parse_part6 xu ly rieng.
        if not (10 <= num <= 15):
            continue

        opts = {}
        # Gom cac lua chon: "(A) agreement (C) agree" / "(B) agreeable (D) agreed"
        for om in re.finditer(r"\(([A-D])\)\s*([^()\n]+?)(?=\s*\([A-D]\)|\s*$|\n)", body):
            letter, text = om.group(1), om.group(2).strip()
            if text and letter not in opts:
                opts[letter] = text
        if not opts:
            continue

        # Cau hoi = phan truoc lua chon dau tien.
        first = re.search(r"\([A-D]\)", body)
        stem = re.sub(r"\s+", " ", body[:first.start()]).strip() if first else ""
        if not stem:
            continue
        stem = clean_md(stem)

        out.append({
            "number": num,
            "question": stem,
            "options": [{"label": k, "text": clean_md(opts[k])} for k in "ABCD" if k in opts],
        })
    return out


def parse_part6(md):
    """Part 6: doan van "Text Completion" co cho trong [16][17][18] + 3 cau hoi.

    Markdown goc (sach in xep options 2 COT tren cung mot dong):
        Part 6 Text Completion
        Choose the word or phrase that best completes the sentence.
        ## Rental Property for Everyone      <- tieu de con cua doan van
        ... A lease is an \\_16\\_ between a landlord and a tenant. ...
        16. (A) agree 18. (A) assure         <- 2 cot: cot 1 = cau 16, cot 2 = cau 18
        (B) agreed (B) will assure
        (C) agreeable (C) are assuring
        (D) agreement (D) are assured
        17. (A) provision                    <- cau le, 1 cot
        (B) provisions

    Truoc day phan nay bi bo qua hoan toan (parser chi lay Part 5), nen UI
    khong co doan van dien tu cua Part 6.
    """
    if not md:
        return None
    i = md.find("Part 6")
    if i == -1:
        return None
    seg = md[i:]

    passage_lines = []
    opt_lines = []
    for ln in seg.splitlines():
        s = ln.strip()
        if not s:
            continue
        if re.match(r"^Part\s+6\b", s, re.I):
            continue
        if s.lower().startswith("choose the word"):
            continue
        # Tieu de con cua doan van ("## Leases") giu lai lam dong tieu de.
        s = re.sub(r"^#+\s*", "", s)
        if re.match(r"^\d{1,2}\.\s", s) or re.match(r"^\([A-D]\)", s):
            opt_lines.append(s)
        else:
            passage_lines.append(s)

    if not opt_lines:
        return None

    # ---- cau hoi: ho tro 3 kieu layout cua sach/OCR ----
    #   (a) 2 cot nhieu dong:  "16. (A) agree 18. (A) assure" / "(B) agreed (B) will assure"
    #   (b) 1 dong duy nhat:   "16. (A) attract (B) attractive (C) ... (D) ..."
    #   (c) cot tron lan:      OCR doc lan cot 1 va cot 2 (bai 33)
    # Chia block option thanh cac NHOM theo dong co so cau hoi; moi nhom gom
    # options tren dong marker + cac dong ke tiep (khong co so).
    groups = []
    for ln in opt_lines:
        nums = [int(n) for n in re.findall(r"(?:^|\s)(\d{1,2})\.(?=\s)", ln)]
        opts = re.findall(
            r"\(([A-D])\)\s*([^()]+?)(?=\s*\([A-D]\)|\s*\d{1,2}\.\s*|$)", ln
        )
        if nums:
            groups.append({"nums": nums, "marker_opts": opts, "cont_opts": []})
        elif groups:
            groups[-1]["cont_opts"].extend(opts)

    def assign_group_local():
        qmap = {}

        def add(num, letter, text):
            e = qmap.setdefault(num, [])
            if all(o["label"] != letter for o in e):
                e.append({"label": letter, "text": clean_md(text)})

        for g in groups:
            nums = g["nums"]
            if len(nums) == 1:
                for letter, text in g["marker_opts"] + g["cont_opts"]:
                    add(nums[0], letter, text)
                continue
            # nhieu cot: options phan bo theo vi tri, cycle qua cac cot
            for k, (letter, text) in enumerate(g["marker_opts"] + g["cont_opts"]):
                add(nums[k % len(nums)], letter, text)
        return qmap

    def assign_global_rank():
        """Truong hop cot bi tron lan: lan thu k cua chu (A)..(D) thuoc cot thu k
        (cot = so cau hoi theo thu tu marker xuat hien)."""
        seen_nums = []
        for g in groups:
            for n in g["nums"]:
                if n not in seen_nums:
                    seen_nums.append(n)
        counts = {}
        qmap = {}
        for g in groups:
            for letter, text in g["marker_opts"] + g["cont_opts"]:
                k = counts.get(letter, 0)
                counts[letter] = k + 1
                if seen_nums:
                    num = seen_nums[k % len(seen_nums)]
                    qmap.setdefault(num, []).append(
                        {"label": letter, "text": clean_md(text)}
                    )
        return qmap

    # Phat hien cot tron lan: trong mot nhom, chu cai cua options phai tien
    # theo thu tu A->B->C->D cho moi cot. Neu chu dau tien cua phan ke tiep
    # "lui lai" so voi ky vong thi block bi tron -> dung global-rank.
    mixed = False
    for g in groups:
        if len(g["nums"]) != 1 or not g["cont_opts"]:
            continue
        last_marker_letters = [o[0] for o in g["marker_opts"]]
        expected = "B"
        if last_marker_letters:
            top = max(last_marker_letters)
            expected = chr(ord(top) + 1) if top != "D" else None
        if expected and g["cont_opts"][0][0] != expected:
            mixed = True
            break

    qmap = assign_global_rank() if mixed else assign_group_local()

    questions = []
    for num in sorted(qmap):
        rows = qmap[num]
        # Bo lap nhan trung (giu lan dau), roi neu du 4 lua chon nhung nhan bi
        # sai (A,B,C,B) thi gan lai theo thu tu — sach luon in A-D dung thu tu.
        seen = []
        for o in rows:
            if all(o["label"] != s["label"] for s in seen):
                seen.append(o)
        if len(rows) == 4 and len(seen) < 4:
            # 4 muc nhung nhan bi OCR doc trung (A,B,C,B) -> gan lai theo thu tu
            seen = [dict(o, label="ABCD"[i]) for i, o in enumerate(rows)]
        elif len(seen) == 4 and [o["label"] for o in seen] != list("ABCD"):
            for i, o in enumerate(seen):
                o["label"] = "ABCD"[i]
        if len(seen) >= 3:
            questions.append(
                {"number": num, "question": "", "options": seen}
            )
    if not questions:
        return None

    # ---- passage: doi marker _16_ / [16] ve dung mot dang [16] ----
    passage = clean_md("\n".join(passage_lines))
    passage = re.sub(
        r"(?<![A-Za-z0-9])[_\[]+(\d{1,2})[_\]]+(?![A-Za-z0-9])", r"[\1]", passage
    )
    return {"passage": passage, "questions": questions}


def parse_part7(md):
    """Part 7: mot hoac nhieu doan van/doc hieu + cau hoi trac nghiem.

    Truoc day ham nay bo het cau hoi (luon tra `questions: []`), lam mat toan bo
    phan doc hieu Part 7 — du Markdown co day du:
        19. What is the purpose of the letter?
        (A) To find out why Mr. Harrison no longer wants this service.
        (B) ...
    """
    if not md:
        return []

    lines = md.splitlines()
    questions = []
    cur = None
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        mq = re.match(r"^(\d{1,2})\.\s+(.*)$", s)
        if mq and not s.startswith("("):
            if cur:
                questions.append(cur)
            cur = {"number": int(mq.group(1)), "question": clean_md(mq.group(2)),
                   "options": []}
            continue
        mo = re.match(r"^\(([A-D])\)\s*(.*)$", s)
        if mo and cur is not None:
            cur["options"].append({"label": mo.group(1), "text": clean_md(mo.group(2))})
            continue

    if cur:
        questions.append(cur)
    # Chi giu cau hoi co du lua chon.
    questions = [q for q in questions if q["options"]]

    # Doan van = phan con lai sau khi bo cac dong cau hoi/lua chon.
    q_nums = {q["number"] for q in questions}
    body_lines = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("#"):
            continue
        mq = re.match(r"^(\d{1,2})\.\s+", s)
        if mq and int(mq.group(1)) in q_nums:
            continue
        if re.match(r"^\([A-D]\)", s):
            continue
        body_lines.append(ln)
    text = clean_md("\n".join(body_lines))

    if not text and not questions:
        return []

    # Giu tuong thich nguoc: `text` van la truong chinh, them `questions`.
    return [{"type": "reading", "text": text, "questions": questions}]


def parse_listening(md):
    """Part 1/2/3/4 cua phan Listening Comprehension.

    Nhieu trang chi co anh Part 1 -> khong co chu nao -> tra ve rong, KHONG bia.

    Phan 3 (Conversation) va Phan 4 (Talk) thi CO cau hoi va lua chon trong sach:
        4. What problem do the speakers have with the computer company?
        (A) It won't renew the contract.
        (B) ...
    Returns:
        {"questions": [...], "instructions": "...", "parts": [...],
         "part3": [...], "part4": [...]}

    `part3`/`part4` la nhom cau hoi THAT SU nam duoi tieu de "Part 3"/"Part 4"
    trong Markdown — KHONG suy ra tu khoang so cau hoi (4..6, 7..9). Nho vay
    cau hoi duoc xep dung phan cua sach ke ca khi MinerU in sai thu tu
    (vd lesson_01: Part 3 in ra 4,6,5). Giu nguyen thu tu xuat hien, khong
    sap xep lai va khong danh so lai.

    CHU Y: `instructions` la phan chu HUONG DAN in tren trang luyen nghe, KHONG
    phai tapescript cua sach. Tapescript that nam o phan rieng cuoi sach (trang
    341-373 ban in) va chua duoc scan — nen tuyet doi khong gan no vao truong
    `tapescript`, lam nguoi hoc tuong da co loi thoai.
    """
    if not md:
        return {"questions": [], "tapescript": "", "parts": [], "part3": [], "part4": []}

    lines = md.splitlines()

    # Ghi nhan cac phan co trong trang (Part 1..4) de UI biet bai co gi.
    parts = []
    for ln in lines:
        m = PART_HEADING_RE.match(ln)
        if m:
            parts.append({"part": int(m.group(1)), "title": m.group(2).strip()})

    # Gom cau hoi: bat dau o dong "N. cau hoi", roi hut cac dong "(A) ...".
    # `q_part` giu phan cua TUNG cau hoi (0 = cau hoi nam truoc moi tieu de
    # Part, trang loi -> chi vao `questions`, KHONG gan bua vao Part 3/4).
    #
    # CHI DOC `part` NGAY LUC MO CAU HOI, khong doc luc ket thuc: tieu de Part 4
    # co the xen giua cau hoi va lua chon cuoi cua no, va cau hoi cuoi Part 3
    # (vd lesson_01 cau 5) nam TRUOC tieu de Part 4 trong khi lua chon cua no
    # van duoc hut sau do.
    questions, q_part = [], []
    cur = None
    cur_part = 0
    part = 0                      # phan hien hanh theo tieu de gan nhat
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        # Tieu de phan: bat ca "## Part 3 Conversation" lan "Part 3 Conversation".
        m = PART_HEADING_RE.match(s)
        if m:
            part = int(m.group(1))
            continue
        if s.startswith("#"):
            continue

        mq = re.match(r"^(\d{1,2})\.\s+(.*)$", s)
        if mq and not s.startswith("("):
            if cur:
                questions.append(cur)
                q_part.append(cur_part)
            cur = {"number": int(mq.group(1)), "question": clean_md(mq.group(2)),
                   "options": []}
            cur_part = part
            continue

        mo = re.match(r"^\(([A-D])\)\s*(.*)$", s)
        if mo and cur is not None:
            cur["options"].append({"label": mo.group(1), "text": clean_md(mo.group(2))})
            continue

    if cur:
        questions.append(cur)
        q_part.append(cur_part)

    # Chi giu cau hoi that su co lua chon (Phan 1/2 khong co) — pair cung
    # phan cua no de chi so khong lech nhau.
    kept = [(q, p) for q, p in zip(questions, q_part) if q["options"]]
    questions = [q for q, _ in kept]
    part3 = [q for q, p in kept if p == 3]
    part4 = [q for q, p in kept if p == 4]

    body = clean_md(re.sub(r"^#+.*$", "", md, flags=re.M))
    return {"questions": questions, "instructions": body, "tapescript": "",
            "parts": parts, "part3": part3, "part4": part4}


def build_lesson(lid, book_map):
    """Ghep 6 phan Markdown thanh JSON. Phan nao thieu thi de trong, KHONG bia."""
    words_md = read_md(lid, "words_to_learn")
    ctx_md = read_md(lid, "words_in_context")
    fam_md = read_md(lid, "word_families")
    lis_md = read_md(lid, "listening_practice")
    p56_md = read_md(lid, "reading_part5_6")
    p7_md = read_md(lid, "reading_part7")

    info = None
    for lesson in book_map.get("lessons", []):
        if lesson.get("lesson_id") == lid or lesson.get("id") == lid:
            info = lesson
            break
    info = info or {}

    words = parse_words_to_learn(words_md)
    families = parse_word_families(fam_md)
    # Word bank cua sach chinh la 12 tu muc tieu -> dung lam moc cat cum.
    ctx = parse_words_in_context(ctx_md, targets=[w["word"] for w in words])

    # Gan bang word-family cho tung tu.
    #
    # Trong sach, tu goc cua nhom (vd "agree") thuong KHONG nam trong 12 tu cua
    # bai (bai co "agreement"). Nen khong the so khop chinh xac: phai so khop
    # theo goc tu chung. vd: agreement <-> agree, provision <-> provide.
    #
    # Moi nhom chi duoc gan cho MOT tu (tu khop nhat), neu khong mot tu ngan nhu
    # "opt" co the hut nham nhieu nhom.
    used = set()
    for w in words:
        wstem = word_stem(w["word"])
        best, best_score, best_idx = None, 0.0, -1
        for idx, grp in enumerate(families):
            if not grp or idx in used:
                continue
            for g in grp:
                score = stem_similarity(wstem, word_stem(g["word"]))
                if score >= 0.7 and score > best_score:
                    best, best_score, best_idx = grp, score, idx
        if best is not None:
            used.add(best_idx)
            # Giu nguyen `pos` doc duoc tu cot tu loai cua sach (neu co).
            # Rong nghia la OCR khong doc duoc -> app tu suy ra + danh dau.
            w["word_family"] = [
                {"pos": g.get("pos", ""), "word": g["word"], "example": g["example"]}
                for g in best
            ]

    listening = parse_listening(lis_md)

    return {
        "lesson_id": lid,
        "title": info.get("title", f"Lesson {lid}"),
        "theme_name": info.get("theme_name", ""),
        "audio_track": info.get("audio_track", f"track_{lid:02d}.mp3"),
        "part1_photo": info.get("part1_photo", f"lesson_{lid:02d}.jpg"),
        "words_to_learn": words,
        "words_in_context": {
            "passage": ctx["passage"],
            "word_bank": ctx["word_bank"],
            "blanks": ctx["blanks"],
            "questions": ctx["questions"],
            "bank_certain": ctx.get("bank_certain", True),
        },
        "word_families": families,
        "practice": {
            "part5": parse_part5(p56_md),
            "part6": parse_part6(p56_md) or [],
            "part7": parse_part7(p7_md),
        },
        "listening": listening,
        # Tapescript that cua sach nam o phan rieng cuoi sach (trang 341-373),
        # CHUA duoc scan -> de trong mot cach trung thuc. Tuyet doi khong gan
        # phan chu huong dan tren trang luyen nghe vao day.
        "tapescript": "",
        # Giu Markdown tho de doi chieu khi can.
        #
        # `\$` la escape LaTeX do MinerU sinh ra khi gap so tien (sach in `$4`,
        # MinerU tra `\$4`). Day KHONG phai noi dung sach, chi la artifact OCR,
        # nen bo ngay tai day de moi truong (ke ca _raw) deu sach nhu sach in.
        "_raw": {
            "words_to_learn": words_md.replace("\\$", "$"),
            "words_in_context": ctx_md.replace("\\$", "$"),
            "word_families": fam_md.replace("\\$", "$"),
            "listening_practice": lis_md.replace("\\$", "$"),
            "reading_part5_6": p56_md.replace("\\$", "$"),
            "reading_part7": p7_md.replace("\\$", "$"),
        },
        "needs_review": True,
    }


def has_markdown(lid):
    """Bai nay da co Markdown that chua (it nhat trang words_to_learn)?"""
    d = os.path.join(MD_ROOT, f"lesson_{lid:02d}")
    if not os.path.isdir(d):
        return False
    for name in os.listdir(d):
        if name.endswith(".md") and os.path.getsize(os.path.join(d, name)) > 0:
            return True
    return False


def convert(lid, book_map):
    """Sinh JSON tu Markdown.

    TU CHOI chay neu chua co Markdown: neu khong se ghi ra JSON rong de len bai
    tot (da tung xay ra voi lesson_01). Tra ve None khi bi tu choi.
    """
    if not has_markdown(lid):
        return None

    # Boc base64 TRUOC khi doc: MinerU nhung anh vao Markdown (30-55 KB/trang),
    # lam JSON phinh len 100+ KB ma khong them thong tin chu nao. Phai lam o day
    # de moi duong vao (convert-only, convert_available_lessons) deu sach.
    strip_lesson_base64(lid)

    data = build_lesson(lid, book_map)

    # Chan ghi de bai da co du lieu that bang mot vo rong.
    dest = os.path.join(OUT_DIR, f"lesson_{lid:02d}.json")
    if os.path.isfile(dest) and not data["_raw"].get("words_to_learn"):
        return None

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return dest


# --------------------------------------------------------------------------

def parse_ids(text):
    out = []
    for part in str(text).split(","):
        part = part.strip()
        if part.isdigit():
            out.append(int(part))
    return out


def main():
    ap = argparse.ArgumentParser(description="MinerU -> JSON cho web app TOEIC 600")
    ap.add_argument("--only", help="chi vai bai, vd: 2,3,4")
    ap.add_argument("--from", dest="from_id", type=int, help="bat dau tu bai nay")
    ap.add_argument("--to", dest="to_id", type=int, help="ket thuc o bai nay")
    ap.add_argument("--force", action="store_true", help="OCR lai du da co .md")
    ap.add_argument("--tier", default="standard", help="flash|basic|standard|advanced")
    ap.add_argument("--skip-convert", action="store_true", help="chi OCR, khong tao JSON")
    ap.add_argument("--convert-only", action="store_true", help="chi doi .md san co -> JSON")
    args = ap.parse_args()

    problems = check_install()
    if problems:
        say("Thiếu thành phần")
        for p in problems:
            bad(p)
        return 1

    if args.only:
        ids = parse_ids(args.only)
    else:
        lo = args.from_id or 1
        hi = args.to_id or 50
        ids = list(range(lo, hi + 1))

    with open(BOOK_MAP, encoding="utf-8") as f:
        book_map = json.load(f)

    say(f"MinerU OCR — {len(ids)} bài (tier {args.tier})")
    print(f"  tool   : {TOOL_ROOT}")
    print(f"  output : {MD_ROOT}")

    t0 = time.time()
    ok_count = 0
    failed = []
    skipped = []

    for i, lid in enumerate(ids, 1):
        print(f"\n[{i}/{len(ids)}] Lesson {lid:02d}", flush=True)
        if not args.convert_only:
            if not ocr_one(lid, force=args.force, tier=args.tier):
                failed.append(lid)
                continue
        if not args.skip_convert:
            try:
                path = convert(lid, book_map)
            except Exception as exc:  # noqa: BLE001
                bad(f"đổi JSON lỗi: {exc}")
                failed.append(lid)
                continue
            if path is None:
                bad("chưa có Markdown cho bài này — bỏ qua (không ghi đè)")
                skipped.append(lid)
                continue
            ok(f"JSON: {os.path.relpath(path, ROOT)}")
        ok_count += 1

    # Copy sang public/ de web app doc duoc.
    if not args.skip_convert and ok_count:
        say("Publish sang public/lessons_json")
        os.makedirs(PUBLIC_OUT, exist_ok=True)
        n = 0
        for lid in ids:
            src = os.path.join(OUT_DIR, f"lesson_{lid:02d}.json")
            if os.path.isfile(src):
                import shutil
                shutil.copy2(src, os.path.join(PUBLIC_OUT, f"lesson_{lid:02d}.json"))
                n += 1
        ok(f"đã copy {n} tệp")

    say("Kết thúc")
    print(f"  thành công : {ok_count}/{len(ids)}")
    if skipped:
        print(f"  bỏ qua     : {skipped}  (chưa có Markdown)")
    if failed:
        print(f"  thất bại   : {failed}")
    print(f"  thời gian  : {time.time()-t0:.0f}s")
    if ok_count:
        print("\nMở web app và bấm 'Quét lại' ở sidebar.")
    elif skipped and not failed:
        print("\nChưa OCR được bài nào. Chạy không có --convert-only để OCR trước.")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
