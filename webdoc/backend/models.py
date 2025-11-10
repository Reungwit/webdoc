from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email


class BackendCustomUser(models.Model):
    user_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'backend_customuser'


class DocIntroduction(models.Model):
    doc_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(                   # <-- เปลี่ยนตรงนี้
        settings.AUTH_USER_MODEL,               # ใช้ auth user เดียวกับระบบ
        on_delete=models.DO_NOTHING,
        db_column='user_id',
        related_name='doc_introductions',)

    # ชื่อโครงงาน
    name_pro_th = models.CharField(max_length=255, blank=True, null=True)
    name_pro_en = models.CharField(max_length=255, blank=True, null=True)

    # ผู้จัดทำ (JSON: {"th": [...], "en": [...]})
    student_name = models.JSONField(blank=True, null=True)

    # ปีการศึกษา
    school_y_BE = models.IntegerField(blank=True, null=True)
    school_y_AD = models.IntegerField(blank=True, null=True)

    # กรรมการ
    comm_dean    = models.CharField(max_length=255, blank=True, null=True)
    comm_prathan = models.CharField(max_length=255, blank=True, null=True)
    comm_first   = models.CharField(max_length=255, blank=True, null=True)
    comm_sec     = models.CharField(max_length=255, blank=True, null=True)

    # อาจารย์ที่ปรึกษา
    advisor_th   = models.CharField(max_length=200, blank=True, null=True)
    advisor_en   = models.CharField(max_length=200, blank=True, null=True)

    # อาจารย์ที่ปรึกษาร่วม (ใน DB เก็บ JSON → ถ้าอยากให้เป็น string ธรรมดา ค่อยเปลี่ยนสคีมา)
    coadvisor_th = models.JSONField(blank=True, null=True)
    coadvisor_en = models.JSONField(blank=True, null=True)

    # ภาควิชา
    dep_th = models.CharField(max_length=255, blank=True, null=True)
    dep_en = models.CharField(max_length=255, blank=True, null=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'doc_introduction'

class SpProject(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        to_field='user_id'
    )
    name_pro_th = models.CharField(max_length=255)
    name_pro_en = models.CharField(max_length=255)
    case_stu = models.CharField(max_length=100)
    term = models.CharField(max_length=50)
    school_y = models.CharField(max_length=10)
    adviser = models.CharField(max_length=255)
    co_advisor = models.CharField(max_length=255, blank=True, null=True)
    strategic = models.TextField()
    plan = models.TextField()
    key_result = models.TextField()
    bg_and_sig_para1 = models.TextField(default='')
    bg_and_sig_para2 = models.TextField(default='')
    bg_and_sig_para3 = models.TextField(default='')
    purpose_1 = models.CharField(max_length=255, default='')
    purpose_2 = models.CharField(max_length=255, default='')
    purpose_3 = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'sp_project'

class SpProjectAuthor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='userid',
        to_field='user_id',
        related_name='sp_project_authors'
    )
    
    # ✅ FK ไป sp_project.id
    project = models.ForeignKey(
        'SpProject',
        on_delete=models.CASCADE,
        db_column='sp_id',         # ใช้ชื่อคอลัมน์จริงใน DB
        to_field='id'              # FK ชี้ไปยัง SpProject.id
    )

    class Meta:
        db_table = 'sp_project_author'
        managed = False  # เนื่องจากคุณสร้างตารางเองใน MySQL
# ตั้งตามชื่อตาราง แต่ต้องขึ้นต้นด้วยพิมพ์ใหญ่
class DocCover(models.Model):
    cover_id = models.AutoField(primary_key=True)
    project_name_th = models.CharField(max_length=500, null=True)
    project_name_en = models.CharField(max_length=500, null=True)
    author1_name_th = models.CharField(max_length=255, null=True)
    author2_name_th = models.CharField(max_length=255, null=True)
    author1_name_en = models.CharField(max_length=255, null=True)
    author2_name_en = models.CharField(max_length=255, null=True)
    academic_year = models.CharField(max_length=10, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        to_field='user_id'
    )

    class Meta:
        db_table = 'doc_cover'
        managed = False  # เพราะคุณสร้างตารางเองใน phpMyAdmin



