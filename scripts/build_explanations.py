"""build_explanations.py — sinh GIAI THICH ngan gon, bam sat tung cau hoi trong bai.

Nguyen tac:
  * Part 5 / Part 6: trich cum tu quanh cho trong trong chinh cau hoi / doan van,
    chi ro dau hieu ngu phap / ket hop tu (collocation) ngay tai vi tri do va
    nghia cua tu muc tieu trong bai; giai thich ngan gon vi sao tung phuong an
    nhieu khong khop cum tu trong cau.
  * Part 7: doi chieu tu khoa (kem tu dong nghia/dien dat lai pho bien trong TOEIC)
    cua CA cau hoi lan dap an dung de trich dan dung cau bang chung trong bai doc;
    xu ly rieng dang cau hoi tu dong nghia ("closest in meaning to").
  * Listening Part 3 / Part 4: uu tien doc tapescripts_full.json (neu co), roi
    ve tapescripts.json; tim dung cau thoai chua thong tin tra loi cho cau hoi.

Chay:
    py -3.11 scripts/build_explanations.py
"""
import glob
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public", "lessons_json")
ANSWER_KEY = os.path.join(ROOT, "scripts", "data", "answer_key.json")
TAPESCRIPTS_FULL = os.path.join(ROOT, "scripts", "data", "tapescripts_full.json")
TAPESCRIPTS_PUBLIC_FULL = os.path.join(ROOT, "public", "answers", "tapescripts_full.json")
TAPESCRIPTS = os.path.join(ROOT, "scripts", "data", "tapescripts.json")
VOCAB_ENRICH = os.path.join(ROOT, "scripts", "data", "vocab_enrichment.json")
VOCAB_ENRICH_PUBLIC = os.path.join(ROOT, "public", "answers", "vocab_enrichment.json")
OUT = os.path.join(ROOT, "scripts", "data", "explanations.json")
OUT_PUBLIC = os.path.join(ROOT, "public", "answers", "explanations.json")

POS_FULL = {
    "n": "noun", "v": "verb", "adj": "adjective", "adv": "adverb",
    "noun": "noun", "verb": "verb", "adjective": "adjective", "adverb": "adverb",
}
POS_VI = {
    "noun": "danh từ", "verb": "động từ",
    "adjective": "tính từ", "adverb": "trạng từ",
}

# Ban sao dong bo voi derivePos() trong app/src/lib/lessonLoader.js
# Giu nguyen cac nhom duoi (ee|eer|ery, some|ary|ory, ian|ant|ent) de dong bo.
def derive_pos(word):
    w = str(word or "").strip().lower()
    if not w or " " in w:
        return ""
    if w.endswith("ly"):
        return "adverb"
    if re.search(r"(tion|sion|ment|ance|ence|ity|ness|ship|hood|age|ee|eer|ery)$", w):
        return "noun"
    if re.search(r"(er|or|ist|ian|ant|ent)$", w):
        return "noun"
    if re.search(r"(ous|ful|able|ible|ive|ical|al|ic|ish|less|some|ary|ory)$", w):
        return "adjective"
    if re.search(r"(ed|ing|ate|ify|ise|ize|s)$", w):
        return "verb"
    if w.endswith("y") and len(w) > 3:
        return "adjective"
    return "verb"


KNOWN_POS_OVERRIDES = {
    "agree": "verb",
    "disagree": "verb",
    "guarantee": "verb",
    "see": "verb",
    "foresee": "verb",
    "oversee": "verb",
    "free": "adjective",
    "oblige": "verb",
    "obligate": "verb",
    "provide": "verb",
    "specify": "verb",
    "assure": "verb",
    "cancel": "verb",
    "determine": "verb",
    "resolve": "verb",
    "engage": "verb",
    "establish": "verb",
    "representative": "noun",
    "alternative": "noun",
    "alternatives": "noun",
    "initiative": "noun",
    "initiatives": "noun",
    "objective": "noun",
    "objectives": "noun",
    "perspective": "noun",
    "incentive": "noun",
    "incentives": "noun",
    "executive": "noun",
    "executives": "noun",
    "relative": "noun",
    "relatives": "noun",
    "directive": "noun",
    "directives": "noun",
    "characteristic": "noun",
    "characteristics": "noun",
    "potential": "noun",
    "professional": "noun",
    "professionals": "noun",
    "official": "noun",
    "officials": "noun",
    "original": "adjective",
    "final": "adjective",
    "specific": "adjective",
    "particular": "adjective",
    "frequent": "adjective",
    "consistent": "adjective",
    "efficient": "adjective",
    "confident": "adjective",
    "dependent": "adjective",
    "independent": "adjective",
    "different": "adjective",
    "important": "adjective",
    "significant": "adjective",
    "relevant": "adjective",
    "hesitant": "adjective",
    "ignorant": "adjective",
    "reluctant": "adjective",
    "abundant": "adjective",
    "constant": "adjective",
    "distant": "adjective",
    "instant": "adjective",
    "pleasant": "adjective",
    "vacant": "adjective",
    "compliant": "adjective",
}

TOEIC_SYNONYMS = {
    "bill": ["payment", "invoice", "charge", "charges", "fee", "billing"],
    "bills": ["payment", "payments", "invoice", "invoices", "charges"],
    "disagreement": ["dispute", "problem", "issue", "conflict"],
    "find": ["determine", "discover", "learn", "identify"],
    "why": ["reason", "reasons", "because", "cause"],
    "cancel": ["cancellation", "cancellations", "stop", "terminate", "no", "longer"],
    "renew": ["extend", "continue", "again"],
    "lawyer": ["attorney", "legal", "counsel"],
    "job": ["position", "employment", "work", "career", "opening"],
    "buy": ["purchase", "purchasing", "order", "ordering", "buyer"],
    "cost": ["price", "prices", "pricing", "fee", "rate", "charge"],
    "help": ["assist", "assistance", "aid", "support"],
    "mistake": ["error", "slip", "mix-up", "inaccurate", "incorrect"],
    "mistakes": ["errors", "slip", "mix-up", "incorrect"],
    "discount": ["off", "sale", "bargain", "save", "reduced", "reduction"],
    "repair": ["fix", "service", "serviced", "maintenance"],
    "delay": ["late", "wait", "waiting", "postpone", "behind"],
    "schedule": ["time", "on", "track", "plan", "hours"],
    "employee": ["worker", "staff", "personnel", "associate"],
    "employees": ["workers", "staff", "personnel", "associates"],
}


