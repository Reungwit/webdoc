from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import JSONField


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email


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
    bg_and_sig_para1 = models.TextField()
    bg_and_sig_para2 = models.TextField()
    bg_and_sig_para3 = models.TextField()
    purpose_1 = models.CharField(max_length=255)
    purpose_2 = models.CharField(max_length=255)
    purpose_3 = models.CharField(max_length=255)
    scope_json = JSONField(blank=True, null=True)
    
    class Meta:
        db_table = 'sp_project'

class SpProjectAuthor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    userid = models.IntegerField()  # FK ไป backend_customuser.user_id (คุณอาจ map เพิ่มภายหลัง)
    
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
class Abstract(models.Model):
    abstract_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        to_field='user_id'
    )
    # ข้อมูลเอกสาร
    project_name_th = models.TextField(null=True, blank=True)
    project_name_en = models.TextField(null=True, blank=True)
    major_th = models.TextField(null=True, blank=True)
    major_en = models.TextField(null=True, blank=True)
    advisor_th = models.CharField(max_length=255, null=True, blank=True)
    advisor_en = models.CharField(max_length=255, null=True, blank=True)
    coadvisor_th = models.CharField(max_length=255, null=True, blank=True)
    coadvisor_en = models.CharField(max_length=255, null=True, blank=True)
    academic_year_th = models.IntegerField(null=True, blank=True)
    academic_year_en = models.IntegerField(null=True, blank=True)

    # 🔹 จำนวนหน้า
    total_pages = models.IntegerField(null=True, blank=True)

    # บทคัดย่อ
    abstract_th_para1 = models.TextField(null=True, blank=True)
    abstract_th_para2 = models.TextField(null=True, blank=True)
    abstract_en_para1 = models.TextField(null=True, blank=True)
    abstract_en_para2 = models.TextField(null=True, blank=True)
    keyword_th = models.TextField(null=True, blank=True)
    keyword_en = models.TextField(null=True, blank=True)

    # ผู้จัดทำ
    author1_th = models.CharField(max_length=255, null=True, blank=True)
    author1_en = models.CharField(max_length=255, null=True, blank=True)
    author2_th = models.CharField(max_length=255, null=True, blank=True)
    author2_en = models.CharField(max_length=255, null=True, blank=True)

    # กิตติกรรมประกาศ
    acknow_para1 = models.TextField(null=True, blank=True)
    acknow_para2 = models.TextField(null=True, blank=True)
    acknow_name1 = models.CharField(max_length=255, null=True, blank=True)
    acknow_name2 = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'abstract'

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
        
#บรรณานุกรมเว็บไซต์
class RefWebsite(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="PK: รหัสรายการอ้างอิงเว็บไซต์")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        to_field='user_id',
        help_text="FK: อ้างอิงผู้ใช้"
    )
    number = models.IntegerField(null=True, blank=True, help_text="ลำดับการอ้างอิง")
    authors_th_json = models.JSONField(help_text="ผู้แต่งภาษาไทย (JSON array)")
    authors_en_json = models.JSONField(help_text="ผู้แต่งภาษาอังกฤษ (JSON array)")
    title_th = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    site_name_th = models.CharField(max_length=255, null=True, blank=True)
    site_name_en = models.CharField(max_length=255, null=True, blank=True)
    year = models.SmallIntegerField(null=True, blank=True)
    month = models.SmallIntegerField(null=True, blank=True)
    day = models.SmallIntegerField(null=True, blank=True)
    url = models.CharField(max_length=1000)
    accessed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ref_website'
        managed = False

#บรรณานุกรมหนังสือ
class RefBook(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="PK: รหัสรายการอ้างอิงหนังสือ")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        to_field='user_id',
        help_text="FK: อ้างอิงผู้ใช้"
    )
    number = models.IntegerField(null=True, blank=True, help_text="ลำดับการอ้างอิง")
    authors_th_json = models.JSONField(help_text="ผู้แต่งภาษาไทย (JSON array)")
    authors_en_json = models.JSONField(help_text="ผู้แต่งภาษาอังกฤษ (JSON array)")
    title_th = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    edition_th = models.CharField(max_length=50, null=True, blank=True)
    edition_en = models.CharField(max_length=50, null=True, blank=True)
    publisher_place_th = models.CharField(max_length=255, null=True, blank=True)
    publisher_place_en = models.CharField(max_length=255, null=True, blank=True)
    publisher_th = models.CharField(max_length=255, null=True, blank=True)
    publisher_en = models.CharField(max_length=255, null=True, blank=True)
    year = models.SmallIntegerField(null=True, blank=True)
    doi = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=1000, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ref_book'
        managed = False



#     Chapter 5 
# backend/models.py
class Chapter5(models.Model):
    """
    แมปตารางที่มีอยู่แล้ว (managed=False) ตาม DDL:
    CREATE TABLE chapter5 (
        doc_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT NOT NULL,
        intro_th LONGTEXT NULL,
        sections_json JSON NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES backend_customuser(id) ON DELETE CASCADE
    );
    """
    doc_id = models.BigAutoField(primary_key=True)
    # อ้างตารางผู้ใช้ที่ระบบ auth ใช้อยู่จริง ผ่าน AUTH_USER_MODEL
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='chapter5_docs',
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