#แก้ไขเพิ่มมา
# สร้างโมเดลใหม่สำหรับบทคัดย่อและกิตติกรรมประกาศ
# project/app/models.py

class DocAbstract(models.Model):
    
    doc_id = models.AutoField(primary_key=True) 
    # One-to-one relationship กับ User model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        to_field='user_id'
    )
    total_pages = models.IntegerField()
    keyword_th = models.CharField(max_length=200)
    keyword_en = models.CharField(max_length=200)
    
    # ใช้ JSONField ของ Django สำหรับเก็บข้อมูล JSON โดยตรง
    abstract_th_json = models.JSONField(default=list)
    abstract_en_json = models.JSONField(null=True, blank=True, default=list)
    acknow_json = models.JSONField(
        verbose_name="", 
        null=True, 
        blank=True, 
        default=list
    )

    class Meta:
        db_table = 'doc_abstract' # กำหนดชื่อตารางในฐานข้อมูล

    def __str__(self):
        return f"Abstract for {self.user.username}"
    
# โมเดลใบรับรองปริญญานิพนธ์ (อิงตาราง certificate เดิม)
class Certificate(models.Model):
    # คีย์หลักอัตโนมัติ (ตามตาราง)
    id = models.AutoField(primary_key=True)  # คอลัมน์ id

    # FK ไปยัง backend_customuser.user_id
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,         # อิง CustomUser
        on_delete=models.CASCADE,         # ลบผู้ใช้ -> ลบใบรับรองตาม
        db_column='user_id',              # คอลัมน์ในตาราง certificate
        to_field='user_id',               # อิงฟิลด์ user_id ของ CustomUser
        related_name='certificates',      # ชื่อ reverse relation
    )

    # ข้อมูลหลัก
    topic = models.CharField(max_length=255)                         # เรื่อง (หัวข้อเล่ม)
    dean = models.CharField(max_length=255)                          # คณบดี
    author1 = models.CharField(max_length=255)                       # ผู้จัดทำคนที่ 1
    author2 = models.CharField(max_length=255, null=True, blank=True) # ผู้จัดทำคนที่ 2 (ไม่บังคับ)

    # คณะกรรมการสอบ
    chairman = models.CharField(max_length=255)                       # ประธานกรรมการ
    committee1 = models.CharField(max_length=255)                     # กรรมการคนที่ 1
    committee2 = models.CharField(max_length=255, null=True, blank=True)  # กรรมการคนที่ 2 (ไม่บังคับ)

    # เวลา (ในตารางตั้ง default อยู่แล้ว ให้ Django ไม่ไปแตะ)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'certificate'   # ชื่อตารางจริง
        managed = False            # ตารางมีอยู่แล้ว ไม่ให้ Django migrate

    def __str__(self):
        return f'Certificate({self.user_id} : {self.topic})'