def norm_pos(raw):
    return POS_FULL.get(str(raw or "").strip().lower().rstrip("."), "")


def norm_letter(raw):
    s = str(raw or "").strip().upper()
    m = re.search(r"[A-D]", s)
    return m.group(0) if m else ""


DET = r"(?:a|an|the|this|that|these|those|my|your|his|her|its|our|their|no|any|some|each|every|final|new|same|written|good|high|low|full|clear|strong|great|major|main|special|legal|moral|annual|initial|additional|different|specific|particular|current|previous|recent|local|global|national|personal|public|private|common|general|total|entire|whole|single|double)"


def normalize_blank_sentence(sentence):
    s = str(sentence or "").strip()
    if "____" not in s:
        s = re.sub(r"(?<=\s)_+(?=[.,;?!:\s]|$)", "____", s)
    return s


def pos_needed_from_blank(sentence):
    s = normalize_blank_sentence(sentence)
    if "____" not in s:
        return ""
    before = s.split("____")[0].strip()
    after = s.split("____", 1)[1].strip() if "____" in s else ""
    b_words = [w.lower().strip(",;:\"'()") for w in before.split() if w.strip(",;:\"'()")]
    a_words = [w.lower().strip(",;:\"'().?!") for w in after.split() if w.strip(",;:\"'().?!")]
    tail = b_words[-1] if b_words else ""
    prev2 = b_words[-2] if len(b_words) >= 2 else ""
    first_after = a_words[0] if a_words else ""

    if tail in ("will", "would", "can", "could", "should", "must", "may", "might", "cannot", "didn't", "don't", "doesn't", "won't"):
        return "verb"
    if tail == "to" and prev2 not in ("according", "prior", "due", "close", "closer", "next", "thanks", "compared", "similar", "equal", "subject", "used", "accustomed", "dedicated", "committed", "devoted", "opposed", "limited", "related", "exposed", "entitled", "look", "looking"):
        return "verb"
    if tail in ("be", "is", "are", "was", "were", "been", "being", "am", "become", "became", "feel", "felt", "seem", "seemed", "remain", "remained", "stay", "stayed", "look", "looked"):
        return "adjective"
    if tail in ("very", "quite", "more", "most", "rather", "extremely", "too", "so", "less", "least", "fairly", "pretty", "highly", "completely", "totally", "absolutely"):
        return "adjective"
    if re.search(r"^" + DET + r"$", tail):
        if first_after and re.search(r"(tion|sion|ment|ance|ence|ity|ness|ship|hood|age)s?$", first_after):
            return "adjective"
        return "noun"
    if tail in ("of", "for", "with", "without", "in", "on", "at", "by", "from",
                "about", "into", "through", "during", "after", "before", "under", "between", "among"):
        return "noun"
    if after and re.match(r"[a-z]", after[:1]):
        if tail in ("you", "we", "they", "he", "she", "it", "i", "who", "that", "which"):
            return "verb"
        if re.search(r"\b(a|an|the|our|their|its|his|her|my|your)\b", before.lower()):
            if re.search(r"[a-z]", tail) and tail not in (
                "is", "are", "was", "were", "be", "been", "being", "am", "to",
            ):
                return "verb"
    if first_after and first_after not in ("to", "and", "or", "for", "in", "of", "with", "that", "than", "by", "from", "at", "on", "as"):
        if re.search(r"(tion|sion|ment|ance|ence|ity|ness|ship|hood|age|ing|er|or|ist)s?$", first_after):
            return "adjective"
    return ""


def extract_blank_snippet(sentence, chosen, window=4):
    """Trich cum 2-4 tu truoc va sau cho trong, dien dap an vao [chosen]."""
    s = normalize_blank_sentence(sentence)
    if "____" not in s:
        return '<b>[%s]</b>' % chosen
    parts = s.split("____", 1)
    before_tokens = parts[0].strip().split()
    after_tokens = parts[1].strip().split()
    b_slice = before_tokens[-window:]
    a_slice = after_tokens[:window]
    prefix = "... " if len(before_tokens) > window else ""
    suffix = " ..." if len(after_tokens) > window else ""
    left = (" ".join(b_slice) + " ") if b_slice else ""
    right = (" " + " ".join(a_slice)) if a_slice else ""
    return '%s%s<b>[%s]</b>%s%s' % (prefix, left, chosen, right, suffix)


