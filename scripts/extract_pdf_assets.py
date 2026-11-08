"""
Script 1: extract_pdf_assets.py
Tác dụng:
1. Tự động trích xuất toàn bộ 50 bức ảnh chụp của phần Listening Part 1 Photo (từ Lesson 1 -> 50).
2. Tự động xuất các trang scan của từng Lesson (6 trang/Lesson), Answer Key và Tapescript ra ảnh PNG sắc nét
   để chuẩn bị đưa vào Script 2 (OCR sang JSON bằng Gemini API hoặc Tesseract).

Cài đặt thư viện trước khi chạy:
    pip install pypdf pillow
"""

import os
import io
import json
import pypdf
from PIL import Image

PDF_PATH = "600 est_.pdf"
OUTPUT_DIR = "extracted_data"

def pick_full_page_scan(page):
    """Chon dung anh SCAN TOAN TRANG trong so cac anh nhung cua mot trang PDF.

    BUG CU (da sua): truoc day dung `max(pg.images, key=lambda x: len(x.data))`
    — tuc la chon anh co NHIEU BYTE NHAT. Sai, vi anh Part 1 Photo nhung trong
    trang la JPEG nen nang hon (vd 21.055 bytes) trong khi ban scan toan trang la
    TIFF nen nhe hon (20.714 bytes) du co kich thuoc lon hon nhieu.

    Hau qua: 37/50 trang "listening_practice" bi luu nham thanh ANH PART 1 PHOTO
    (296x312) thay vi ca trang (1456x1936). MinerU OCR mot buc anh chup anh ->
    khong co chu -> tra ve rong. Vi vay 37 bai mat toan bo cau hoi Part 3/Part 4
    du sach in rat ro.

    Cach chon dung: anh co DIEN TICH PIXEL lon nhat (khong phai nhieu byte nhat).
    Moi trang cua ban scan nay luon co mot anh TIFF toan trang ~1440x2000.
    """
    best, best_area = None, -1
    for im in page.images:
        try:
            pil = Image.open(io.BytesIO(im.data))
        except Exception:
            continue
        w, h = pil.size
        area = w * h
        # Bo qua anh rac/icon nho; ban scan toan trang luon >= 800px ca hai chieu.
        if area > best_area and w >= 800 and h >= 800:
            best, best_area = pil, area
    if best is not None:
        return best

    # Du phong: neu trang khong co anh nao du lon (trang la la), lay anh to nhat
    # theo dien tich de khong crash — nhung KHONG am tham lay anh nho roi OCR.
    best, best_area = None, -1
    for im in page.images:
        try:
            pil = Image.open(io.BytesIO(im.data))
        except Exception:
            continue
        area = pil.size[0] * pil.size[1]
        if area > best_area:
            best, best_area = pil, area
    return best


def main():
    if not os.path.exists(PDF_PATH):
        print(f"Không tìm thấy file {PDF_PATH}! Hãy đặt script cùng thư mục với file PDF.")
        return

    reader = pypdf.PdfReader(PDF_PATH)
    with open("book_structure_map.json", "r", encoding="utf-8") as f:
        book_map = json.load(f)

    photos_dir = os.path.join(OUTPUT_DIR, "part1_photos")
    pages_dir = os.path.join(OUTPUT_DIR, "lesson_page_scans")
    os.makedirs(photos_dir, exist_ok=True)
    os.makedirs(pages_dir, exist_ok=True)

    print("Đang trích xuất 50 ảnh Part 1 Photo và các trang scan từng Lesson...")
    for lesson in book_map["lessons"]:
        lid = lesson["lesson_id"]
        p_map = lesson["pdf_pages_1indexed"]

        # 1. Trích xuất ảnh Part 1 Photo ở trang thứ 4 của mỗi Lesson
        photo_page = reader.pages[p_map["listening_practice"] - 1]
        best_img = None
        best_area = 0
        for im in photo_page.images:
            pil_im = Image.open(io.BytesIO(im.data))
            w, h = pil_im.size
            if im.name.endswith(".jpg") and w >= 150 and h >= 200:
                if w * h > best_area:
                    best_area = w * h
                    best_img = pil_im

        if best_img:
            if best_img.mode not in ("RGB", "L"):
                best_img = best_img.convert("RGB")
            best_img.save(os.path.join(photos_dir, f"lesson_{lid:02d}.jpg"), quality=95)

        # 2. Xuất 6 trang scan TIFF của Lesson ra thư mục riêng để tiện OCR theo từng bài
        lesson_scan_folder = os.path.join(pages_dir, f"lesson_{lid:02d}")
        os.makedirs(lesson_scan_folder, exist_ok=True)
        for section_name, pdf_p_num in p_map.items():
            pg = reader.pages[pdf_p_num - 1]
            # Lay ban SCAN TOAN TRANG (dien tich pixel lon nhat), khong phai anh
            # nhieu byte nhat — xem pick_full_page_scan() de biet vi sao.
            pil_scan = pick_full_page_scan(pg)
            if pil_scan is None:
                print(f"  [CANH BAO] Lesson {lid:02d} / {section_name}: "
                      f"trang {pdf_p_num} khong co anh scan nao")
                continue
            pil_scan.save(os.path.join(lesson_scan_folder, f"{pdf_p_num:03d}_{section_name}.png"))

        print(f"  [OK] Lesson {lid:02d}: {lesson['title']}")

    # 3. Xuất trang Answer Key (333-336) và Tapescript (341-373)
    ref_dir = os.path.join(OUTPUT_DIR, "reference_scans")
    os.makedirs(ref_dir, exist_ok=True)
    for p_num in book_map["special_sections_pdf_pages_1indexed"]["answer_key"]:
        pil_scan = pick_full_page_scan(reader.pages[p_num - 1])
        if pil_scan is not None:
            pil_scan.save(os.path.join(ref_dir, f"answer_key_p{p_num}.png"))

    for p_num in book_map["special_sections_pdf_pages_1indexed"]["listening_tapescripts"]:
        pil_scan = pick_full_page_scan(reader.pages[p_num - 1])
        if pil_scan is not None:
            pil_scan.save(os.path.join(ref_dir, f"tapescript_p{p_num}.png"))

    print("Hoàn tất! Toàn bộ ảnh đã sẵn sàng trong thư mục:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