class Chapter1(models.Model):
   
    chapter_id = models.AutoField(
        primary_key=True,
        help_text="PK: รหัสรายการ (อัตโนมัติ)"
    )

    # 1.1 ความเป็นมาและความสำคัญของปัญหา (3 ย่อหน้า)
    sec11_p1 = models.TextField(null=True, blank=True,
                                help_text="1.1 ย่อหน้า 1")
    sec11_p2 = models.TextField(null=True, blank=True,
                                help_text="1.1 ย่อหน้า 2")
    sec11_p3 = models.TextField(null=True, blank=True,
                                help_text="1.1 ย่อหน้า 3")

    # 1.2 วัตถุประสงค์ของการวิจัย (สูงสุด 3 ข้อ)
    purpose_count = models.PositiveSmallIntegerField(default=0,
                                help_text="จำนวนวัตถุประสงค์ที่ผู้ใช้กรอก (0-3)")
    purpose_1 = models.CharField(max_length=500, null=True, blank=True,
                                 help_text="วัตถุประสงค์ ข้อที่ 1 (1.2.1)")
    purpose_2 = models.CharField(max_length=500, null=True, blank=True,
                                 help_text="วัตถุประสงค์ ข้อที่ 2 (1.2.2)")
    purpose_3 = models.CharField(max_length=500, null=True, blank=True,
                                 help_text="วัตถุประสงค์ ข้อที่ 3 (1.2.3)")

    # 1.3 สมมติฐานของการวิจัย
    hypo_paragraph = models.TextField(null=True, blank=True,
                                      help_text="1.3 ย่อหน้า")
    hypo_items_json = models.JSONField(null=True, blank=True,
                                       help_text="1.3.x รายการสมมติฐานย่อย ")

    # 1.4 ขอบเขตของการวิจัย (หัวข้อหลัก/ย่อย)
    scope_json = models.JSONField(null=True, blank=True,
                                  help_text='1.4 ขอบเขต (JSON array ของ object: [{"main":"...","subs":["..."]}])')

    # 1.5 ข้อตกลงเบื้องต้น
    para_premise = models.JSONField(null=True, blank=True,
                                    help_text="1.5 ข้อตกลงเบื้องต้น (ย่อหน้า/รายละเอียด) - เก็บเป็น JSON ตามที่ใช้งาน")
    premise_json = models.JSONField(null=True, blank=True,
                                    help_text='1.5 หัวข้อหลัก/ย่อย (JSON array ของ object แบบเดียวกับ scope_json)')

    # 1.6 นิยามศัพท์เฉพาะ (ไม่มี paragraph)
    def_items_json = models.JSONField(null=True, blank=True,
                                      help_text="1.6.x รายการนิยามศัพท์ (JSON array ของ string)")

    # 1.7 ประโยชน์ที่คาดว่าจะได้รับ (ไม่มี paragraph)
    benefit_items_json = models.JSONField(null=True, blank=True,
                                          help_text="1.7.x รายการประโยชน์ที่คาดว่าจะได้รับ (JSON array ของ string)")

    # เวลาสร้าง (ใน DB ตั้ง DEFAULT CURRENT_TIMESTAMP ไว้อยู่แล้ว)
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text="เวลาที่สร้างข้อมูล")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        to_field='user_id'
    )

    class Meta:
        managed = False          # ไม่ให้ Django สร้าง/แก้โครงสร้างตาราง
        db_table = 'chapter_1'
        
class RefWebsite(models.Model):
    ref_web_id = models.AutoField(primary_key=True)   # PK
    ref_no = models.CharField(max_length=10)          # ลำดับรายการ (1,2,3,...)

    # ผู้แต่ง (เก็บเป็น list[str]) แยกไทย/อังกฤษ
    ref_web_authors_th = models.JSONField()
    ref_web_authors_en = models.JSONField()

    # ชื่อเรื่องหน้าเว็บ แยกไทย/อังกฤษ
    ref_web_title_th = models.CharField(max_length=255)
    ref_web_title_en = models.CharField(max_length=255)

    # URL และวันที่เข้าถึง
    ref_url = models.CharField(max_length=255)
    ref_date_access = models.DateField()

    # FK ไปยัง backend_customuser.user_id
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        to_field='user_id',
        related_name='ref_websites',
    )

    class Meta:
        db_table = 'doc_ref_web'   
        managed = False

    def __str__(self):
        return f'{self.user_id} #{self.ref_no}'
    