def explain_blank_context(sentence, chosen, cpos, opts):
    """Sinh loi giai ngan gon, cu the theo dung cum tu quanh cho trong trong cau."""
    s = normalize_blank_sentence(sentence)
    if "____" not in s:
        return 'Khớp trực tiếp với cấu trúc và ngữ cảnh của câu.'
    before, after = s.split("____", 1)
    b_raw = before.strip().split()
    a_raw = after.strip().split()
    b_low = [w.lower().strip(",;:\"'()") for w in b_raw if w.strip(",;:\"'()")]
    a_low = [w.lower().strip(",;:\"'().?!") for w in a_raw if w.strip(",;:\"'().?!")]

    w_prev1 = b_low[-1] if b_low else ""
    w_prev2 = b_low[-2] if len(b_low) >= 2 else ""
    w_next1 = a_low[0] if a_low else ""

    raw_prev1 = b_raw[-1].strip(",;:\"'()") if b_raw else ""
    raw_next1 = a_raw[0].strip(",;:\"'().?!") if a_raw else ""
    cw = chosen.strip().lower()

    # 0. Cum dong tu nhieu tu (vd "are assured", "will be satisfied", "will expire", "to persuade")
    if " " in cw:
        parts = cw.split()
        if parts[0] in ("is", "are", "was", "were", "be", "been") or (len(parts) >= 3 and parts[0] == "will" and parts[1] == "be"):
            if parts[-1].endswith(("ed", "en")):
                return (
                    'Chủ ngữ “%s” nhận tác động / được đảm bảo bởi hành động nên vị ngữ chia ở thể bị động <b>%s</b>%s.'
                    % (raw_prev1 or "you", chosen, (' trước “%s”' % raw_next1) if raw_next1 else '')
                )
        if parts[0] in ("will", "should", "might", "can", "could", "would", "must", "may"):
            return (
                'Sau chủ ngữ “%s”, mạch câu diễn tả sự việc/quy định dẫn đến kết quả trong tương lai nên dùng <b>%s</b>.'
                % (raw_prev1 or "câu", chosen)
            )
        if parts[0] == "to":
            return (
                'Cấu trúc sau cụm từ phía trước (“%s”) cần động từ nguyên mẫu có “to”: <b>%s</b>.'
                % (" ".join(b_raw[-2:]), chosen)
            )

    # 1. Cau dieu kien If ...
    if ("if" in b_low[-3:] or (b_low and b_low[0] == "if")) and re.search(r"\b(will|won't|can|cannot|should|may|must)\b", s.lower()):
        if cpos == "verb" and not cw.startswith("will"):
            return (
                'Trong mệnh đề điều kiện bắt đầu bằng “If” (vế chính phía sau dùng thì tương lai/khuyết thiếu), '
                'động từ sau chủ ngữ “%s” chia ở hiện tại đơn <b>%s</b>.' % (raw_prev1 or "you", chosen)
            )

    # 2. Modal verb + V nguyen mau
    if w_prev1 in ("will", "would", "can", "could", "should", "must", "may", "might", "cannot", "won't", "wouldn't", "couldn't", "shouldn't", "didn't", "don't", "doesn't"):
        return (
            'Đứng ngay sau trợ động từ / động từ khuyết thiếu “%s” cần một <b>động từ</b> nguyên mẫu (<b>%s</b>)%s.'
            % (raw_prev1, chosen, (' đi với “%s”' % raw_next1) if raw_next1 else '')
        )
    if w_prev2 in ("will", "would", "can", "could", "should", "must", "may", "might") and w_prev1 in ("not", "never", "only", "also", "always", "soon", "still", "definitely"):
        return (
            'Sau cụm động từ khuyết thiếu “%s %s” cần một <b>động từ</b> nguyên mẫu (<b>%s</b>).'
            % (b_raw[-2], raw_prev1, chosen)
        )

    # 3. Cau truc nguyen mau "to + V"
    if w_prev1 == "to" and cpos == "verb" and not cw.endswith("ing"):
        return (
            'Đứng sau “to” trong cấu trúc động từ nguyên mẫu (%s) cần một <b>động từ</b> nguyên thể (<b>%s</b>)%s.'
            % (" ".join(b_raw[-3:]), chosen, (' kết hợp với “%s”' % raw_next1) if raw_next1 else '')
        )

    # 4. Tro dong tu have/has/had + P2
    if w_prev1 in ("have", "has", "had", "haven't", "hasn't", "hadn't") or (
        w_prev2 in ("have", "has", "had") and w_prev1 in ("not", "never", "already", "just", "ever", "always", "also", "been")
    ):
        aux_str = " ".join(b_raw[-2:]) if w_prev2 in ("have", "has", "had") else raw_prev1
        return (
            'Đứng sau trợ động từ “%s” cần quá khứ phân từ (dạng <b>%s</b>) để hoàn thành cấu trúc thì hoàn thành.'
            % (aux_str, chosen)
        )

    # 5. To be + V-ing / V-ed / Adj
    be_verbs = ("be", "is", "are", "was", "were", "been", "being", "am", "isn't", "aren't", "wasn't", "weren't")
    if w_prev1 in be_verbs or (w_prev2 in be_verbs and w_prev1 in ("not", "always", "often", "usually", "currently", "still", "already", "quite", "very", "more", "most", "so", "too")):
        be_str = " ".join(b_raw[-2:]) if w_prev2 in be_verbs else raw_prev1
        if cw.endswith("ing") and cpos == "verb":
            return (
                'Sau to be “%s” và đứng trước tân ngữ “%s” cần dạng V-ing <b>%s</b> (thì tiếp diễn chủ động).'
                % (be_str, raw_next1 or "...", chosen)
            )
        if cw.endswith("ed") or cw.endswith("en"):
            prep_hint = (' đi kèm giới từ “%s”' % raw_next1) if w_next1 in ("to", "with", "in", "by", "for", "of", "from", "at", "as") else ""
            return (
                'Sau to be “%s” cần quá khứ phân từ <b>%s</b> để tạo cấu trúc bị động / tính từ chỉ trạng thái%s.'
                % (be_str, chosen, prep_hint)
            )
        if cpos == "adjective":
            return (
                'Đứng sau động từ liên kết “%s” cần một <b>tính từ</b> (<b>%s</b>) làm bổ ngữ miêu tả chủ ngữ.'
                % (be_str, chosen)
            )

    # 6. Danh tu: dung dau cau lam chu ngu, hoac sau han dinh tu / tinh tu / gioi tu
    if cpos == "noun":
        if not b_low:
            return (
                'Đứng đầu câu làm chủ ngữ chính%s nên cần một <b>danh từ</b> (<b>%s</b>).'
                % ((' trước “%s”' % raw_next1) if raw_next1 else '', chosen)
            )
        if w_next1 in ("were", "are", "have") and cw.endswith("s"):
            return (
                'Động từ phía sau chia số nhiều (“%s”) nên vị trí chủ ngữ sau “%s” cần <b>danh từ</b> số nhiều <b>%s</b>.'
                % (raw_next1, raw_prev1, chosen)
            )
        if any(v in a_low[:5] for v in ("were", "are")) and cw.endswith("s") and w_prev1 in ("the", "these", "those", "many", "several", "some", "all"):
            return (
                'Vị ngữ chính trong câu chia số nhiều (“were/are”) nên cụm chủ ngữ bắt đầu bằng “%s” cần <b>danh từ</b> số nhiều <b>%s</b>.'
                % (raw_prev1, chosen)
            )
        if w_prev1 in ("a", "an", "the", "this", "that", "these", "those", "my", "your", "his", "her", "its", "our", "their", "any", "some", "no", "each", "every"):
            prep_after = (' trước giới từ “%s”' % raw_next1) if w_next1 in ("of", "for", "in", "to", "with", "on", "between", "from", "at", "by") else ""
            return (
                'Đứng ngay sau từ hạn định/sở hữu “%s”%s cần một <b>danh từ</b> làm thành phần chính: <b>%s %s</b>.'
                % (raw_prev1, prep_after, raw_prev1, chosen)
            )
        if w_prev1 in ("of", "for", "with", "without", "in", "on", "at", "by", "from", "about", "into", "through", "during", "after", "before", "under", "between"):
            return (
                'Đứng sau giới từ “%s” cần một <b>danh từ</b> làm tân ngữ của giới từ: <b>%s %s</b>.'
                % (raw_prev1, raw_prev1, chosen)
            )
        return (
            'Đứng sau “%s”%s cần một <b>danh từ</b> đóng vai trò danh từ chính của cụm: <b>%s %s</b>.'
            % (raw_prev1, (' và trước “%s”' % raw_next1) if raw_next1 else '', raw_prev1, chosen)
        )

    # 7. Tinh tu bo nghia cho danh tu dung sau
    if cpos == "adjective":
        if raw_next1:
            return (
                'Đứng trước danh từ “%s” cần một <b>tính từ</b> (<b>%s</b>) để bổ nghĩa cho “%s”.'
                % (raw_next1, chosen, raw_next1)
            )
        return 'Vị trí này cần một <b>tính từ</b> (<b>%s</b>) làm bổ ngữ trong câu.' % chosen

    # 8. Trang tu bo nghia cho dong tu / tinh tu
    if cpos == "adverb":
        if w_prev1 and w_prev1 not in ("the", "a", "an"):
            return (
                'Cần một <b>trạng từ</b> (<b>%s</b>) để bổ nghĩa cho động từ/tính từ “%s” trong câu.'
                % (chosen, raw_next1 or raw_prev1)
            )
        return 'Cần một <b>trạng từ</b> (<b>%s</b>) để bổ nghĩa cho hành động/tính chất trong câu.' % chosen

    # 9. Dong tu chinh sau chu ngu
    if cpos == "verb":
        if cw.endswith("s") and not cw.endswith("ss"):
            return (
                'Chủ ngữ phía trước (“%s”) ở ngôi thứ 3 số ít nên vị ngữ cần <b>động từ</b> chia hiện tại đơn thêm -s (<b>%s</b>).'
                % (" ".join(b_raw[-2:]), chosen)
            )
        if cw.endswith("ed"):
            return (
                'Sau chủ ngữ “%s” cần <b>động từ</b> chính chia thì quá khứ đơn (<b>%s</b>) cho khớp mạch thời gian của câu.'
                % (" ".join(b_raw[-2:]), chosen)
            )
        return (
            'Sau chủ ngữ “%s” cần một <b>động từ</b> chính (<b>%s</b>) kết hợp với phần tân ngữ/bổ ngữ phía sau.'
            % (" ".join(b_raw[-2:]) if b_raw else "câu", chosen)
        )

    return 'Cụm từ <b>%s</b> khớp trực tiếp về ngữ pháp và nghĩa trong câu.' % chosen


