from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import JSONField
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

