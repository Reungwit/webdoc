# from docx import Document
# from docx.enum.text import WD_BREAK
# from docx.enum.section import WD_SECTION

# doc = Document()

# doc.add_paragraph("บทที่ 1: บทนำ")

# # ขึ้นหน้าแบบเร็ว
# doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# doc.add_paragraph("บทที่ 2: วัตถุประสงค์")

# # แยก section พร้อมขึ้นหน้าใหม่
# doc.add_section(WD_SECTION.NEW_PAGE)
# doc.add_paragraph("บทที่ 3: ขอบเขต")

# doc.save("report.docx")


# from docx import Document

# # รับข้อความจากคีย์บอร์ด
# text = input("กรุณาพิมพ์ข้อความ: ")

# # นับจำนวนตัวอักษร (ไม่รวมช่องว่าง)
# num_chars = len(text.replace(" ", ""))
# print(f"จำนวนตัวอักษร (ไม่นับช่องว่าง): {num_chars}")

# สร้างไฟล์ docx และเพิ่มข้อความลงไป


# compare_tokenizers.py
# เปรียบเทียบการตัดคำด้วย newmm, attacut, deepcut + วัดเวลา + สรุปความต่าง

import time
from collections import OrderedDict

# ====== ตรวจว่าโมดูลเสริมพร้อมไหม ======
def is_available(modname: str) -> bool:
    try:
        __import__(modname)
        return True
    except Exception:
        return False

have_attacut = is_available("attacut")
have_deepcut = is_available("deepcut")

from pythainlp.tokenize import word_tokenize

# ====== ข้อความทดสอบ (แก้ไข/เพิ่มได้) ======
samples = OrderedDict([
    ("ชื่อเฉพาะ", "ฉันเรียนที่มหาวิทยาลัยขอนแก่น คณะวิศวกรรมศาสตร์"),
    ("คำประสม", "วันนี้อากาศร้อนแต่ฉันยังอยากกินชานมไข่มุก"),
    ("ภาษาพูด/โซเชียล", "เดี๋ยวแวะ 7-11 แป๊บนึงนะ เดี๋ยวกลับมา"),
    ("คำใหม่/เทค", "กำลังเรียนวิชาเทคโนโลยีสารสนเทศและ data science"),
])

# ====== รายการเอนจินที่จะทดสอบ ======
engines = ["newmm"]
if have_attacut:
    engines.append("attacut")
else:
    print("[!] ข้าม attacut (ไม่พบโมดูล attacut)")

if have_deepcut:
    engines.append("deepcut")
else:
    print("[!] ข้าม deepcut (ไม่พบโมดูล deepcut)")

# ====== ฟังก์ชันช่วยแสดงผล ======
def tokenize_with_time(text: str, engine: str):
    t0 = time.perf_counter()
    tokens = word_tokenize(text, engine=engine)
    t1 = time.perf_counter()
    return tokens, (t1 - t0)

def pretty(tokens):
    # แสดงผลแบบอ่านง่าย: คั่นด้วย | และมีช่องว่าง
    return " | ".join(tokens)

def compare_sets(results_dict):
    """
    สรุปความต่างแบบง่ายด้วยเซ็ต:
    - unique ของแต่ละเอนจิน (โทเค็นที่เอนจินหนึ่งมี แต่อีกเอนจินไม่มี)
    หมายเหตุ: ใช้ set จะไม่รักษาลำดับ แต่ช่วยชี้ให้เห็นโทเค็นที่ต่างกันชัด ๆ
    """
    engines = list(results_dict.keys())
    sets = {e: set(results_dict[e]) for e in engines}
    union_all = set().union(*sets.values())
    summary = {}
    for e in engines:
        others = set().union(*(sets[oe] for oe in engines if oe != e))
        summary[e] = sorted(list(sets[e] - others), key=lambda s: (len(s), s))
    return summary, union_all

# ====== รันและแสดงผล ======
for title, text in samples.items():
    print("\n" + "="*80)
    print(f"[เคส] {title}")
    print("-"*80)
    print(f"ข้อความ: {text}\n")

    per_engine_tokens = {}
    for eng in engines:
        toks, sec = tokenize_with_time(text, eng)
        per_engine_tokens[eng] = toks
        print(f"{eng:<8} ({sec*1000:.2f} ms): {pretty(toks)}")

    # สรุปความต่างแบบ set
    diff, union_all = compare_sets(per_engine_tokens)
    print("\n[สรุปความต่างแบบโทเค็นเฉพาะของแต่ละเอนจิน]")
    for eng in engines:
        only_here = diff[eng]
        if only_here:
            print(f" - เฉพาะ {eng}: {', '.join(only_here)}")
        else:
            print(f" - เฉพาะ {eng}: (ไม่มี)")

# ====== สรุปแนวทางเลือกใช้ (ข้อความกำกับ) ======
print("\n" + "="*80)
print("คำแนะนำโดยสรุป:")
print("- newmm   : เบา เร็ว พึ่งพาพจนานุกรม เหมาะกับงานทั่วไป/ทรัพยากรจำกัด")
if have_attacut:
    print("- attacut : โมเดล Neural (BiLSTM-CRF) เก่งชื่อเฉพาะ/คำประสม")
else:
    print("- attacut : (ไม่ได้รันทดสอบ - ไม่พบโมดูล)")
if have_deepcut:
    print("- deepcut : โมเดล Neural (CNN+BiLSTM) เสถียรกับข้อความยาว/โซเชียล")
else:
    print("- deepcut : (ไม่ได้รันทดสอบ - ไม่พบโมดูล)")