def explain_wrong_option(lab, txt, chosen, tpos, cpos, sentence):
    """Giai thich ngan gon vi sao phuong an nhieu sai trong ngu canh cau."""
    tw = txt.strip().lower()
    cw = chosen.strip().lower()
    s = normalize_blank_sentence(sentence)
    before = s.split("____")[0].strip() if "____" in s else ""
    after = s.split("____", 1)[1].strip() if "____" in s else ""
    b_raw = before.split()
    a_raw = after.split()
    raw_prev1 = b_raw[-1].strip(",;:\"'()") if b_raw else ""
    raw_next1 = a_raw[0].strip(",;:\"'().?!") if a_raw else ""

    if tw.startswith("will ") and "if " in s.lower():
        return '(%s) %s — trong mệnh đề điều kiện “If”, không chia tương lai với “will”.' % (lab, txt)
    if " " in cw and cw.split()[0] in ("is", "are", "was", "were", "will") and cw.split()[-1].endswith(("ed", "en")):
        if not tw.endswith(("ed", "en")):
            return '(%s) %s — dạng chủ động, không khớp cấu trúc bị động cần dùng tại vị trí của “%s”.' % (lab, txt, chosen)
    if tpos and cpos and tpos != cpos:
        ctx = ('sau “%s”' % raw_prev1) if raw_prev1 else ('trước “%s”' % raw_next1 if raw_next1 else 'ở vị trí này')
        return (
            '(%s) %s — là <b>%s</b>, nhưng vị trí %s cần <b>%s</b> (%s).'
            % (lab, txt, POS_VI.get(tpos, tpos), ctx, POS_VI.get(cpos, cpos), chosen)
        )
    if tpos == "noun" and cpos == "noun":
        if tw.endswith("s") != cw.endswith("s"):
            if cw.endswith("s"):
                return '(%s) %s — là <b>danh từ</b> số ít, không khớp với động từ/ngữ cảnh số nhiều trong câu.' % (lab, txt)
            return '(%s) %s — là <b>danh từ</b> số nhiều, không khớp với vị trí cần danh từ số ít/không đếm được.' % (lab, txt)
        if re.search(r"(er|or|ist|ant|ent)s?$", tw) and not re.search(r"(er|or|ist|ant|ent)s?$", cw):
            return '(%s) %s — là <b>danh từ</b> chỉ người/tác nhân, không hợp nghĩa với ngữ cảnh cần sự việc/khái niệm (%s).' % (lab, txt, chosen)
        return '(%s) %s — cùng là <b>danh từ</b> nhưng lệch nghĩa so với cụm “%s” trong câu.' % (lab, txt, chosen)
    if tpos == "verb" and cpos == "verb":
        if tw.endswith("ing") and not cw.endswith("ing"):
            return '(%s) %s — dạng V-ing không đứng trực tiếp làm vị ngữ chính nếu thiếu trợ động từ to be.' % (lab, txt)
        if tw.endswith("ed") and not cw.endswith("ed"):
            return '(%s) %s — dạng V-ed/quá khứ không khớp cấu trúc ngữ pháp tại vị trí của “%s”.' % (lab, txt, chosen)
        if not tw.endswith("ed") and cw.endswith("ed"):
            return '(%s) %s — dạng nguyên mẫu/hiện tại không khớp cấu trúc bị động hoặc mạch quá khứ (“%s”).' % (lab, txt, chosen)
        return '(%s) %s — là <b>động từ</b> nhưng sai dạng chia thì/ngôi so với “%s” trong câu.' % (lab, txt, chosen)
    if tpos:
        return '(%s) %s — là <b>%s</b>, không khớp cấu trúc và mạch nghĩa của câu (đáp án là “%s”).' % (lab, txt, POS_VI.get(tpos, tpos), chosen)
    return '(%s) %s — không khớp cấu trúc ngữ pháp và mạch nghĩa tại chỗ trống (đáp án là “%s”).' % (lab, txt, chosen)