class RefBook(models.Model):
    
    ref_book_id = models.AutoField(primary_key=True)
    # JSON ผู้แต่ง
    book_authors_en = models.JSONField(blank=True, null=True)
    # คอลัมน์ TH เป็น NOT NULL ใน DB → ตั้ง default=list เพื่อไม่ส่ง NULL ตอน insert
    book_authors_th = models.JSONField(default=list, blank=True)
    # ชื่อเรื่อง
    book_title_en = models.CharField(max_length=255, blank=True, null=True)
    # TH เป็น NOT NULL → ให้ default='' เพื่อกัน NULL
    book_title_th = models.CharField(max_length=255, default='', blank=True)

    # ครั้งที่พิมพ์
    book_print_count_en = models.IntegerField(blank=True, null=True)
    # TH เป็น NOT NULL → ให้ default=0 (แก้ภายหลังได้ถ้าต้องการบังคับกรอก)
    book_print_count_th = models.IntegerField(default=0, blank=True)

    # เมืองที่พิมพ์
    book_city_print_en = models.CharField(max_length=255, blank=True, null=True)
    book_city_print_th = models.CharField(max_length=255, default='', blank=True)

    # สำนักพิมพ์
    book_publisher_en = models.CharField(max_length=255, blank=True, null=True)
    book_publisher_th = models.CharField(max_length=255, default='', blank=True)

    # ปีที่พิมพ์
    book_y_print_en = models.IntegerField(blank=True, null=True)
    book_y_print_th = models.IntegerField(default=0, blank=True)

    # FK → backend_customuser.user_id
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        to_field='user_id',
        db_column='user_id',
        on_delete=models.DO_NOTHING,
        related_name='ref_books',
    )

    class Meta:
        managed = False                 # ตารางถูกสร้างใน MySQL อยู่แล้ว
        db_table = 'doc_ref_book'       # ชื่อตารางตามที่แจ้ง

    def __str__(self):
        # แสดงชื่อเรื่องภาษาไทยก่อน ถ้าไม่มีค่อย fallback อังกฤษ
        return (self.book_title_th or self.book_title_en or f"Book #{self.ref_book_id}")


    # FK -> backend_customuser.user_id (PK)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        to_field='user_id',
        db_column='user_id',
        on_delete=models.CASCADE,
        related_name='userid_refbook',
    )

    class Meta:
        managed = False                           
        db_table = 'doc_ref_book'                 
    
    def __str__(self):
        return self.book_title or f"Book #{self.ref_book_id}"
        db_table = 'ref_book'
        managed = False

class DocChapter1(models.Model):
    doc_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        db_column='user_id',
        to_field='user_id',
        db_constraint=False
    )
    intro_body = models.TextField(null=True, blank=True)
    sections_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=False, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        managed = False
        db_table = 'doc_chapter_1'

#     Chapter 5 
class Chapter5(models.Model):
    """
    แมปตารางที่มีอยู่แล้ว (managed=False) ตาม DDL:
    """
    doc_id = models.BigAutoField(primary_key=True)
    # อ้างตารางผู้ใช้ที่ระบบ auth ใช้อยู่จริง ผ่าน AUTH_USER_MODEL
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='fk_user_ct5',
    )
    intro_th = models.TextField(null=True, blank=True)
    sections_json = models.JSONField(default=list)  # เก็บ list[{title, body, mains:[{text, subs[]}], section_order, main_order}]
    created_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)   # ใช้ค่าจาก DB
    updated_at = models.DateTimeField(auto_now=True)                                # สำหรับ Django ให้ sync เวลาใน obj

    class Meta:
        managed = False              # สำคัญ: ไม่ให้ Django สร้าง/แก้ตาราง
        db_table = 'chapter5'

    def __str__(self):
        return f'Chapter5(doc_id={self.doc_id}, user_id={self.user_id})'




class DocChapter2(models.Model):
    doc_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="user_id",
        on_delete=models.RESTRICT,
        related_name="chapter2_docs",
    )
    # คอลัมน์ JSON ตามสกีมาที่คุณตั้ง
    intro_body = models.JSONField(blank=True, null=True)
    sections_json = models.JSONField(blank=True, null=True)

    chap_id = models.IntegerField(default=2, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "doc_chapter_2"   # <<< ชื่อตารางจริงใน MySQL ของคุณ
        managed = False              # อย่าให้ Django migrate/สร้างตารางนี้


# ----------------------------
# บทที่ 3: อิงตารางที่มีอยู่แล้วใน MySQL
# ----------------------------
class DocChapter3(models.Model):
    doc_id = models.AutoField(primary_key=True)  # PK: AUTO_INCREMENT
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="user_id",
        on_delete=models.RESTRICT,
        related_name="chapter3_docs",
    )
    intro_body = models.JSONField(blank=True, null=True)
    sections_json = models.JSONField(blank=True, null=True)       # เนื้อหา+รูปภาพ (โครงเดียวกับบท 2)
    tb_sections_json = models.JSONField(blank=True, null=True)    # ตารางของแต่ละหัวข้อ
    chap_id = models.IntegerField(blank=True, null=True, db_column="chap_id")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False                 # ใช้ตารางเดิม (สร้างใน phpMyAdmin)
        db_table = "doc_chapter_3"
        unique_together = (('user',),)  # ให้ update_or_create(user=...) ชี้ตัวเดียว
