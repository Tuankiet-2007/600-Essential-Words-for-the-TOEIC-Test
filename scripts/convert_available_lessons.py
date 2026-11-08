"""Sinh JSON cho cac bai da co Markdown (dung de kiem tra giua chung).

Sau khi sinh, in bang kiem tra chat luong. Muc dich quan trong nhat: phat hien
cac bai bi MinerU BO SOT du lieu ma khong bao loi. Vi du da gap o bai 8: MinerU
bo nguyen nhom word-family 'expose/exposure/exposed' (3 dong) — JSON van hop le,
khong co exception, chi co so dong hut di. Chi khi doi chieu voi so mong doi
(12 tu, 24 vi du, 18 dong word-family, 12 word bank) moi thay.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import run_mineru_local as r  # noqa: E402
import patch_missing as pm  # noqa: E402

# So mong doi theo cau truc sach: 12 tu, 2 vi du/tu, 3 dong word-family/tu.
WANT_WORDS = 12
WANT_EXAMPLES = 24
WANT_FAMILY = 18
WANT_BANK = 12

with open(r.BOOK_MAP, encoding="utf-8") as f:
    book_map = json.load(f)

md_root = r.MD_ROOT
ids = []
if os.path.isdir(md_root):
    for name in sorted(os.listdir(md_root)):
        if name.startswith("lesson_"):
            try:
                ids.append(int(name.split("_")[1]))
            except (IndexError, ValueError):
                pass

print(f"Tim thay {len(ids)} bai co Markdown: {ids}")
done = []
for lid in ids:
    p = r.convert(lid, book_map)
    if p is None:
        print(f"  L{lid:02d}: bo qua (chua du du lieu)")
        continue

    # Vá ngay sau khi sinh: convert() luôn ghi lại từ Markdown nên các dòng
    # MinerU bỏ sót sẽ mất nếu không vá ở đây mỗi lần.
    with open(p, encoding="utf-8") as f:
        lesson = json.load(f)
    n_added, msgs = pm.apply_all_patches(lesson, lid)
    if n_added:
        lesson.setdefault("_meta", {})["patched"] = True
        lesson["_meta"]["patch_note"] = (
            "Mot so dong duoc doc lai tu anh scan vi MinerU bo sot"
        )
        with open(p, "w", encoding="utf-8") as f:
            json.dump(lesson, f, ensure_ascii=False, indent=2)
        for m in msgs:
            print(f"      [va] {m}")

    print(f"  L{lid:02d}: {os.path.getsize(p):6} bytes  {os.path.relpath(p, r.ROOT)}")
    done.append(lid)

# copy sang public/
if done:
    import shutil
    os.makedirs(r.PUBLIC_OUT, exist_ok=True)
    for lid in done:
        src = os.path.join(r.OUT_DIR, f"lesson_{lid:02d}.json")
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(r.PUBLIC_OUT, f"lesson_{lid:02d}.json"))
    print(f"\nDa publish {len(done)} bai sang public/lessons_json/")

# ---------------------------------------------------------------- kiem tra
if not done:
    sys.exit(0)


def audit(lid):
    """Tra ve (danh_sach_canh_bao) cho mot bai."""
    path = os.path.join(r.OUT_DIR, f"lesson_{lid:02d}.json")
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    warn = []
    nw = len(d.get("words_to_learn") or [])
    ex = sum(len(w.get("examples") or []) for w in d.get("words_to_learn") or [])
    fam = sum(len(w.get("word_family") or []) for w in d.get("words_to_learn") or [])
    ctx = d.get("words_in_context") or {}
    nb = len(ctx.get("word_bank") or [])
    nbl = len(ctx.get("blanks") or [])
    p5 = len(((d.get("practice") or {}).get("part5")) or [])

    if nw != WANT_WORDS:
        warn.append(f"{nw} tu (mong doi {WANT_WORDS})")
    if ex < WANT_EXAMPLES:
        warn.append(f"{ex} vi du (mong doi {WANT_EXAMPLES})")
    # 18 dong word-family la chuan; it hon nghia la MinerU bo sot ca mot nhom.
    if fam < WANT_FAMILY:
        warn.append(f"{fam} dong word-family (mong doi {WANT_FAMILY}) — co the bi bo sot")
    if nb != WANT_BANK:
        warn.append(f"{nb} word_bank (mong doi {WANT_BANK})")
    if nbl != WANT_WORDS:
        warn.append(f"{nbl} cho trong (mong doi {WANT_WORDS})")
    if not ctx.get("bank_certain", True):
        warn.append("word_bank khong chac chan")
    return warn, {"words": nw, "examples": ex, "family": fam,
                  "bank": nb, "blanks": nbl, "p5": p5}


print("\n=== KIEM TRA CHAT LUONG ===")
print(f"{'Bai':<6}{'Tu':>4}{'ViDu':>7}{'Fam':>6}{'Bank':>6}{'Trong':>7}{'P5':>4}  Tinh trang")
bad = []
for lid in done:
    warn, s = audit(lid)
    status = "OK" if not warn else "; ".join(warn)
    if warn:
        bad.append(lid)
    print(f"L{lid:02d}   {s['words']:>4}{s['examples']:>7}{s['family']:>6}"
          f"{s['bank']:>6}{s['blanks']:>7}{s['p5']:>4}  {status}")

ok = len(done) - len(bad)
print()
print(f"{ok}/{len(done)} bai dat chuan day du "
      f"({WANT_WORDS} tu, {WANT_EXAMPLES} vi du, {WANT_FAMILY} dong fam, "
      f"{WANT_BANK} bank, {WANT_WORDS} cho trong).")
if bad:
    print(f"{len(bad)} bai thieu du lieu do MinerU doc sot: {bad}")
    print("Xem chi tiet: python scripts\\diagnose_flags.py")
    print("Anh scan tuong ung: extracted_data/lesson_page_scans/lesson_NN/")
    print("Neu vi du con trong Markdown thi khoi phuc duoc -> them vao "
          "ORPHANS/PATCHES trong scripts/patch_missing.py.")