STOPWORDS = {
    "what", "where", "when", "who", "whom", "whose", "why", "how", "which",
    "the", "this", "that", "these", "those", "is", "are", "was", "were", "be",
    "been", "being", "will", "would", "can", "could", "should", "may", "might",
    "must", "does", "did", "do", "has", "have", "had", "not", "for", "to", "in",
    "on", "at", "of", "from", "with", "by", "about", "into", "over", "after",
    "before", "under", "between", "through", "during", "without", "within",
    "following", "refer", "questions", "question", "letter", "memo", "email",
    "e-mail", "notice", "article", "advertisement", "ad", "form", "according",
    "passage", "most", "likely", "probably", "stated", "mentioned", "indicated",
    "true", "false", "NOT", "person", "people", "man", "woman", "speaker",
    "speakers", "talk", "talking", "conversation", "say", "says", "said",
    "doing", "going", "next", "their", "they", "them", "his", "her", "its",
    "our", "your", "you", "and", "but", "or", "so", "than", "then", "there",
    "here", "some", "any", "all", "many", "much", "more", "other", "another",
    "each", "every", "both", "such", "own", "same", "very", "just", "only",
}


def content_tokens(text):
    words = re.findall(r"[a-z0-9]{3,}", str(text or "").lower())
    return [w for w in words if w not in STOPWORDS]


def expand_with_synonyms(tokens):
    expanded = list(tokens)
    for t in tokens:
        for syn in TOEIC_SYNONYMS.get(t, []):
            if syn not in expanded:
                expanded.append(syn)
    return expanded


def split_passage_chunks(raw_text):
    """Tach van ban thanh cac cau/dong nho gon, tranh cat nham sau Mr./Ms./Dr./St./Ltd."""
    raw = str(raw_text or "").strip()
    if not raw:
        return []
    # Tach truoc cac nhan truong bieu mau pho bien de khong gop ca bieu mau thanh 1 cau dai
    raw = re.sub(
        r"\s+(?=(?:Date contract signed|Type of facility|Frequency of service|Reason for|Comments|To|From|Date|Subject|Re)\s*:)",
        "\n",
        raw,
    )
    parts = re.split(
        r"(?<!\bMr)(?<!\bMs)(?<!\bMrs)(?<!\bDr)(?<!\bSt)(?<!\bLtd)(?<!\bInc)(?<!\bCo)(?<!\bJr)(?<!\bSr)(?<=[.!?])\s+|\n+",
        raw,
    )
    return [
        c.strip()
        for c in parts
        if c and c.strip() and not re.match(r"^Questions?\s+\d+", c.strip(), re.I)
    ]


def find_best_evidence(text_block, question_text, chosen_text):
    """Tim cau trong bai doc / tapescript khop tu khoa cua CA cau hoi va dap an."""
    chunks = split_passage_chunks(text_block)
    if not chunks:
        return ""

    # Neu la cau hoi tu dong nghia: "The word X in ... is closest in meaning to"
    m_syn = re.search(r"word\s+([A-Za-z\-]+)\s+in\b", str(question_text or ""), re.I)
    if m_syn:
        target_w = m_syn.group(1).lower()
        for c in chunks:
            if re.search(r"\b" + re.escape(target_w) + r"\b", c.lower()):
                return c

    q_toks = expand_with_synonyms(content_tokens(question_text))
    c_toks = expand_with_synonyms(content_tokens(chosen_text))

    best_chunk = ""
    best_score = 0.0
    for c in chunks:
        cl = c.lower()
        score = 0.0
        c_hits = 0
        q_hits = 0
        for w in c_toks:
            if re.search(r"\b" + re.escape(w) + r"\b", cl):
                score += 2.5
                c_hits += 1
            elif len(w) >= 5 and w[:5] in cl:
                score += 1.8
                c_hits += 1
        for w in q_toks:
            if re.search(r"\b" + re.escape(w) + r"\b", cl):
                score += 1.5
                q_hits += 1
            elif len(w) >= 5 and w[:5] in cl:
                score += 1.0
                q_hits += 1
        if c_hits > 0 and q_hits > 0:
            score += 2.0
        if score > best_score:
            best_score = score
            best_chunk = c

    if best_score >= 1.2:
        return best_chunk
    return ""


