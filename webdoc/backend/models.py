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

class DocCover(models.Model):
    cover_id = models.AutoField(primary_key=True)  # ใช้ cover_id เป็น PK
    project_name_th = models.CharField(max_length=500)
    project_name_en = models.CharField(max_length=500)
    author1_name_th = models.CharField(max_length=255)
    author2_name_th = models.CharField(max_length=255, blank=True, null=True)
    author1_name_en = models.CharField(max_length=255)
    author2_name_en = models.CharField(max_length=255, blank=True, null=True)
    academic_year = models.CharField(max_length=10)

    class Meta:
        db_table = 'doc_cover'

    def __str__(self):
        return f"{self.project_name_th} ({self.academic_year})"