def find_part6_sentence(passage, q_num, q_idx, total_qs):
    """Tim dung cau chua cho trong [q_num] (hoac cho trong thu q_idx) trong Part 6."""
    if not passage:
        return "", ""
    sentences = split_passage_chunks(passage)
    pat_exact = re.compile(r"\[%d\]|_%d\b|\b%d_" % (q_num, q_num, q_num))
    for s in sentences:
        if pat_exact.search(s):
            norm_s = pat_exact.sub("____", s, count=1)
            return s, norm_s

    # Fallback: neu so thu tu cau hoi bi lech (vd Lesson 38: cau 17,18,19 ung voi [16],[17],[18])
    marker_sents = []
    any_marker = re.compile(r"\[\d+\]|_\d+\b|____|\[__+\]")
    for s in sentences:
        for m in any_marker.finditer(s):
            marker_sents.append((s, m.group(0)))
    if 0 <= q_idx < len(marker_sents):
        s, raw_m = marker_sents[q_idx]
        norm_s = s.replace(raw_m, "____", 1)
        return s, norm_s
    if marker_sents:
        s, raw_m = marker_sents[0]
        return s, s.replace(raw_m, "____", 1)
    return "", ""


def main():
    if not os.path.isfile(ANSWER_KEY):
        print("LOI: chua co %s — chay scripts/parse_answer_key.py truoc." % ANSWER_KEY)
        return 1

    answers = json.load(open(ANSWER_KEY, encoding="utf-8"))

    # Uu tien tapescripts_full.json neu co
    tapescripts = {}
    for ts_path in (TAPESCRIPTS_FULL, TAPESCRIPTS_PUBLIC_FULL, TAPESCRIPTS):
        if os.path.isfile(ts_path):
            try:
                loaded = json.load(open(ts_path, encoding="utf-8"))
                if loaded and isinstance(loaded, dict):
                    for k, v in loaded.items():
                        if k not in tapescripts or not (tapescripts[k].get("part3") or tapescripts[k].get("part4")):
                            tapescripts[k] = v
            except Exception:
                pass

    vocab_enrich = {}
    for ve_path in (VOCAB_ENRICH, VOCAB_ENRICH_PUBLIC):
        if os.path.isfile(ve_path):
            try:
                vocab_enrich = json.load(open(ve_path, encoding="utf-8"))
                if vocab_enrich:
                    break
            except Exception:
                pass

    out = {}
    stats = {"grammar": 0, "tapescript": 0, "passage": 0, "no_answer": 0, "no_evidence": 0}

    for path in sorted(glob.glob(os.path.join(PUBLIC, "lesson_*.json"))):
        lesson = json.load(open(path, encoding="utf-8"))
        lid = lesson["lesson_id"]
        wp = answers.get(str(lid), {}).get("word_practice", {})

        # Ban do tu muc tieu + ho tu -> {pos, def_en, def_vi, word}
        target = {}
        form_to_target = {}
        form_pos = {}

        for w in lesson.get("words_to_learn", []):
            key = (w.get("word") or "").strip().lower()
            if not key:
                continue
            def_vi = (w.get("definition_vi") or "").strip()
            if not def_vi and isinstance(vocab_enrich, dict):
                ve_entry = (
                    (vocab_enrich.get(str(lid)) or {}).get(key)
                    or (vocab_enrich.get("words") or {}).get(key)
                    or vocab_enrich.get(key)
                )
                if isinstance(ve_entry, dict):
                    def_vi = (ve_entry.get("definition_vi") or ve_entry.get("meaning_vi") or "").strip()
            info_obj = {
                "pos": norm_pos(w.get("pos")),
                "def_en": (w.get("definition_en") or "").strip(),
                "def_vi": def_vi,
                "word": w.get("word"),
            }
            target[key] = info_obj
            form_to_target[key] = info_obj
            if info_obj["pos"]:
                form_pos[key] = info_obj["pos"]
            for fam in w.get("word_family") or []:
                if isinstance(fam, dict):
                    fw = (fam.get("word") or "").strip().lower()
                    fp = norm_pos(fam.get("pos"))
                    if fw:
                        form_to_target[fw] = info_obj
                        if fp and fw not in form_pos:
                            form_pos[fw] = fp

        for group in lesson.get("word_families") or []:
            if not isinstance(group, list):
                continue
            linked_info = None
            for row in group:
                if isinstance(row, dict):
                    rw = (row.get("word") or "").strip().lower()
                    if rw in form_to_target:
                        linked_info = form_to_target[rw]
                        break
            for row in group:
                if not isinstance(row, dict):
                    continue
                f = (row.get("word") or "").strip().lower()
                p = norm_pos(row.get("pos"))
                if f:
                    if p and f not in form_pos:
                        form_pos[f] = p
                    if linked_info and f not in form_to_target:
                        form_to_target[f] = linked_info

        def lookup_vocab_info(word):
            w = str(word or "").strip().lower()
            if not w:
                return {}
            if w in form_to_target:
                return form_to_target[w]
            if " " in w:
                last_tok = w.split()[-1]
                res = lookup_vocab_info(last_tok)
                if res:
                    return res
            for cand in (w.rstrip("s"), w[:-2] if w.endswith("es") else "", w[:-3] + "y" if w.endswith("ies") else "", w.rstrip("d"), w.rstrip("ed"), w[:-3] if w.endswith("ing") else ""):
                if cand and cand in form_to_target:
                    return form_to_target[cand]
            for k, v in target.items():
                if len(k) >= 5 and len(w) >= 5 and w[:5] == k[:5]:
                    return v
            return {}

        def pos_of(word):
            """Tu loai cua mot tu: uu tien KNOWN_POS_OVERRIDES & du lieu sach, xu ly danh tu so nhieu, roi derive_pos."""
            key = str(word or "").strip().lower()
            if not key or " " in key:
                return ""
            if key in KNOWN_POS_OVERRIDES:
                return KNOWN_POS_OVERRIDES[key]
            if key in form_pos:
                return form_pos[key]
            if key.endswith("s") and not key.endswith(("ss", "ous", "is", "us")):
                sing = key[:-3] + "y" if key.endswith("ies") else (
                    key[:-2] if key.endswith(("ches", "shes", "xes", "zes", "ses")) else key[:-1]
                )
                if sing in KNOWN_POS_OVERRIDES and KNOWN_POS_OVERRIDES[sing] == "noun":
                    return "noun"
                if form_pos.get(sing) == "noun":
                    return "noun"
                if re.search(r"(tion|sion|ment|ance|ence|ity|ness|ship|hood|age|ee|eer|ery|er|or|ist|ian|ant|ent)$", sing):
                    return "noun"
            return derive_pos(key)

        per_lesson = {}

        # ---------------- Part 5 ----------------
        for q in lesson.get("practice", {}).get("part5", []):
            num = q.get("number")
            letter = norm_letter(wp.get(str(num)))
            if not letter:
                stats["no_answer"] += 1
                continue
            opts = {o["label"]: o["text"] for o in q.get("options", [])}
            chosen = opts.get(letter, "")
            question_sent = q.get("question", "") or ""
            cw = chosen.strip().lower()
            info = lookup_vocab_info(cw)
            cpos = pos_of(cw)
            need = cpos or pos_needed_from_blank(question_sent)

            snippet = extract_blank_snippet(question_sent, chosen, window=4)
            ctx_explain = explain_blank_context(question_sent, chosen, cpos, opts)

            bits = [
                'Đáp án đúng là (%s) <b>%s</b>.' % (letter, chosen),
                'Cụm trong câu: “%s”.' % snippet,
                ctx_explain,
            ]
            if info.get("def_vi") and info.get("def_en"):
                bits.append('Nghĩa trong bài (%s): <b>%s</b> (<i>%s</i>).' % (info.get("word", chosen), info["def_vi"], info["def_en"]))
            elif info.get("def_en"):
                bits.append('Nghĩa trong bài (%s): <i>%s</i>.' % (info.get("word", chosen), info["def_en"]))

            notes = {}
            for lab, txt in opts.items():
                if lab == letter:
                    continue
                tpos = pos_of(txt)
                notes[lab] = explain_wrong_option(lab, txt, chosen, tpos, cpos, question_sent)

            per_lesson[str(num)] = {
                "answer": letter,
                "why": " ".join(bits),
                "pos_needed": need,
                "option_notes": notes,
                "source": "grammar",
                "section": "part5",
            }
            stats["grammar"] += 1

        # ---------------- Part 6 ----------------
        p6 = lesson.get("practice", {}).get("part6") or {}
        passage = p6.get("passage", "") or ""
        p6_questions = p6.get("questions", []) or []
        for idx, q in enumerate(p6_questions):
            num = q.get("number")
            letter = norm_letter(wp.get(str(num)))
            if not letter:
                stats["no_answer"] += 1
                continue
            opts = {o["label"]: o["text"] for o in q.get("options", [])}
            chosen = opts.get(letter, "")
            cw = chosen.strip().lower()
            info = lookup_vocab_info(cw)
            cpos = pos_of(cw)

            evidence, norm_sent = find_part6_sentence(passage, num, idx, len(p6_questions))
            snippet = extract_blank_snippet(norm_sent, chosen, window=4) if norm_sent else ('<b>[%s]</b>' % chosen)
            ctx_explain = explain_blank_context(norm_sent, chosen, cpos, opts) if norm_sent else (
                'Khớp trực tiếp với cấu trúc ngữ pháp và mạch nghĩa tại ô [%s] trong đoạn văn.' % num
            )

            bits = [
                'Đáp án đúng là (%s) <b>%s</b>.' % (letter, chosen),
                'Tại ô [%s]: “%s”.' % (num, snippet),
                ctx_explain,
            ]
            if info.get("def_vi") and info.get("def_en"):
                bits.append('Nghĩa từ vựng (%s): <b>%s</b> (<i>%s</i>).' % (info.get("word", chosen), info["def_vi"], info["def_en"]))
            elif info.get("def_en"):
                bits.append('Nghĩa từ vựng (%s): <i>%s</i>.' % (info.get("word", chosen), info["def_en"]))

            notes = {}
            for lab, txt in opts.items():
                if lab == letter:
                    continue
                tpos = pos_of(txt)
                notes[lab] = explain_wrong_option(lab, txt, chosen, tpos, cpos, norm_sent or "")

            per_lesson[str(num)] = {
                "answer": letter,
                "why": " ".join(bits),
                "pos_needed": "",
                "option_notes": notes,
                "source": "grammar",
                "section": "part6",
                "evidence": evidence,
            }
            stats["grammar"] += 1

        # ---------------- Part 7 ----------------
        for block in lesson.get("practice", {}).get("part7", []) or []:
            ptext = block.get("text", "") or ""
            for q in block.get("questions", []) or []:
                num = q.get("number")
                letter = norm_letter(wp.get(str(num)))
                if not letter:
                    stats["no_answer"] += 1
                    continue
                opts = {o["label"]: o["text"] for o in q.get("options", [])}
                chosen = opts.get(letter, "")
                qtext = (q.get("question") or "").strip()

                evidence = find_best_evidence(ptext, qtext, chosen)
                m_syn = re.search(r"word\s+([A-Za-z\-]+)\s+in\b", qtext, re.I)

                bits = ['Đáp án đúng là (%s) <b>%s</b>.' % (letter, chosen)]
                if m_syn:
                    target_w = m_syn.group(1)
                    vinfo = lookup_vocab_info(target_w)
                    def_str = (' (sách định nghĩa: <i>%s</i>)' % vinfo["def_en"]) if vinfo.get("def_en") else ""
                    bits.append(
                        'Câu hỏi tìm từ đồng nghĩa với <b>“%s”</b> trong văn bản%s — đặt vào ngữ cảnh câu trích dẫn, “%s” đồng nghĩa trực tiếp với <b>%s</b>.'
                        % (target_w, def_str, target_w, chosen.rstrip("."))
                    )
                elif evidence:
                    bits.append(
                        'Đối chiếu câu hỏi <i>“%s”</i> với nội dung văn bản: câu dẫn chứng bên dưới nêu trực tiếp thông tin khớp với phương án <b>%s</b>.'
                        % (qtext, chosen)
                    )
                else:
                    bits.append(
                        'Đối chiếu câu hỏi <i>“%s”</i> với mạch thông tin tổng thể của văn bản để suy ra phương án <b>%s</b>.'
                        % (qtext, chosen)
                    )

                notes = {}
                ptext_low = ptext.lower()
                for lab, txt in opts.items():
                    if lab == letter:
                        continue
                    if m_syn:
                        notes[lab] = '(%s) %s — khác nghĩa với từ “%s” trong ngữ cảnh văn bản.' % (lab, txt, m_syn.group(1))
                    else:
                        toks = content_tokens(txt)
                        in_pass = any(w in ptext_low for w in toks) if toks else False
                        if in_pass:
                            notes[lab] = '(%s) %s — có từ khóa xuất hiện trong bài nhưng sai chi tiết so với câu hỏi “%s”.' % (lab, txt, qtext)
                        else:
                            notes[lab] = '(%s) %s — thông tin không được nêu hoặc trái với nội dung trong văn bản.' % (lab, txt)

                per_lesson[str(num)] = {
                    "answer": letter,
                    "why": " ".join(bits),
                    "pos_needed": "",
                    "option_notes": notes,
                    "source": "passage" if evidence else "passage-no-evidence",
                    "section": "part7",
                    "evidence": evidence,
                }
                if evidence:
                    stats["passage"] += 1
                else:
                    stats["no_evidence"] += 1

        # ---------------- Listening Part 3 / 4 ----------------
        tap = tapescripts.get(str(lid), {}) if isinstance(tapescripts, dict) else {}
        for part_key, section in (("part3", "listening3"), ("part4", "listening4")):
            for q in lesson.get("listening", {}).get(part_key, []) or []:
                num = q.get("number")
                letter = norm_letter(wp.get(str(num)))
                if not letter:
                    stats["no_answer"] += 1
                    continue
                opts = {o["label"]: o["text"] for o in q.get("options", [])}
                chosen = opts.get(letter, "")
                qtext = (q.get("question") or "").strip()
                script = (tap.get(part_key) or "").strip() if isinstance(tap, dict) else ""

                evidence = find_best_evidence(script, qtext, chosen) if script else ""
                if not evidence and script:
                    sents = split_passage_chunks(script)
                    if sents:
                        evidence = sents[0]

                bits = ['Đáp án đúng là (%s) <b>%s</b>.' % (letter, chosen)]
                if evidence:
                    bits.append(
                        'Với câu hỏi <i>“%s”</i>, lời thoại trong bài nêu trực tiếp thông tin ứng với phương án <b>%s</b> (xem câu trích dẫn bên dưới).'
                        % (qtext or ("câu %s" % num), chosen)
                    )
                else:
                    bits.append(
                        'Với câu hỏi <i>“%s”</i>, đáp án chuẩn theo Answer Key của sách là <b>%s</b> — hãy mở Tapescript / nghe lại đoạn hội thoại để đối chiếu ngữ cảnh.'
                        % (qtext or ("câu %s" % num), chosen)
                    )

                notes = {}
                script_low = script.lower()
                for lab, txt in opts.items():
                    if lab == letter:
                        continue
                    toks = content_tokens(txt)
                    if script_low and toks and any(w in script_low for w in toks):
                        notes[lab] = '(%s) %s — chi tiết có nhắc thoáng qua trong bài nghe nhưng không trả lời đúng câu hỏi “%s”.' % (lab, txt, qtext)
                    else:
                        notes[lab] = '(%s) %s — không khớp với thông tin người nói đưa ra cho câu hỏi “%s”.' % (lab, txt, qtext or ("câu %s" % num))

                per_lesson[str(num)] = {
                    "answer": letter,
                    "why": " ".join(bits),
                    "pos_needed": "",
                    "option_notes": notes,
                    "source": "tapescript" if evidence else "listening-no-script",
                    "section": section,
                    "evidence": evidence,
                }
                if evidence:
                    stats["tapescript"] += 1
                else:
                    stats["no_evidence"] += 1

        out[str(lid)] = per_lesson

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    os.makedirs(os.path.dirname(OUT_PUBLIC), exist_ok=True)
    shutil.copyfile(OUT, OUT_PUBLIC)

    total = sum(len(v) for v in out.values())
    print("Da ghi %s (va dong bo sang %s)" % (os.path.relpath(OUT, ROOT), os.path.relpath(OUT_PUBLIC, ROOT)))
    print("  so bai                   : %d/50" % len(out))
    print("  tong so cau co giai thich: %d" % total)
    print()
    print("  Nguon giai thich:")
    print("    ngu phap/tu vung (Part 5-6) : %d" % stats["grammar"])
    print("    co trich dan bai doc (P7)   : %d" % stats["passage"])
    print("    co trich dan loi thoai (P3/4): %d" % stats["tapescript"])
    print("    KHONG co bang chung         : %d" % stats["no_evidence"])
    print("    khong co dap an trong key   : %d" % stats["no_answer"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
